import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

FONT_STYLE = "freesansbold.ttf"
GAME_SPEED = 20

class Game:
    def __init__(self): 
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = GAME_SPEED
        self.score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
    
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5

    def draw_score(self):
        self.make_menu(f"Score: {self.score}",(1000, 50))
        #font = pygame.font.Font(FONT_STYLE, 22)
        #text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        #text_rect = text.get_rect()
        #text_rect.center = (1000, 50)
        #self.screen.blit (text, text_rect)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) # '#FFFFFF'
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.score = 0
                self.game_speed = GAME_SPEED
                self.run()

    #def make_text(self, final_text):
        #font = pygame.font.Font(FONT_STYLE, 22)
        #text = font.render(final_text, True, (0, 0, 0))
        #return text

    def make_menu(self, create_text, position):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(create_text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (position)
        self.screen.blit(text, text_rect)


    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.make_menu("Press any key to start", (half_screen_width, half_screen_height))
            #font = pygame.font.Font(FONT_STYLE, 22)
            #text = font.render("Press any key to start", True, (0, 0, 0))
            #text_rect = text.get_rect()
            #text_rect.center = (half_screen_width, half_screen_height)
            #self.screen.blit(text, text_rect)
        else:
            self.make_menu(f"Press any key to restart. Number deth {self.death_count} (Score {self.score}!)",(half_screen_width, half_screen_height))
            #font = pygame.font.Font(FONT_STYLE, 22)
            #text = font.render(f"Press any key to restart. Number deth {self.death_count}. Score {self.score}", True, (0, 0, 0))
            #text_rect = text.get_rect()
            #text_rect.center = (half_screen_width, half_screen_height)
            #self.screen.blit(text, text_rect)
            self.screen.blit(ICON, (half_screen_height + 200, half_screen_width - 400)) # self.screen.blit(ICON, (half_screen_height - 20, half_screen_width - 140))
            #self.game_speed = GAME_SPEED
            ## mostrar mensagem de "Press any key to restart"
            ## mostrar score atingido
            ## mostrar death_count

            ### Resetar score e game_speed quando o jogo for 'restartado'
            ### Criar método para remover a repetição de código para o texto
        pygame.display.update()  # .update()
        
        self.handle_events_on_menu()  