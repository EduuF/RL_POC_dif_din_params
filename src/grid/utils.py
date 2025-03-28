import pygame
from typing import Dict, List
import numpy as np
from dotenv import load_dotenv
import os

from utils import draw_shape
from configs import COLORS, SHAPES, player_status, ELEMENTS
from params import SAFE_ZONE_RADIUS, DEBUFF_PERCENTAGE, DEBUFF_TURNS, STUN_TURNS, NUM_MINION_ARQUEIRO, NUM_MINION_GUERREIRO, NUM_TRAP_DEBUFF, NUM_TRAP_STUN

load_dotenv()

# Definições básicas
GRID_SIZE = int(os.getenv('GRID_SIZE'))
CELL_SIZE = int(os.getenv('CELL_SIZE'))
INFO_PANEL_WIDTH = int(os.getenv('INFO_PANEL_WIDTH'))
LEGEND_PANEL_HEIGHT = int(os.getenv('LEGEND_PANEL_HEIGHT'))
GRID_WIDTH, GRID_HEIGHT = GRID_SIZE * CELL_SIZE + INFO_PANEL_WIDTH, GRID_SIZE * CELL_SIZE + LEGEND_PANEL_HEIGHT
def draw_grid(screen: pygame.surface.Surface, player_status: Dict, grid: List, font: pygame.font.Font):
    """
    Desenha o grid na tela
    :param screen: Tela
    :param player_status: Status atual do player
    :param grid: Objeto Grid
    """
    screen.fill((0, 0, 0))
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            # Se for int é pq é vazio (0), se não, é objeto
            if isinstance(grid[x][y], int):
                draw_shape(screen, SHAPES[grid[x][y]], COLORS[grid[x][y]], x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE)
            else:
                if grid[x][y].type in [2,3,4,5,6]:
                    draw_shape(screen, SHAPES[grid[x][y].type], COLORS[grid[x][y].type], x * CELL_SIZE, y * CELL_SIZE,CELL_SIZE, grid[x][y].id, font)
                else:
                    draw_shape(screen, SHAPES[grid[x][y].type], COLORS[grid[x][y].type], x * CELL_SIZE, y * CELL_SIZE,CELL_SIZE)

    draw_status_panel(screen, player_status, font)
    draw_legend_panel(screen, font)
    pygame.display.flip()


def draw_legend_panel(screen: pygame.surface.Surface, font: pygame.font.Font):
    """
    Desenha os paineis de legenda da tela
    :param screen: Tela
    :param font: Fonte na qual a legenda será escrita
    """
    y_offset = GRID_SIZE * CELL_SIZE
    pygame.draw.rect(screen, (50, 50, 50), (0, y_offset, GRID_WIDTH, LEGEND_PANEL_HEIGHT))
    for key, value in COLORS.items():
        if key == 0:
            continue
        draw_shape(screen, SHAPES[key], value, 10, y_offset, 20)
        text_surface = font.render(f"{ELEMENTS[key]}", True, (255, 255, 255))
        screen.blit(text_surface, (40, y_offset))
        y_offset += 25


def draw_status_panel(screen: pygame.surface.Surface, player_status: Dict, font: pygame.font.Font):
    """
    Desenha o painel de status na tela
    :param screen: Tela
    :param player_status: Status atual do player
    :param font:  Fonte na qual a legenda será escrita
    """
    panel_x = GRID_SIZE * CELL_SIZE
    pygame.draw.rect(screen, (30, 30, 30), (panel_x, 0, INFO_PANEL_WIDTH, GRID_HEIGHT - LEGEND_PANEL_HEIGHT))
    y_offset = 20
    for key, value in player_status.items():
        text_surface = font.render(f"{key}: {value:.2f}", True, (255, 255, 255))
        screen.blit(text_surface, (panel_x + 10, y_offset))
        y_offset += 30