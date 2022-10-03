# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 16:26:26 2022

@author: lepas
"""

import pygame
import pytmx
import pyscroll
# import numpy as np

# USE pygame.time.set_timer to spawn stuffs


from rabbit import Rabbit

class Game():
    
    def __init__(self):
        # Create window and name it
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption("Ecosys-test")

        # Load map
        self.tmx_data = pytmx.util_pygame.load_pygame("ecosys_map.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1
        
        # Draw map
        self.group = pyscroll.PyscrollGroup(map_layer, default_layer=1)
        
        # # Spawn a rabbit where it has been decided in spawn
        self.rabbit = Rabbit(self.tmx_data) 
        self.rabbit2 = Rabbit(self.tmx_data)
        
        # Add rabbits on the map
        self.all_rabbits = pygame.sprite.Group()
        self.all_rabbits.add(self.rabbit)
        self.all_rabbits.add(self.rabbit2)
        
        
        
        # Define USEREVENTS such as move, spawn times, ...
        self.move_pnj = pygame.USEREVENT+1
        pygame.time.set_timer(self.move_pnj, 50) #self.rabbit.elapsed_time_before_next_move())
        
        
    def update(self):
        self.group.update()
        self.all_rabbits.update()
    
    def run(self):
        
        clock = pygame.time.Clock()
        running = True
        counter_move = 1
        
        while running:
            
            # Game is at 60 fps
            clock.tick(60) 
            
            # Update groups
            self.update()
            
            # Add map to screen
            self.group.draw(self.screen)

            # add character to screen
            self.all_rabbits.draw(self.screen)
            
            # x,y = pygame.mouse.get_pos()
            # print(x,y)
            
            # Refresh screen
            pygame.display.flip() 
            
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == self.move_pnj:
                    # Move rabbit
                    for rabbit in self.all_rabbits:
                        # Display image that the rabbit turns
                        if counter_move == 1:
                            rabbit.turn()
                        # Display animation of movement
                        elif counter_move <= 4:
                            rabbit.move_animation()
                        # Reset counter if move is completed
                        else:
                            counter_move = 0
                        
                    counter_move += 1

                
        pygame.quit()