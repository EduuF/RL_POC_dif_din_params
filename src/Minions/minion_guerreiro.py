from configs import minion_guerreiro_status
from Minions.base_minion import Base_minion


class Minion_guerreiro(Base_minion):
    def __init__(self, id, minion_pos):
        super().__init__()

        # Inicializa os atributos específicos do Minion Arqueiro
        self.id = id
        self.Life = minion_guerreiro_status['Life']
        self.Velocidade = minion_guerreiro_status['Velocidade']
        self.Forca = minion_guerreiro_status['Forca']
        self.Precisao = minion_guerreiro_status['Precisao']
        self.Magia = minion_guerreiro_status['Magia']
        self.Armadura = minion_guerreiro_status['Armadura']
        self.Escudo_magico = minion_guerreiro_status['Escudo Magico']

        # Definir atributos específicos do Minion Arqueiro
        self.type = 3
        self.Meelee = False
        self.Distance = True
        self.pos = minion_pos




