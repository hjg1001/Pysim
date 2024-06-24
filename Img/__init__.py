from pygame import image as imm
import os
images = {}
for file_name in os.listdir(os.path.dirname(os.path.abspath(__file__))):
    if file_name.endswith('.png'):
        name = os.path.splitext(file_name)[0]
        image=imm.load(os.path.dirname(os.path.abspath(__file__))+'/'+file_name)
        images[name] = image