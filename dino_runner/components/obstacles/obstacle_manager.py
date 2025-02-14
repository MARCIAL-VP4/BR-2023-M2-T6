import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus, Large_cactus
from dino_runner.components.obstacles.Bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):

        if len(self.obstacles) == 0:
            choice = random.randint(0,2)
                
            if choice == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif choice == 1:
                self.obstacles.append(Large_cactus(LARGE_CACTUS))
            elif choice == 2:
                self.obstacles.append(Bird(BIRD))
            
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:    
                    pygame.time.delay(500)
                    game.playing = False
                    #por a musica de quando morrer aqui
                    game.best_score.append(game.score) 	                    
                    game.death_count += 1	                    
                    break
                
                elif game.player.hammer:
                    self.obstacles.remove(obstacle)

                elif game.player.clock:
                    game.game_speed = 20
                
                elif game.player.shield:
                    pass

    def reset_obstacles(self):
        self.obstacles = []

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)   