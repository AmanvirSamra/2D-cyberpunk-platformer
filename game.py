import pygame
import sys
import random
from scripts.entities import PhysicsEntity, PlayerEntity, EnemyEntity
from scripts.utils import load_image, load_image_folder, load_sprite_sheet, crop_player, Animation
from scripts.tilemap import Tilemap

class Game():
    #Colours
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
            'player/wall_slide' : Animation(crop_player(load_sprite_sheet('entities/player/player_sprite_sheet.png', 32, 32, 4, 6), 11, 7, 10), 5, False),
            'player/dash_attack' : Animation(crop_player(load_sprite_sheet('entities/player/player_sprite_sheet.png', 32, 32, 4, 15)), 3, False),
            'player/death' : Animation(crop_player(load_sprite_sheet('entities/player/player_sprite_sheet.png', 32, 32, 8, 17)), 5, False),
            'enemy/idle' : Animation(crop_player(load_sprite_sheet('entities/enemy/enemy_sprite_sheet.png', 32, 32, 6, 9), 3, width = 20), 5),
            'enemy/walk' : Animation(crop_player(load_sprite_sheet('entities/enemy/enemy_sprite_sheet.png', 32, 32, 6, 10), 3, width = 20), 5),
            'enemy/death' : Animation(crop_player(load_sprite_sheet('entities/enemy/enemy_sprite_sheet.png', 32, 32, 8, 19), 3, width = 20), 5, False),
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
            'projectile' : load_image('particles/projectile.png'),
            'player_spawner' : load_image_folder('tiles/player_spawner'),
            'goal' : load_image_folder('tiles/goal'),
        }
        self.tilemap = Tilemap(self)

        self.screenshake = 0

        #Player Details
        self.player = PlayerEntity(self, (50, 100), (10, 24))
        self.h_movement = [False, False]

        self.level = 1

        self.load_level(self.level)

    def load_level(self, mapID):
        self.tilemap.load('data/maps/' + str(mapID) + '.json')

        self.scroll = [0, 0]

        self.enemies = []

        for spawner in self.tilemap.extract_tile('player_spawner', 0, False):
            self.player.pos = spawner['pos']
            self.player.air_time = 0

        for spawner in self.tilemap.extract_tile('enemy_spawner', 0, False):
            self.enemies.append(EnemyEntity(self, spawner['pos'], (16, 24)))

        for spawner in self.tilemap.extract_tile('enemy_spawner', 1, False):
            self.enemies.append(EnemyEntity(self, spawner['pos'], (16, 24)))

        for goal in self.tilemap.extract_tile('goal', 0, True):
            self.goal_pos = goal['pos']

        self.projectiles = []
        self.dead = 0
        self.transition = -30
        self.goal_reached = False

    def run(self):
        while True:
            #Restart level after death
            if self.dead:
                self.dead += 1
                if self.dead > 60:
                    self.load_level(self.level)

            #Check if player is at finish line and transition to next level
            if self.player.rect().colliderect(pygame.Rect(self.goal_pos[0], self.goal_pos[1], 32, 32)):
                self.goal_reached = True
            
            if self.goal_reached:
                self.transition += 1
                if self.transition > 30:
                    self.level += 1
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1

            #Refresh Screen
            for bg in self.assets['day_bg']:
                self.display.blit(pygame.transform.scale(bg, self.display.get_size()), (0,0))

            self.scroll[0] += int((self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30)
            self.scroll[1] += int((self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30)

            self.tilemap.render(self.display, self.scroll)
            
            if self.screenshake:
                self.screenshake = max(0, self.screenshake - 1)

            for enemy in self.enemies.copy():
                dead = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, self.scroll)
                if dead:
                    self.enemies.remove(enemy)
            
            if not self.dead:
                self.player.update(self.tilemap, (self.h_movement[1] - self.h_movement[0], 0))
                self.player.render(self.display, self.scroll)
            else:
                self.player.update(self.tilemap, (self.h_movement[1] - self.h_movement[0], 0), True)
                self.player.render(self.display, self.scroll)

            for projectile in self.projectiles.copy():
                projectile['pos'][0] += projectile['direction']
                projectile['duration'] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile['pos'][0] - img.get_width() / 2 - self.scroll[0], projectile['pos'][1] - img.get_height() / 2 - self.scroll[1]))
                if self.tilemap.check_solid_tile(projectile['pos']):
                    self.projectiles.remove(projectile)
                elif projectile['duration'] > 600:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dash) < 50:
                    if self.player.rect().collidepoint(projectile['pos']):
                        self.screenshake = max(24, self.screenshake)
                        self.projectiles.remove(projectile)
                        self.dead += 1
            if self.transition:
                transition_circle = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_circle, self.white, (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 16)
                transition_circle.set_colorkey(self.white)
                self.display.blit(transition_circle, (0, 0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)

            pygame.display.flip()

            #Key Inputs
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