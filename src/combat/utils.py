from typing import List, Dict
import numpy as np
from math import exp, pi, sqrt, inf
import random
from dotenv import load_dotenv
import os

from params import SAFE_ZONE_RADIUS, FOV_PLAYER
from Player.player import Player

load_dotenv()

GRID_SIZE = int(os.getenv('GRID_SIZE'))

def calculate_manhattan_distance(first_point_coords: List[int], second_point_coords: List[int]) -> int:
    return abs(first_point_coords[0] - second_point_coords[0]) + abs(first_point_coords[1] - second_point_coords[1])


def check_damage_applicability(player_pos: List[int], minion_pos: List[int], minion_type: int):
    distance = calculate_manhattan_distance(player_pos, minion_pos)

    # Inicializando as variáveis
    player_deal_dist_damage = False
    player_deal_meelee_damage = False
    player_takes_meelee_damage = False
    player_takes_dist_damage = False

    if distance <= SAFE_ZONE_RADIUS:
        player_deal_dist_damage = True
        if minion_type == 4:
            player_takes_magic_damage = True
        if minion_type == 2:
            player_takes_dist_damage = True

        if distance <= 1:
            player_deal_meelee_damage = True
            if minion_type == 3:
                player_takes_meelee_damage = True


        if minion_type in [2, 3]:  # Minion tipo 2 ou 3 pode causar dano
            player_takes_dist_damage = True
        if distance <= 1:  # Distância de 1 significa que o dano de "melee" é aplicável
            player_deal_meelee_damage = True
            if minion_type == 3:  # Minion tipo 3 pode causar dano "melee"
                player_takes_meelee_damage = True

    return distance, player_deal_dist_damage, player_deal_meelee_damage, player_takes_dist_damage, player_takes_meelee_damage


# Função para gerar dano com base na distribuição normal
def generate_damage(median: float, min_damage_factor: float = 0.6, max_damage_factor: float = 1.5) -> float:
    # Média do dano é a mediana
    mean = median
    # Desvio padrão, determinando a variação no dano
    stddev = (max_damage_factor - min_damage_factor) * median / 6  # Aproximadamente 99% de chance de estar entre min e max

    # Gerar um valor de dano com uma distribuição normal
    damage = random.gauss(mean, stddev)

    # Garantir que o dano nunca seja negativo
    return max(0, damage)

def generate_damage(median_damage):
    """Gerar dano aleatório com base na mediana (normal)."""
    return random.uniform(median_damage * 0.5, median_damage * 1.5)

def calculate_crit_chance(precision):
    """Modelo ajustado para a chance de crítico considerando a precisão."""
    # Curva sigmoide para chances de crítico
    return 0.1 + (0.8 / (1 + np.exp(-0.05 * (precision - 50))))

def sigmoid(attacker_power, defender_power):
    """
    Modelo de dano a distancia (Sigmoid alterada)
    - Não linear
    - Nunca zero
    """
    atk_factor = (attacker_power-defender_power)
    return 1 / (1 + np.exp(-atk_factor))

def calculate_damage(attacker, defender, damage_type):
    """Função principal para calcular o dano de acordo com o tipo de dano."""
    if damage_type == "distancia":
        attacker_accuracy = attacker.Precisao
        attacker_power = attacker.Forca
        defender_power = defender.Armadura
        median_damage = sigmoid(attacker_power, defender_power)

        # Chance de acerto
        accuracy_factor = random.random()

        # Falha crítica
        if accuracy_factor > attacker_accuracy/100:
            return 0

        # Chance de acerto crítico
        crit_chance = calculate_crit_chance(attacker_accuracy)
        if accuracy_factor < crit_chance:
            return generate_damage(median_damage) * 2  # Dano crítico

        return generate_damage(median_damage) * (attacker_accuracy * 2)/100

    if damage_type == "meelee":
        attacker_accuracy = attacker.Precisao
        attacker_power = attacker.Forca
        defender_power = defender.Armadura
        median_damage = sigmoid(attacker_power, defender_power)

        # Chance de acerto
        accuracy_factor = random.random()

        # Falha crítica
        if accuracy_factor > attacker_accuracy/100:
            return 0

        # Chance de acerto crítico
        crit_chance = calculate_crit_chance(attacker_accuracy)
        if accuracy_factor < crit_chance:
            return generate_damage(median_damage) * 2  # Dano crítico

        return generate_damage(median_damage)

