import pygame
import os
images = {}
for file_name in os.listdir(os.path.dirname(os.path.abspath(__file__))):
    if file_name.endswith('.png'):
        name = os.path.splitext(file_name)[0]
        image=pygame.image.load(os.path.dirname(os.path.abspath(__file__))+'/'+file_name)
        images[name] = image