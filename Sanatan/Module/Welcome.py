
class HaremModule:
    def __init__(self):
        self.grabbed_harem = 0
        self.total_coins = 0

    def grab_harem(self):
        self.grabbed_harem += 1
        self.total_coins += 50
        return f"Harem grabbed! Total coins: {self.total_coins}"

    def get_coins(self):
        return f"Total coins: {self.total_coins}"

# Example usage
harem_module = HaremModule()
print(harem_module.grab_harem())
print(harem_module.get_coins())
