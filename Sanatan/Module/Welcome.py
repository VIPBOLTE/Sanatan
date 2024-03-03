
class CoinBank:
    def __init__(self):
        self.coins = 0

    def add_coin(self, amount):
        self.coins += amount

    def get_coins(self):
        return self.coins

def main():
    bank = CoinBank()
    while True:
        command = input("Enter command: ")
        if command == "/coin":
            print(f"You have {bank.get_coins()} coins.")
        elif command == "/grab":
            bank.add_coin(50)
            print("You grabbed 50 coins!")
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
