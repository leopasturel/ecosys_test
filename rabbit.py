# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 12:04:27 2022

@author: lepas
"""

import pygame
import pnj
import numpy as np

class Rabbit(pnj.Pnj):
    
    # Call here the attributes that are needed in parent __init__
    # Give a size to the image
    SIZE_PNJ = (25,25)
    COLOR_BACKGROUND = [0,0,0]
    
    def __init__(self, tmx_data):
        
        super().__init__("rabbit", tmx_data)
        # pygame.image.load("assets/rabbit-rbg/rabbit-rbg_down_2.png")
        
        # Give a position to the character
        self.rect.x = 250
        self.rect.y = 200
        
        # Give a speed to the character
        self.velocity = 10
        
    # Pbly remove that and play on velocity instead (keep a given value for everything)
    def elapsed_time_before_next_move(self):
        # n = np.random.randint(800,1200)
        return 300 #np.random.randint(800,1200)

       
            
        
        
        
    
        
        
