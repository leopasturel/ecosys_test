# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 11:57:44 2022

@author: lepas
"""

import pygame
import random
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
        self.collide_list, self.object_dict = objects.collision_objects(tmx_data)
        
        
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
                                              self.rect.height/2).copy()
        
        # Pnj checks its surroundings
        proba, target_direction = self.check_vitals()
        
        # Create list of possible directions
        directions = ["right", "left", "down", "up", 
                 "none", self.previous_move, target_direction]

        # Start by drawing the direction it will go for 
        # (random.choices returns a list so we draw 2 items and keep only the first one to have a str)
        self.direction = random.choices(directions, weights = proba, k=2)[0]
        
        # Save previous move to reinject it in the next draw.
        self.previous_move = self.direction
        
        # Reset number of the first image to display during animation
        self.image_anim = 2
        
        if self.thirst <= 10:
            pass
        # Return image
        print(self.direction)
        if self.direction != "none":
            self.image = self.get_image(self.direction, 1)
            
            # Try and see if the move is possible. Otherwise, pick another one.
            for n in range(2):
                self.simulated_position = self.simulate_move_pnj(self.direction, self.simulated_position)

                # Check if there is a collision between simulated position of pnj and an object
                hit = pygame.Rect.collidelist(self.simulated_position, self.collide_list)
                if hit != -1:

                    # Change previous_move to have less probability to pick the same move
                    direc_change = directions[:4]
                    new_previous_move = self.previous_move
                    while new_previous_move == self.previous_move:
                        new_previous_move = random.choices(direc_change, k=2)[0]
                    self.previous_move = new_previous_move
                    return self.turn()
                
            # Update vitals
            self.thirst = self.update_vitals(self.thirst, 0.5)
    
    
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
        # Update vitals
        self.thirst = self.update_vitals(self.thirst, 1)
        
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
        

    def check_vitals(self):
        """
        Check vitals of pnj.
        """
        
        # Update sensor of pnj
        self.sensor_pnj()
        
        # if self.thirst <= self.hunger:
        proba, target_direction = self.define_proba_direction(self.thirst, "water") #, thirst_emergency)
            
        # else:
        #     proba, target_direction = self.define_proba_direction(self.food, hunger_emergency)
            
        return proba, target_direction
    
    
    def sensor_pnj(self):
        """
        Create a sensor centered around the pnj for it to know its surroundings.
        """
        self.sensor_full = []
        
        self.sensor_full.append(pygame.Rect(self.rect.x + self.sensor_width/2, 
                                            self.rect.y + self.sensor_length/2,
                                            self.sensor_width/2, self.sensor_length))
        
        self.sensor_full.append(pygame.Rect(self.rect.x + self.sensor_width/2, 
                                       self.rect.y + self.sensor_length/2,
                                       self.sensor_width, self.sensor_length/2))
                           
        self.sensor_full.append(pygame.Rect(self.rect.x + self.sensor_width/2, 
                                       self.rect.y + self.sensor_length/2,
                                       self.sensor_width/1.25, self.sensor_length/1.5))
        
        self.sensor_full.append(pygame.Rect(self.rect.x + self.sensor_width/2, 
                                       self.rect.y + self.sensor_length/2,
                                       self.sensor_width/1.5, self.sensor_length/1.25))

                
    def define_proba_direction(self, vital, target_type): #, emergency):
        """
        Define which behaviour to adopt depending on vitals.
        Check the best route to get closer to the target.
        If the target is close enough, don't move and eat/drink it'
        target_type: (str)
            Type of the target that you want to join (Eg: "water")
        emergency: (str)
            The level of emergency to get to the target.
            Should be one of the following: "good", "okay", "bad", "critical"
        """
        # Initialize target_direction in case pnj's drinking or has no water in sight.
        target_direction = "none"
        
        if vital <= 90 and pygame.Rect.collidelist(self.rect, self.object_dict[target_type]) != -1:
            proba = [0, 0, 0, 0, 1, 0, 0]
            self.thirst += 10
            
        else:
            
            # Check if there is a target around by checking collision with each sub-sensor
            for sensor in self.sensor_full:
                target_nb = pygame.Rect.collidelist(sensor, self.object_dict[target_type])

                # Stop scanning as soon as a target is found
                if target_nb != -1:
                    break
                    
            if target_nb != -1:
                # Compute distance from pnj to target.
                distance_x = self.rect.x - self.object_dict[target_type][target_nb].x
                distance_y = self.rect.y - self.object_dict[target_type][target_nb].y
                
                # Define direction to go for depending on the distance to the target.
                if abs(distance_x) > abs(distance_y):
                    if distance_x <= 0:
                        target_direction = "right"
                    else:
                        target_direction = "left"
                else:
                    if distance_y <= 0:
                        target_direction = "down"
                    else:
                        target_direction = "up"
                
                # Define probability of any direction to be drawn
                p_vital = 100 - vital
                
                proba = [vital/6, vital/6, vital/6,
                         vital/6, vital/6, vital/6, p_vital]
                
            else:
                # If there is no water in sight, target_direction cannot be drawn.
                if vital < 50:
                    # If vital is low, there's no chance that pnj chills, it needs to find water
                    proba = [1/4, 1/4, 1/4, 1/4, 0, 1/2, 0]
                else:
                    proba = [1/8, 1/8, 1/8, 1/8, 1/4, 1/4, 0]
        return proba, target_direction
        
        
    def update_vitals(self, vital, n):
        vital -= n
        print(vital)
        if vital <= 0:
            print("dead")
            print(self.alive())
            self.remove()
            self.kill()
        return vital
        
        

        
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
