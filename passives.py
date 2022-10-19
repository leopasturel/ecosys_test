# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 10:45:13 2022

@author: lepas
"""

import pygame

# To call: print(sensor.Sensor(self.pnj_to_call, self.direction))


class Sensor():
    """
    Create a sensor around the pnj for it to know its surroundings.
    """
    def __init__(self, pnj_to_call, direction):
        
        self.pnj_to_call = pnj_to_call
        self.direction = direction
        
        
        