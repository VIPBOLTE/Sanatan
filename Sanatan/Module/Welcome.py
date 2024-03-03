
class CoinModule:
    def __init__(self):
        self.coins = 0
        self.harem = 0

    def grab_hareem(self):
        self.harem += 1
        self.coins += 50
        return f"Grabbed a harem! You now have {self.harem} harem and {self.coins} coins."

    def check_coins(self):
        return f"You currently have {self.coins} coins."

# Example usage:
coin_module = CoinModule()
print(coin_module.grab_harem())
print(coin_module.check_coins())
