# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 11:57:44 2022

@author: lepas
"""

import pygame
import numpy as np
import os

import objects

class Pnj(pygame.sprite.Sprite):

    def __init__(self, pnj_to_call, tmx_data):
        
        """
        pnj_to_call: (str)
            Takes the name of the folder where the images are.
            
        tmx_data: (class: pytmx.pytmx.TiledMap)
            The attribute that contains the data from your tmx map.
            It will serve to simulate the move.
            
        """
        
        super().__init__()
        self.pnj_to_call = pnj_to_call
        
        # Load all images of all pnj in order to gain memory use
        self.all_images = load_all_images(self.pnj_to_call, self.SIZE_PNJ, self.COLOR_BACKGROUND)
        
        # Define current image for animation
        self.current_image = 0
        
        # Call image
        self.image = self.get_image("down", 1)
        
        # Create a rectangle around the character
        self.rect = self.image.get_rect()
        
        # Initialise the previous_move variable for the turn method
        self.previous_move = "down"
        
        # Define the list of objects that we want to avoid
        self.collide_list = objects.collision_objects(tmx_data)
        
        
    # Get image
    def get_image(self, direction, number):
        """
        direction: (str) 
            One of "left", "right", "up", "down"
        number: (int)
            Number of the picture to display from 1 to 3.
        """

        self.image = self.all_images[f"{self.pnj_to_call}_{direction}_{number}.png"]
        
        return self.image
    
    
    def turn(self):
        """
        Display the image that the pnj has turned and chose direction for next move.
        """
        # Define the feet position to use for collisions
        self.simulated_position = pygame.Rect(self.rect.x, # + self.rect.width/2, 
                                              self.rect.y,# + self.rect.height/3,
                                              self.rect.width/2,
                                              self.rect.height/3).copy()

        # Create list of possible diections
        directions = ["right", "left", "down", "up", 
                 "none", "none", self.previous_move, self.previous_move]
        
        # Start by drawing the direction it will go for
        self.direction = np.random.choice(directions)
        
        # Save previous move to reinject it in the next draw.
        self.previous_move = self.direction
        
        
        # Reset number of the first image to display during animation
        self.image_anim = 2
        
        
        # Return image
        if self.direction != "none":
            self.image = self.get_image(self.direction, 1)
            
            for n in range(2):
                self.simulated_position = self.simulate_move_pnj(self.direction, self.simulated_position)

                for obj in self.collide_list:
                    # If the simulated position ends in an object recall turn()
                    hit = pygame.Rect.collidelist(self.simulated_position, self.collide_list)
                    if hit != -1:
                        return self.turn()
                    
            
    def move_animation(self):
        """
        Define which image will be displayed depending on the direction and the 
        time of the animation
        """
        if self.direction != "none":
            # Play animation
            if self.image_anim <= 3:
                self.image = self.get_image(self.direction, self.image_anim)
                self.move_pnj(self.direction)
                
            # Finish animation by basic image
            elif self.image_anim == 4:
                self.image = self.get_image(self.direction, 1)
            
            # Increment counter
            self.image_anim += 1
        
        
    # Define all moves 
    def move_pnj(self, direction):
        """
        Function to move the rect
        
        direction: (str)
            Direction to go for. 
            Should be one of the following: left, right, up, down, none.
        """
        # Move pnj on map
        if direction == "right":
            self.rect.x += self.velocity
        if direction == "left":
            self.rect.x -= self.velocity
        if direction == "up":
            self.rect.y -= self.velocity
        if direction == "down":
            self.rect.y += self.velocity
        if direction == "none":
            pass
        
    
    # Define all moves 
    def simulate_move_pnj(self, direction, position):
        """
        Function similar to move_pnj but we are just checking if the move is possible
        
        direction: (str)
            Direction to go for. 
            Should be one of the following: left, right, up, down, none.
        
        position: ()
            The position where the rect is
        """
        
        # Move pnj on map
        if direction == "right":
            position.x += self.velocity
            
        if direction == "left":
            position.x -= self.velocity
            
        if direction == "up":
            position.y -= self.velocity
            
        if direction == "down":
            position.y += self.velocity
        
        return position
        

# =============================================================================
# The part below is called only once to call all images
# =============================================================================

def load_all_images(pnj, size_pnj, color_background):
    """
    Create a dictionnary of the pictures segregated by movement
    pnj: (str)
        The name of the pnj from whom you want the images
    size_pnj: (tuple)
        The size of the pnj in width and height.
        Takes two integers. Example: (25,25) (for a size of 25 px * 25 px)
    color_background: (list)
        Color of the backgound of the image that we want to remove.
        Takes three arguments (for the RGB channels). Eg: [0,0,0] (for black)
    """
    
    # Define path to images
    path = f"assets/{pnj}/"
    
    # Retrieve all images of the pnj
    image_names = os.listdir(path)
    images = {}
    
    for img in image_names:
        
        # Create surface object
        image = pygame.Surface([32, 32])
        
        # Load image
        image.blit(pygame.image.load((path + img)), 
                    (0,0))
        
        # Resize image
        image = pygame.transform.scale(image, size_pnj)
        
        # Remove background of picture
        image.set_colorkey(color_background)
        
        # Add a new key and value to the dict of images
        images[img] = image
        
    return images












    # im_left = []
    # im_right = []
    # im_up = []
    # im_down = []
    
    # for image in images:
    #     if "left" in image:
    #         im_left.append(path/image)
    #     elif "right" in image:
    #         im_right.append(path/image)
    #     elif "down" in image:
    #         im_down.append(path/image)
    #     elif "up" in image:
    #         im_up.append(path/image)
            
    # return im_left, im_right, im_down, im_up
    
# import time
# n1 = time.time()
    
# dict_move = {
#     "rabbit_left" : load_all_images("rabbit")[0],
#     "rabbit_right" : load_all_images("rabbit")[1],
#     "rabbit_down" : load_all_images("rabbit")[2],
#     "rabbit_up" : load_all_images("rabbit")[3]
#     }

# n2 = time.time()
# n2-n1
