
import random

class HaremGame:
    def __init__(self):
        self.coins = 0

    def grab_harem(self):
        harem = random.randint(1, 10)
        if harem == 1:
            self.coins += 50
            print("Congratulations! You grabbed a harem and earned 50 coins.")
        else:
            print("Oops! You missed the harem. Try again.")

    def get_coins(self):
        return self.coins

# Example of how to use the HaremGame module
game = HaremGame()
game.grab_harem()
print("Total coins earned: ", game.get_coins())
