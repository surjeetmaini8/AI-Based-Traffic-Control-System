import pygame
import time

class TrafficSignal:
    
    # Signal states
    RED = 'RED'
    YELLOW = 'YELLOW'
    GREEN = 'GREEN'
    
    def __init__(self, lane, position):
        
        self.lane = lane
        self.position = position
        self.state = self.RED
        self.green_duration = 0  # Dynamically assigned
        self.time_remaining = 0
        self.last_change_time = time.time()
        
    def set_state(self, state, duration=0):
        
        self.state = state
        self.green_duration = duration
        self.time_remaining = duration
        self.last_change_time = time.time()
    
    def update(self):
        elapsed = time.time() - self.last_change_time
        self.time_remaining = max(0, self.green_duration - elapsed)
    
    def draw(self, screen, font):
        
        red_color = (255, 0, 0) if self.state == self.RED else (100, 0, 0)
        yellow_color = (255, 255, 0) if self.state == self.YELLOW else (100, 100, 0)
        green_color = (0, 255, 0) if self.state == self.GREEN else (0, 100, 0)
        
        x, y = self.position
        box_width = 40
        box_height = 100
        
        pygame.draw.rect(screen, (50, 50, 50), 
                        (x - box_width // 2, y - box_height // 2, box_width, box_height))
        
        pygame.draw.circle(screen, red_color, (x, y - 30), 12)
        
        pygame.draw.circle(screen, yellow_color, (x, y), 12)
        
        pygame.draw.circle(screen, green_color, (x, y + 30), 12)
        
        state_text = font.render(self.state, True, (255, 255, 255))
        screen.blit(state_text, (x - state_text.get_width() // 2, y + 55))
        
        if self.state == self.GREEN and self.time_remaining > 0:
            time_text = font.render(f"{int(self.time_remaining)}s", True, (255, 255, 255))
            screen.blit(time_text, (x - time_text.get_width() // 2, y + 75))
