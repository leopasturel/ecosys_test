# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 18:09:50 2022

@author: lepas
"""

import pygame
import pytmx

        
def collision_objects(tmx_data):
    """
    Return a list of the objects that are colliders
    tmx_data: (class: pytmx.pytmx.TiledMap)
        The attribute that contains the data from your tmx map.
    """
    colliders = []
    counter = 0
    for obj in tmx_data.objects:
        if obj.name != "dirt":
            colliders.append(pygame.Rect(obj.x, obj.y, 
                                         obj.width, obj.height))
            counter += 1
    #         print(obj)
    # print(colliders)
    
    return colliders
    

# =============================================================================
# Still draft...
# =============================================================================
    
# def check_collision(self, group):
#     """
#     Check collision and move back if there is one.
#     group: (group of sprite)
#         Group of sprites to check the collision for.
#     """
#     for sprite in group.sprites():
#         if sprite.feet.collidelist(self.colliders):
#            return sprite.move_back()
    
    
# # Créer fenêtre du jeu
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Pygame - first game")

# tmx_data = pytmx.util_pygame.load_pygame("ecosys_map.tmx")
# for obj in tmx_data.objects:
#     if obj.name == "water":
#         obj.type = "collision"
#     print(obj.type)