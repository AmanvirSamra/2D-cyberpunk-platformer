import sys

import pygame
from scripts.utils import load_image, load_image_folder, load_sprite_sheet
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    black = 0, 0, 0
    white = 255, 255, 255

    def __init__(self):
        pygame.init()
        
        #Game Setup
        self.screen = pygame.display.set_mode((1280, 720))
        self.display = pygame.Surface((640, 360))
        pygame.display.set_caption("Editor")
        self.clock = pygame.time.Clock()
        self.assets = {
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
        }
        self.bg = {
            'day_bg' : load_image_folder('background/day'),
            'industrial_day_bg' : load_image_folder('background/industrial_day'),
            'industrial_night_bg' : load_image_folder('background/industrial_night'),
        }

        self.tile_list = list(self.assets)
        self.tile_type = 0
        self.tile_variant = 0

        self.tilemap = Tilemap(self)
        self.scroll = [0, 0]

        self.movement = [False, False, False, False]

        self.click = False
        self.right_click = False
        self.shift = False
        self.offgrid = False

        try:
            self.tilemap.load('maps/map.json')
        except FileNotFoundError:
            pass
    

    def run(self):
        while True:

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
            tile_pos = (int((mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size))

            #Refresh Screen
            for bg in self.bg['day_bg']:
                self.display.blit(pygame.transform.scale(bg, self.display.get_size()), (0,0))

            current_tile = self.assets[self.tile_list[self.tile_type]][self.tile_variant].copy()
            current_tile.set_alpha(100)
            self.display.blit(current_tile, (5, 5))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            self.tilemap.render(self.display, (int(self.scroll[0]), int(self.scroll[1])))

            if not self.offgrid:
                self.display.blit(current_tile, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile, mouse_pos)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.flip()


            if self.click and not self.offgrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_type], 'variant': self.tile_variant, 'pos': (tile_pos)}
            if self.right_click:
                temp = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if temp in self.tilemap.tilemap:
                    del self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_type = self.assets[tile['type']][tile['variant']]
                    tile_rect = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_type.get_width(), tile_type.get_height())
                    if tile_rect.collidepoint(mouse_pos):
                        self.tilemap.offgrid_tiles.remove(tile)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                        if self.offgrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_type], 'variant': self.tile_variant, 'pos': (mouse_pos[0] + self.scroll[0], mouse_pos[1] +  self.scroll[1])})
                    if event.button == 3:
                        self.right_click = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_type]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_type]])
                    else:
                        if event.button == 4:
                            self.tile_type = (self.tile_type - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_type = (self.tile_type + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False
                    if event.button == 3:
                        self.right_click = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_x:
                        self.offgrid = not self.offgrid
                    if event.key == pygame.K_s:
                        self.tilemap.save('maps/map.json')

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            #FPS
            self.clock.tick(60)

Editor().run()