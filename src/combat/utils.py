from typing import List, Dict
import numpy as np
from math import exp, pi, sqrt
import random

from params import SAFE_ZONE_RADIUS
def calculate_manhattan_distance(first_point_coords: List[int], second_point_coords: List[int]) -> int:
    return abs(first_point_coords[0] - second_point_coords[0]) + abs(first_point_coords[1] - second_point_coords[1])


def check_damage_applicability(player_pos: List[int], minion_pos: List[int], minion_type: int):
    distance = calculate_manhattan_distance(player_pos, minion_pos)

    # Inicializando as variáveis
    player_deal_dist_damage = False
    player_deal_meelee_damage = False
    player_takes_damage = False

    if distance <= SAFE_ZONE_RADIUS:
        player_deal_dist_damage = True
        if minion_type in [2, 3]:  # Minion tipo 2 ou 3 pode causar dano
            player_takes_damage = True
        if distance == 1:  # Distância de 1 significa que o dano de "melee" é aplicável
            player_deal_meelee_damage = True
            if minion_type == 3:  # Minion tipo 3 pode causar dano "melee"
                player_takes_damage = True

    return player_deal_dist_damage, player_deal_meelee_damage, player_takes_damage


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


# Função principal para calcular o dano
def calculate_damage(attacker_status: Dict, defender_status: Dict, damage_type: str) -> float:
    if damage_type == "distancia":
        attacker_accuracy = attacker_status['Precisão']
        attacker_power = attacker_status['Força'] * 1.3  # Força com fator 1.5 para distância
        defender_power = defender_status['Armadura']

        median_damage = (attacker_power - defender_power) * (attacker_accuracy / 100)

        accuracy_factor = random.random()  # Número aleatório entre 0 e 1

        if accuracy_factor > attacker_accuracy / 100:  # Falha crítica
            return 0

        if accuracy_factor < attacker_accuracy / 200:  # Acerto crítico (50% de chance para o acerto crítico)
            return generate_damage(median_damage) * 2  # Dano crítico (2x da mediana)

        return generate_damage(median_damage)

    if damage_type == "meelee":
        attacker_accuracy = attacker_status['Precisão']
        attacker_power = attacker_status['Força']
        defender_power = defender_status['Armadura']

        median_damage = attacker_power - defender_power

        accuracy_factor = random.random()  # Número aleatório entre 0 e 1

        if accuracy_factor > attacker_accuracy / 100:  # Falha crítica
            return 0

        if accuracy_factor < attacker_accuracy / 200:  # Acerto crítico (50% de chance para o acerto crítico)
            return generate_damage(median_damage) * 2  # Dano crítico (2x da mediana)

        return generate_damage(median_damage)

    if damage_type == "magico":
        attacker_power = attacker_status['Magia']
        defender_power = defender_status['Escudo Mágico']

        median_damage = attacker_power - defender_power

        accuracy_factor = random.random()  # Número aleatório entre 0 e 1

        if accuracy_factor > attacker_status['Precisão'] / 100:  # Falha crítica
            return 0

        if accuracy_factor < attacker_status['Precisão'] / 200:  # Acerto crítico (50% de chance para o acerto crítico)
            return generate_damage(median_damage) * 2  # Dano crítico (2x da mediana)

        return generate_damage(median_damage)

def do_fight(attacker_status: Dict, defender_status: Dict):

    pass

def search_fight(enemies: List, player_status: Dict):

    pass


#TODO Função que verifica se o dano é aplicável a um minion ou ao player (Arqueiros e Magos dão dano a distancia e Guerreiros meelee)
#TODO Função que aplica X de dano ao minion
#TODO Função que aplica X de dano ao player
#Todo Caso o dano seja aplicável, aplique (Minion e Player)



