
class Harem:
    def __init__(self):
        self.coins = 0

    def grab(self):
        self.coins += 50
        print("You grabbed 1 harem and earned 50 coins.")

    def coin_count(self):
        return self.coins

harem = Harem()

while True:
    command = input("Enter a command (grab/coin/exit): ")
    
    if command == 'grab':
        harem.grab()
    elif command == 'coin':
        print(f"You have {harem.coin_count()} coins.")
    elif command == 'exit':
        print("Exiting the program.")
        break
    else:
        print("Invalid command. Please try again.")
