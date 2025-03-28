from configs import player_status
from params import DEBUFF_PERCENTAGE, DEBUFF_TURNS, STUN_TURNS

class Player:
    def __init__(self):
        self.Life = player_status['Life']
        self.Dinheiro = player_status['Dinheiro']
        self.Velocidade = player_status['Velocidade']
        self.Forca = player_status['Forca']
        self.Precisao = player_status['Precisao']
        self.Armadura = player_status['Armadura']
        self.debuffed = False
        self.debuff_turns_left = 0
        self.debuff_percentage = 0
        self.stuned = False
        self.stun_turns_left = 0
        self.pos = (0, 0)
        self.type = 1

    def get_player_status(self):
        player_status = {
            "Life": self.Life,
            "Dinheiro": self.Dinheiro,
            "Velocidade": self.Velocidade * (1-self.debuff_percentage),
            "Forca": self.Forca * (1-self.debuff_percentage),
            "Precisao": self.Precisao * (1-self.debuff_percentage),
            "Armadura": self.Armadura * (1-self.debuff_percentage)
        }
        return player_status

    def apply_debuff(self):
        self.debuffed = True
        self.debuff_percentage = DEBUFF_PERCENTAGE
        self.debuff_turns_left = DEBUFF_TURNS

    def debuff_countdown(self):
        self.debuff_turns_left = self.debuff_turns_left - 1 if self.debuff_turns_left > 0 else self.debuff_turns_left
        if self.debuff_turns_left <= 0:
            self.cure_debuff()

    def cure_debuff(self):
        self.debuffed = False
        self.debuff_percentage = 0

    def apply_stun(self):
        self.stuned = True
        self.stun_turns_left = STUN_TURNS

    def stun_countdown(self):
        self.stun_turns_left = self.stun_turns_left - 1 if self.stun_turns_left > 0 else self.stun_turns_left
        if self.stun_turns_left <= 0:
            self.cure_stun()
        print(f'self.stun_turns_left: {self.stun_turns_left}')
        print(f'self.stuned: {self.stuned}')

    def cure_stun(self):
        self.stuned = False

    def is_debuffed(self):
        return self.debuffed
    def get_debuff_turns_left(self):
        return self.debuff_turns_left

    def is_stuned(self):
        return self.stuned

    def get_stun_turns_left(self):
        return self.stun_turns_left
