import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_image_folder(path):
    images = []
    
    for file in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + file))
    return images

def load_sprite_sheet(path, width, height, frame_num, row=0):
    images = []
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    total_width = 0

    for i in range(frame_num):
        images.append(img.subsurface(pygame.Rect((total_width, height * row), (width, height))))
        total_width += width
        
    return images

def crop_player(image_list, x=8, y=7, width=16, height=25):
    images = image_list
    new_images = []

    for image in images:
        new_images.append(image.subsurface(pygame.Rect(x, y, width, height)))
    return new_images

class Animation:
    def __init__(self, images, img_dur, loop=True):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.img_dur)
        else:
            self.frame = min(self.frame + 1, len(self.images) * self.img_dur - 1)
            if self.frame >= len(self.images) * self.img_dur - 1:
                self.done = True

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)
    
    def img(self):
        return self.images[int(self.frame / self.img_dur)]
