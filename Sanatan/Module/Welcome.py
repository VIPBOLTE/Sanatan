class Harem:
    def __init__(self):
        self.grabbed_harem = []
        self.coins = 0

    def grab_character(self):
        self.grabbed_harem.append("New Character")
        self.coins += 50

    def show_grabbed_harem(self):
        return self.grabbed_harem

    def show_coins(self):
        return self.coins

if __name__ == "__main__":
    my_harem = Harem()

    # Grab a character and earn coins
    my_harem.grab_character()
    print(f"You have {my_harem.show_coins()} coins.")
    print(f"Your grabbed harem: {my_harem.show_grabbed_harem()}")

    # Grab another character and earn coins
    my_harem.grab_character()
    print(f"You have {my_harem.show_coins()} coins.")
    print(f"Your grabbed harem: {my_harem.show_grabbed_harem()}")
