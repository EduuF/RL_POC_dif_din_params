from configs import minion_arqueiro_status
from Minions.base_minion import Base_minion


class Minion_arqueiro(Base_minion):
    def __init__(self, id, minion_pos):
        super().__init__()

        # Inicializa os atributos específicos do Minion Arqueiro
        self.id = id
        self.Life = minion_arqueiro_status['Life']
        self.Velocidade = minion_arqueiro_status['Velocidade']
        self.Forca = minion_arqueiro_status['Forca']
        self.Precisao = minion_arqueiro_status['Precisao']
        self.Armadura = minion_arqueiro_status['Armadura']

        # Definir atributos específicos do Minion Arqueiro
        self.type = 2
        self.Meelee = False
        self.Distance = True
        self.pos = minion_pos





