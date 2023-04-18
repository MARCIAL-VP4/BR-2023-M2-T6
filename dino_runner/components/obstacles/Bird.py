import random

from dino_runner.components.obstacles.obstacle import Obstacle

class Bird(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        bird_position = random.randint(200,280)
        self.rect.y = bird_position
        self.index = 0
    
    def draw(self, screen):
       if self.index >= 9:
          self.index = 0
       screen.blit(self.image[self.index//5],self.rect) 
       self.index += 1