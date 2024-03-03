
class CoinModule:
    def __init__(self):
        self.coins = 0
        self.hareems = 0

    def grab_hareem(self):
        self.hareems += 1
        self.coins += 50
        return f"Grabbed a hareem! You now have {self.hareems} hareems and {self.coins} coins."

    def check_coins(self):
        return f"You currently have {self.coins} coins."

# Example usage:
coin_module = CoinModule()
print(coin_module.grab_hareem())
print(coin_module.check_coins())
