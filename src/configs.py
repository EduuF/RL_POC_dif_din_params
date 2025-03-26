# Cores
COLORS = {
    0: (50, 50, 50),  # Vazio
    1: (0, 255, 0),  # Player
    2: (200, 200, 200),  # Minion Arqueiro
    3: (100, 100, 100),  # Minion Guerreiro
    4: (128, 0, 128),  # Minion Mago
    5: (255, 255, 100),  # Trap Debuff
    6: (200, 200, 50),  # Trap Stun
    7: (150, 0, 0)  # Boss
}

ELEMENTS = {
    0: "Empty",
    1: "Player",
    2: "Arqueiro",
    3: "Guerreiro",
    4: "Mago",
    5: "Trap de Debuff",
    6: "Trap de Stun",
    7: "Boss"
}

SHAPES = {
    0: "square",
    1: "circle",
    2: "triangle",
    3: "triangle",
    4: "triangle",
    5: "square",
    6: "square_x",
    7: "x"
}

# Status do Player
player_status = {
    "Life": 100.0,
    "Dinheiro": 100.0,
    "Velocidade": 1.0,
    "Forca": 10.0,
    "Precisao": 80.0,
    "Magia": 10.0,
    "Armadura": 5.0,
    "Escudo Magico": 3.0
}

minion_arqueiro_status = {
    "Life": 10,
    "Velocidade": 1.2,
    "Forca": 8.0,
    "Precisao": 60.0,
    "Magia": 0.0,
    "Armadura": 4.0,
    "Escudo Magico": 1.0
}

minion_guerreiro_status = {
    "Life": 20,
    "Velocidade": 0.8,
    "Forca": 12.0,
    "Precisao": 80.0,
    "Magia": 0.0,
    "Armadura": 7.0,
    "Escudo Magico": 2.0
}

minion_mago_status = {
    "Life": 15,
    "Velocidade": 0.5,
    "Forca": 3.0,
    "Precisao": 90.0,
    "Magia": 10.0,
    "Armadura": 2.0,
    "Escudo Magico": 10.0
}