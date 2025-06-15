import pygame
import sys
from scripts.entities import PhysicsEntity, PlayerEntity
from scripts.utils import load_image, load_image_folder, load_sprite_sheet, crop_player, Animation
from scripts.tilemap import Tilemap

class Game():
    black = 0, 0, 0
    white = 255, 255, 255

    def __init__(self):
        pygame.init()
        
        #Game Setup
        self.screen = pygame.display.set_mode((1280, 720))
        self.display = pygame.Surface((640, 360))
        pygame.display.set_caption("Platformer")
        self.clock = pygame.time.Clock()
        self.assets = {
            'player/idle' : Animation(crop_player(load_sprite_sheet('entities/player/player_sprite_sheet.png', 32, 32, 12, 1)), 5),
            'player/run' : Animation(crop_player(load_sprite_sheet('entities/player/player_sprite_sheet.png', 32, 32, 8, 3)), 4),
            'player/jump' : Animation(crop_player(load_sprite_sheet('entities/player/player_sprite_sheet.png', 32, 32, 5, 4)), 10, False),
            'player/double_jump' : Animation(crop_player(load_sprite_sheet('entities/player/player_sprite_sheet.png', 32, 32, 6, 5)), 6, False),
            'player/wall_slide' : Animation(crop_player(load_sprite_sheet('entities/player/player_sprite_sheet.png', 32, 32, 4, 6), 10, 7, 12), 5, False),
            'player/dash_attack' : Animation(crop_player(load_sprite_sheet('entities/player/player_sprite_sheet.png', 32, 32, 4, 15)), 3, False),
            'mossy_stone' : load_image_folder('tiles/mossy_stone'),
            'stone' : load_image_folder('tiles/stone'),
            'brick' : load_image_folder('tiles/bricks'),
            'weeds' : load_image_folder('tiles/weeds'),
            'boxes' : load_image_folder('tiles/boxes'),
            'brick_decor' : load_image_folder('tiles/brick_decor'),
            'powerlines' : load_image_folder('tiles/powerlines'),
            'rocks' : load_image_folder('tiles/rocks'),
            'trees' : load_image_folder('tiles/trees'),
            'bushes' : load_image_folder('tiles/bushes'),
            'enemy_spawner' : load_image_folder('tiles/enemy_spawner'),
            'day_bg' : load_image_folder('background/day'),
            'industrial_day_bg' : load_image_folder('background/industrial_day'),
            'industrial_night_bg' : load_image_folder('background/industrial_night'),
        }
        self.tilemap = Tilemap(self)
        self.scroll = [0, 0]

        self.tilemap.load('maps/map.json')

        #Player Details
        self.player = PlayerEntity(self, (50, 100), (12, 24))
        self.h_movement = [False, False]

    def run(self):
        while True:
            #Refresh Screen
            for bg in self.assets['day_bg']:
                self.display.blit(pygame.transform.scale(bg, self.display.get_size()), (0,0))

            self.scroll[0] += int((self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30)
            self.scroll[1] += int((self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30)

            self.tilemap.render(self.display, self.scroll)
            
            self.player.update(self.tilemap, (self.h_movement[1] - self.h_movement[0], 0))
            self.player.render(self.display, self.scroll)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.h_movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.h_movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_x:
                        self.player.dash_attack()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.h_movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.h_movement[1] = False

            #FPS
            self.clock.tick(60)

Game().run()