from configs import minion_mago_status
from Minions.base_minion import Base_minion


class Minion_mago(Base_minion):
    def __init__(self, id, minion_pos):
        super().__init__()

        # Inicializa os atributos específicos do Minion Arqueiro
        self.id = id
        self.Life = minion_mago_status['Life']
        self.Velocidade = minion_mago_status['Velocidade']
        self.Forca = minion_mago_status['Forca']
        self.Precisao = minion_mago_status['Precisao']
        self.Magia = minion_mago_status['Magia']
        self.Armadura = minion_mago_status['Armadura']
        self.Escudo_magico = minion_mago_status['Escudo Magico']

        # Definir atributos específicos do Minion Arqueiro
        self.type = 4
        self.Meelee = False
        self.Distance = True
        self.pos = minion_pos




