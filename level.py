import pygame

levels_data = {
    #this is just the background data
    0: [(255,0,0),1],
    1:[(255,255,0),5],
    2:[(255,255,255), 10]
}
class Level:
    def __init__(self, level_data,chosen_lvl):
        self.chosen_lvl = chosen_lvl
        self.lvl_data = level_data[self.chosen_lvl]
        self.num_of_enemies = self.lvl_data[1]
        self.background = self.lvl_data[0]
        self.lvl_complete = False
    def is_complete_status(self, enemies_remaining):
        self.enemies_remaining = len(enemies_remaining)
        if self.enemies_remaining == 0:
            self.chosen_lvl += 1    
            self.lvl_complete = True
            
            return True
        return False
    # def is_complete_status(self, enemies_remaining):
    #     if enemies_remaining.length == 0:
            
    def display_lvl(self, display):
        display.fill((self.background))
    def start_next_lvl(self, display):
        display.fill((self.background))
    def next_chosen_level(self):
        self.chosen_lvl += 1
        return self.chosen_lvl