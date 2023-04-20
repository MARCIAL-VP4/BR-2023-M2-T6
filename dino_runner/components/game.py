import pygame

from dino_runner.utils.constants import BG, ICON, MENU, MENU_SOUND, RUNNING_SOUND, GRAMA, SCREEN_HEIGHT, GAME_OVER, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

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
        self.best_score = []
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
    
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
                MENU_SOUND.play()
                #por a musica do menu aqui 

        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.score = 0
        self.game_speed = GAME_SPEED
        self.playing = True
        RUNNING_SOUND.play()
        #por a musica de quando começar o jogo aqui
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
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
        self.power_up_manager.update(self)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5
    
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)

            if time_to_show >= 0:
                self.make_text(
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",(500,40),tamanho_da_fonte = 18)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def draw_score(self):
        if self.death_count == 0:
            self.make_text(f"Score: {self.score}",(1000, 50))
        elif self.death_count > 0:
            self.make_text(f"Score: {self.score}",(1000, 50))
            self.make_text(f"Best score: {max(self.best_score)}",(120, 50), cores = (0,255,0))

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
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
                MENU_SOUND.stop()
                self.run()

    def make_text(self,create_text, position, tamanho_da_fonte = 22, cores = (0,0,0)):
        font = pygame.font.Font(FONT_STYLE, tamanho_da_fonte)
        text = font.render(create_text, True, cores)
        text_rect = text.get_rect()
        text_rect.center = (position)
        self.screen.blit(text, text_rect)


    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.make_text("Press any key to start", (half_screen_width, half_screen_height))
            self.screen.blit(MENU, (half_screen_height, half_screen_width - 430))
            self.screen.blit(GRAMA, (half_screen_height - 300, half_screen_width - 350))
            #aqui imagem para decorar o menu
        else:
            RUNNING_SOUND.stop()
            MENU_SOUND.stop()
            self.make_text(f"Press any key to restart.",(half_screen_width, half_screen_height))
            self.make_text(f"Score: {self.score - 1}",(half_screen_width, half_screen_height + 30))
            self.make_text(f"Best score: {max(self.best_score)}",(half_screen_width, half_screen_height + 60), cores = (0,255,0))
            self.make_text(f"Number death: {self.death_count}", (half_screen_width, half_screen_height + 90), cores = (255,0,0))
            self.screen.blit(ICON, (half_screen_height + 200, half_screen_width - 400))
            self.screen.blit(GAME_OVER, (half_screen_height + 60, half_screen_width - 120))
            
        pygame.display.update()
        
        self.handle_events_on_menu()  