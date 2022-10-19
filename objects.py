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
    object_dict = {}
    for obj in tmx_data.objects:
        
        # Create a list containing all object rectangles.
        if obj.name != "dirt":
            colliders.append(pygame.Rect(obj.x, obj.y, 
                                         obj.width, obj.height))
        
        # Create a dictionnary containing all objects rectangles and what they are.
        if obj.name not in object_dict.keys():
            object_dict.setdefault(obj.name, [])
        object_dict[obj.name].append(pygame.Rect(obj.x, obj.y, 
                                     obj.width, obj.height))
    
    return colliders, object_dict



def spawn_plants():
    
    pass