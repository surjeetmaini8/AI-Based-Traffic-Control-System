import pygame
import random

class Vehicle:
    
    def __init__(self, lane, position, speed=2.0):
        
        self.lane = lane
        self.position = list(position)
        self.speed = speed
        self.stopped = False
        self.color = self._get_random_color()
        self.width = 30
        self.height = 20
        
        # Determine turning behavior (70% straight, 15% left, 15% right)
        turn_choice = random.random()
        if turn_choice < 0.70:
            self.turn_direction = 'straight'
        elif turn_choice < 0.85:
            self.turn_direction = 'left'
        else:
            self.turn_direction = 'right'
        
        self.is_turning = False
        self.turn_progress = 0
        
    def _get_random_color(self):
        colors = [
            (255, 0, 0),      # Red
            (0, 0, 255),      # Blue
            (255, 255, 0),    # Yellow
            (255, 165, 0),    # Orange
            (128, 0, 128),    # Purple
            (0, 255, 255),    # Cyan
        ]
        return random.choice(colors)
    
    def update(self, stop_line_position, can_move, vehicle_ahead=None, intersection_center=None):
        
        safe_distance = 35  
        
        # Check if we should start turning at intersection
        if intersection_center and not self.is_turning:
            center_x, center_y = intersection_center
            # Start turning when close to intersection center
            if (abs(self.position[0] - center_x) < 50 and 
                abs(self.position[1] - center_y) < 50 and 
                self.turn_direction != 'straight'):
                self.is_turning = True
        
        # Handle turning logic
        if self.is_turning:
            self._execute_turn(intersection_center)
            return
        
        if self.lane == 'north':
            
            if vehicle_ahead and self.position[1] >= vehicle_ahead.position[1] - safe_distance:
                self.stopped = True
                return
            
            if can_move:
                self.position[1] += self.speed
                self.stopped = False
            elif self.position[1] < stop_line_position - self.height // 2:
                self.position[1] += self.speed
                self.stopped = False
            elif self.position[1] >= stop_line_position:
                self.position[1] += self.speed
                self.stopped = False
            else:
                self.stopped = True
                
        elif self.lane == 'south':
            
            if vehicle_ahead and self.position[1] <= vehicle_ahead.position[1] + safe_distance:
                self.stopped = True
                return
            
            if can_move:
                self.position[1] -= self.speed
                self.stopped = False
            elif self.position[1] > stop_line_position + self.height // 2:
                self.position[1] -= self.speed
                self.stopped = False
            elif self.position[1] <= stop_line_position:
                self.position[1] -= self.speed
                self.stopped = False
            else:
                self.stopped = True
                
        elif self.lane == 'east':
            
            if vehicle_ahead and self.position[0] <= vehicle_ahead.position[0] + safe_distance:
                self.stopped = True
                return
            
            if can_move:
                self.position[0] -= self.speed
                self.stopped = False
            elif self.position[0] > stop_line_position + self.height // 2:
                self.position[0] -= self.speed
                self.stopped = False
            elif self.position[0] <= stop_line_position:
                self.position[0] -= self.speed
                self.stopped = False
            else:
                self.stopped = True
                
        elif self.lane == 'west':
            
            if vehicle_ahead and self.position[0] >= vehicle_ahead.position[0] - safe_distance:
                self.stopped = True
                return
            
            if can_move:
                self.position[0] += self.speed
                self.stopped = False
            elif self.position[0] < stop_line_position - self.height // 2:
                self.position[0] += self.speed
                self.stopped = False
            elif self.position[0] >= stop_line_position:
                self.position[0] += self.speed
                self.stopped = False
            else:
                self.stopped = True
    
    def _execute_turn(self, intersection_center):
        """Execute the turning maneuver"""
        center_x, center_y = intersection_center
        turn_radius = 40
        
        if self.lane == 'north':
            if self.turn_direction == 'left':
                # Turn left: north -> west
                self.position[0] -= self.speed * 0.7
                self.position[1] += self.speed
            else:  # right
                # Turn right: north -> east
                self.position[0] += self.speed * 0.7
                self.position[1] += self.speed
                
        elif self.lane == 'south':
            if self.turn_direction == 'left':
                # Turn left: south -> east
                self.position[0] += self.speed * 0.7
                self.position[1] -= self.speed
            else:  # right
                # Turn right: south -> west
                self.position[0] -= self.speed * 0.7
                self.position[1] -= self.speed
                
        elif self.lane == 'east':
            if self.turn_direction == 'left':
                # Turn left: east -> north
                self.position[0] -= self.speed
                self.position[1] -= self.speed * 0.7
            else:  # right
                # Turn right: east -> south
                self.position[0] -= self.speed
                self.position[1] += self.speed * 0.7
                
        elif self.lane == 'west':
            if self.turn_direction == 'left':
                # Turn left: west -> south
                self.position[0] += self.speed
                self.position[1] += self.speed * 0.7
            else:  # right
                # Turn right: west -> north
                self.position[0] += self.speed
                self.position[1] -= self.speed * 0.7
        
        self.stopped = False
    
    def draw(self, screen):
        """Draw the vehicle on the screen"""
        if self.lane in ['north', 'south']:
            # Vertical lanes - vertical rectangles
            rect = pygame.Rect(self.position[0] - self.width // 2, 
                             self.position[1] - self.height // 2,
                             self.width, self.height)
        else:
            # Horizontal lanes - horizontal rectangles
            rect = pygame.Rect(self.position[0] - self.height // 2,
                             self.position[1] - self.width // 2,
                             self.height, self.width)
        
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Black border
    
    def is_off_screen(self, screen_width, screen_height):
        """Check if vehicle has left the screen"""
        margin = 50
        return (self.position[0] < -margin or 
                self.position[0] > screen_width + margin or
                self.position[1] < -margin or 
                self.position[1] > screen_height + margin)
