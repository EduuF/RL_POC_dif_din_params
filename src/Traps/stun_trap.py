from Traps.base_trap import Base_trap

class Stun_trap(Base_trap):
    def __init__(self, id, pos):
        super().__init__()

        self.id = id
        self.type = 6
        self.pos = pos