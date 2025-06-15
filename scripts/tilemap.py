import json

import pygame

PLAYER_OFFSETS = [(1, 0), (1, 1), (0, 1), (-1, 1), (0, 0), (-1, 0), (-1, -1), (0, -1), (1, -1)]
PHYSICS_TILES = {'mossy_stone', 'stone', 'brick'}

class Tilemap:
    def __init__(self, game, tile_size=32):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def neighbour_tiles(self, pos):
        tiles = []
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in PLAYER_OFFSETS:
            offset_loc = str(tile_pos[0] + offset[0]) + ';' + str(tile_pos[1] + offset[1])
            if offset_loc in self.tilemap:
                tiles.append(self.tilemap[offset_loc])
        return tiles
    
    def physics_tile_rect(self, pos):
        rects = []
        for tile in self.neighbour_tiles(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, "offgrid": self.offgrid_tiles}, f)
        f.close()
    
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def extract_tile(self, tile_type, tile_variant, keep):
        tiles = []
        for tile in self.tilemap:
            if tile['type'] == tile_type and tile['variant'] == tile_variant:
                tiles.append(tile['pos'])
                if not keep:
                    del self.tilemap[str(tile['pos'][0]) + ':' + str(tile['pos'][1])]
        pass

    def render(self, dis, offset):
        for off_tile in self.offgrid_tiles:
            dis.blit(self.game.assets[off_tile['type']][off_tile['variant']], (off_tile['pos'][0] - offset[0], off_tile['pos'][1] - offset[1]))
            
        for x in range(offset[0] // self.tile_size, (offset[0] + dis.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + dis.get_height()) // self.tile_size + 1):
                tile_pos = str(x) + ';' + str(y)
                if tile_pos in self.tilemap:
                    tile = self.tilemap[tile_pos]
                    dis.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))