def do_fight(grid: List[List], player: Player, fight_scenario: Dict):
    for id, fight_summary in fight_scenario.items():
        enemy_pos = fight_summary['pos']
        enemy = grid[enemy_pos[0]][enemy_pos[1]]

        total_taken_damage = 0
        total_dealt_damage = 0

        if fight_summary['player_deal_dist_damage']:
            damage = calculate_damage(player, enemy, "distancia")
            total_dealt_damage += max(0,damage)
            print(f'player_deal_dist_damage: {id}')
        if fight_summary['player_deal_meelee_damage']:
            damage = calculate_damage(player, enemy, "meelee")
            total_dealt_damage += max(0,damage)
        if fight_summary['player_takes_dist_damage']:
            damage = calculate_damage(enemy, player, "distancia")
            total_taken_damage += max(0,damage)
        if fight_summary['player_takes_meelee_damage']:
            damage = calculate_damage(enemy, player, "distancia")
            total_taken_damage += max(0,damage)

        player.Life -= total_taken_damage
        enemy.Life -= total_dealt_damage
        print(f'total_taken_damage: {total_taken_damage}')
        print(f'total_dealt_damage: {total_dealt_damage}')
        print(f"id: {enemy.id} | Life {enemy.Life}")
        print(f"Player: {player.Life}")

        if enemy.Life <= 0:
            print(f"id: {enemy.id} morreu")
            grid[enemy.pos[0]][enemy.pos[1]] = 0

    return grid



def search_fight(grid: List[List], player: Player):
    fight_scenario = {}
    px, py = player.pos  # Posição do player no grid

    for nx in range(max(0, px - FOV_PLAYER), min(GRID_SIZE, px + FOV_PLAYER + 1)):  # Garante que nx está dentro do grid
        for ny in range(max(0, py - FOV_PLAYER),min(GRID_SIZE, py + FOV_PLAYER + 1)):  # Garante que ny está dentro do grid
            # Verifica se a distância de Manhattan é menor ou igual ao FOV
            if abs(nx - px) + abs(ny - py) > FOV_PLAYER:
                continue
            if grid[nx][ny] == 0:
                continue
            enemy = grid[nx][ny]
            if enemy.type in [2,3]:
                distance, player_deal_dist_damage, player_deal_meelee_damage, player_takes_dist_damage, player_takes_meelee_damage = check_damage_applicability(player.pos, enemy.pos, enemy.type)
                print(f'ID: {enemy.id} | Dis: {distance} | Ene. pos: {enemy.pos} | P. pos.: {player.pos} | pddd: {player_deal_dist_damage} | pdmd: {player_deal_meelee_damage} | ptdd: {player_takes_dist_damage} | ptmd: {player_takes_meelee_damage}')
                if player_deal_dist_damage or player_deal_meelee_damage or player_takes_dist_damage or player_takes_meelee_damage:
                    fight_scenario[enemy.id] = {"pos": enemy.pos, "player_deal_dist_damage": player_deal_dist_damage, "player_deal_meelee_damage": {player_deal_meelee_damage}, "player_takes_dist_damage": {player_takes_dist_damage}, "player_takes_meelee_damage": {player_takes_meelee_damage}}


    print(f'fight_scenario: {fight_scenario}')
    # Procurar qual inimigo no campo de visão com menor life para que ele seja o alvo da flecha
    less_life_enemy_life = float(inf)
    less_life_enemy_id = None
    for id, fight_summary in fight_scenario.items():
        enemy_pos = fight_scenario[id]['pos']
        print(f'enemy_pos: {enemy_pos}')
        enemy = grid[enemy_pos[0]][enemy_pos[1]]
        print(f'enemy: {enemy}')

        if enemy.Life < less_life_enemy_life:
            less_life_enemy_life = enemy.Life
            less_life_enemy_id = enemy.id
        else:
            fight_scenario[id]['player_deal_dist_damage'] = False

    print(f'less_life_enemy_id: {less_life_enemy_id} | less_life_enemy_life: {less_life_enemy_life}')



    grid = do_fight(grid, player, fight_scenario)
    return grid




#TODO Função que verifica se o dano é aplicável a um minion ou ao player (Arqueiros e Magos dão dano a distancia e Guerreiros meelee)
#TODO Função que aplica X de dano ao minion
#TODO Função que aplica X de dano ao player
#Todo Caso o dano seja aplicável, aplique (Minion e Player)



