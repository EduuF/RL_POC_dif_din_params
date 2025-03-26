class Base_minion():
    def __init__(self):
        self.id = None
        self.Life = None
        self.Velocidade = None
        self.Forca = None
        self.Precisao = None
        self.Magia = None
        self.Armadura = None
        self.Escudo_magico = None
        self.Tipo = None
        self.Meelee = None
        self.Distance = None
        self.minion_pos = None
        self.type = None
        self.pos = None

    def get_minion_status(self):
        minion_status = {
            "Velocidade": self.Velocidade,
            "Forca": self.Forca,
            "Precisao": self.Precisao,
            "Magia": self.Magia,
            "Armadura": self.Armadura,
            "Escudo Magico": self.Escudo_magico,
            "Tipo": self.Tipo,
            "Meelee": self.Meelee,
            "Distance": self.Distance,
            "Pos": self.pos

        }
        return minion_status

    def take_damage(self, damage):
        self.Life -= damage



