class DiceResult:
    def __init__(self, success_level, value, boons):
        self.success_level = success_level
        self.value = value
        self.boons = boons

    def to_dict(self):
        return {
            "success_level": self.success_level,
            "value": self.value,
            "boons": self.boons
        } 