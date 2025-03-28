# Cores
COLORS = {
    0: (50, 50, 50),  # Vazio
    1: (0, 255, 0),  # Player
    2: (200, 200, 200),  # Minion Arqueiro
    3: (100, 100, 100),  # Minion Guerreiro
    5: (255, 255, 100),  # Trap Debuff
    6: (200, 200, 50),  # Trap Stun
    7: (150, 0, 0)  # Boss
}

ELEMENTS = {
    0: "Empty",
    1: "Player",
    2: "Arqueiro",
    3: "Guerreiro",
    5: "Trap de Debuff",
    6: "Trap de Stun",
    7: "Boss"
}

SHAPES = {
    0: "square",
    1: "circle",
    2: "triangle",
    3: "triangle",
    5: "square",
    6: "square_x",
    7: "x"
}

# Status do Player
player_status = {
    "Life": 100.0,
    "Dinheiro": 100.0,
    "Velocidade": 1.5,
    "Forca": 2.0,
    "Precisao": 60.0,
    "Armadura": 1.0,
}

minion_arqueiro_status = {
    "Life": 30,
    "Velocidade": 1.2,
    "Forca": 1.5,
    "Precisao": 80.0,
    "Armadura": 0.5,
}

minion_guerreiro_status = {
    "Life": 50,
    "Velocidade": 0.8,
    "Forca": 2.5,
    "Precisao": 60.0,
    "Armadura": 1.5,
}
