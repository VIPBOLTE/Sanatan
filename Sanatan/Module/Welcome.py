
class HaremModule:
    def __init__(self):
        self.harem_count = 0
        self.coin_count = 0

    def grab_harem(self):
        self.harem_count += 1
        self.coin_count += 50
        return f"Harem grabbed! You now have {self.harem_count} harem and {self.coin_count} coins."

    def get_coin_count(self):
        return f"You currently have {self.coin_count} coins."

# Example Usage
module = HaremModule()
print(module.grab_harem())
print(module.get_coin_count())
print(module.grab_harem())
print(module.get_coin_count())
