class Harem:
    def __init__(self):
        self.grabbed_characters = []
        self.coins = 0

    def grab_character(self):
        # Logic to grab a character from somewhere
        self.grabbed_characters.append("New Character")
        self.coins += 50

    def show_harem(self):
        print("Your Harem:")
        for character in self.grabbed_characters:
            print(character)
    
    def show_coins(self):
        print(f"You have {self.coins} coins in your account.")

if __name__ == "__main__":
    my_harem = Harem()

    # Grab a character and earn coins
    my_harem.grab_character()
    my_harem.show_harem()
    my_harem.show_coins()

    # Grab another character and earn coins
    my_harem.grab_character()
    my_harem.show_harem()
    my_harem.show_coins()
