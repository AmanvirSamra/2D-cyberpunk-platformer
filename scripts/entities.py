import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"Left": False, "Right": False, "Up": False, "Down": False}
        self.action = ''
        self.animation_offset = (-3, -3)
        self.flip = True
        self.set_action('idle')
        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animaton = self.game.assets[self.type + '/' + self.action].copy()
    
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {"Left": False, "Right": False, "Top": False, "Bottom": False}

        self.frame_movement = (movement[0]*2 + self.velocity[0], movement[1]*2 + self.velocity[1])

        self.pos[0] += self.frame_movement[0]
        entity_rect = self.rect()
        for tile_rect in tilemap.physics_tile_rect(self.pos):
            if entity_rect.colliderect(tile_rect):
                if self.frame_movement[0] > 0:
                    self.collisions["Right"] = True
                    entity_rect.right = tile_rect.left
                if self.frame_movement[0] < 0:
                    self.collisions["Left"] = True
                    entity_rect.left = tile_rect.right
                self.pos[0] = entity_rect.x

        self.pos[1] += self.frame_movement[1]
        entity_rect = self.rect()
        for tile_rect in tilemap.physics_tile_rect(self.pos):
            if entity_rect.colliderect(tile_rect):
                if self.frame_movement[1] > 0:
                    self.collisions["Bottom"] = True
                    entity_rect.bottom = tile_rect.top
                if self.frame_movement[1] < 0:
                    self.collisions["Top"] = True
                    entity_rect.top = tile_rect.bottom
                self.pos[1] = entity_rect.y
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['Bottom'] or self.collisions['Top']:
            self.velocity[1] = 0

        if movement[0] > 0:
            self.flip = True
        if movement[0] < 0:
            self.flip = False

        self.last_movement = movement

        self.animaton.update()
            

    def render(self, dis, offset):
        # pygame.draw.rect(dis, (255, 0, 0), pygame.Rect(self.pos[0] - offset[0], self.pos[1] - offset[1], self.size[0], self.size[1]), 1)
        dis.blit(pygame.transform.flip(self.animaton.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class PlayerEntity(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 2
        self.second_jump = False
        self.wall_slide = False
        self.dash = False

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        self.air_time += 1
        if self.collisions['Bottom']:
            self.air_time = 0
            self.jumps = 2
            self.second_jump = False

        self.wall_slide = False
        if(self.collisions['Right'] or self.collisions['Left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)

            if self.collisions['Right']:
                self.flip = True
            else:
                self.flip = False

            self.set_action('wall_slide')

        if self.velocity[0] > 0:
            self.velocity[0] = max(0, self.velocity[0] - 0.1)
        else:
            self.velocity[0] = min(0, self.velocity[0] + 0.1)
        
        if not self.wall_slide:
            if abs(self.dash) > 40:
                self.set_action('dash_attack')
            elif self.second_jump:
                self.set_action('double_jump')
            elif self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        
        if self.dash > 0:
            self.dash = max(0, self.dash - 1)
        elif self.dash < 0:
            self.dash = min(0, self.dash + 1)

        if abs(self.dash) > 50:
            self.velocity[0] = abs(self.dash) / self.dash * 8
            if abs(self.dash) == 51:
                self.velocity[0] *= 0.1

    def jump(self):
        if self.wall_slide:
            if self.flip and self.frame_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
            elif not self.flip and self.frame_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)

        elif self.jumps == 2:
            if(self.air_time > 4):
                self.jumps -= 1
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
        elif self.jumps == 1:
            self.velocity[1] = -3
            self.jumps -= 1
            self.second_jump = True
    
    def dash_attack(self):
        if not self.dash:
            if self.flip:
                self.dash = 60
            else:
                self.dash = -60