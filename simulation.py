import pygame
import random
import time
from vehicle import Vehicle
from traffic_signal import TrafficSignal
from traffic_controller import TrafficController

class Simulation:
    
    def __init__(self, width=1200, height=800):
        
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("AI-Based Traffic Management System")
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
        # Colors
        self.bg_color = (34, 139, 34)  # Forest green for grass
        self.road_color = (50, 50, 50)  # Dark gray for roads
        self.line_color = (255, 255, 255)  # White for lane markings
        
        # Intersection setup
        self.center_x = width // 2
        self.center_y = height // 2
        self.road_width = 200
        self.lane_width = self.road_width // 2
        
       
        approach_north = self.center_y - self.road_width // 2
        approach_south = self.center_y + self.road_width // 2
        approach_east = self.center_x + self.road_width // 2
        approach_west = self.center_x - self.road_width // 2
        
        stop_distance = 40  # Distance before traffic light where vehicles should stop
        
        self.stop_lines = {
            'north': approach_north - stop_distance,  # Stop before reaching the light
            'south': approach_south + stop_distance,  # Stop before reaching the light
            'east': approach_east + stop_distance,    # Stop before reaching the light
            'west': approach_west - stop_distance     # Stop before reaching the light
        }
        
        # Lane data structure
        self.lanes = {
            'north': {'vehicles': [], 'stop_line': self.stop_lines['north']},
            'south': {'vehicles': [], 'stop_line': self.stop_lines['south']},
            'east': {'vehicles': [], 'stop_line': self.stop_lines['east']},
            'west': {'vehicles': [], 'stop_line': self.stop_lines['west']}
        }
        
        # Traffic signals (positioned at approach side)
        self.signals = {
            'north': TrafficSignal('north', (self.center_x - 60, approach_north)),
            'south': TrafficSignal('south', (self.center_x + 60, approach_south)),
            'east': TrafficSignal('east', (approach_east, self.center_y - 60)),
            'west': TrafficSignal('west', (approach_west, self.center_y + 60))
        }
        
        # Traffic controller
        self.controller = TrafficController(self.signals, self.lanes)
        
        # Vehicle spawning
        self.spawn_interval = 1.5  # Seconds between spawns
        self.last_spawn_time = time.time()
        self.spawn_probability = 0.7  # Probability of spawning per lane
        
    def spawn_vehicles(self):
        """Spawn new vehicles in random lanes"""
        current_time = time.time()
        
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.last_spawn_time = current_time
            
            # Randomly spawn vehicles in each lane
            for lane_name in self.lanes.keys():
                if random.random() < self.spawn_probability:
                    self._spawn_vehicle(lane_name)
    
    def _spawn_vehicle(self, lane):
        """
        Spawn a vehicle in a specific lane
        
        Args:
            lane: Lane name ('north', 'south', 'east', 'west')
        """
        if lane == 'north':
            # Spawn at top, moving down
            position = [self.center_x - self.lane_width // 2, -30]
        elif lane == 'south':
            # Spawn at bottom, moving up
            position = [self.center_x + self.lane_width // 2, self.height + 30]
        elif lane == 'east':
            # Spawn at right, moving left
            position = [self.width + 30, self.center_y - self.lane_width // 2]
        elif lane == 'west':
            # Spawn at left, moving right
            position = [-30, self.center_y + self.lane_width // 2]
        else:
            return
        
        vehicle = Vehicle(lane, position, speed=random.uniform(1.5, 3))
        self.lanes[lane]['vehicles'].append(vehicle)
    
    def update_vehicles(self):
        """Update all vehicles in all lanes"""
        intersection_center = (self.center_x, self.center_y)
        
        for lane_name, lane_data in self.lanes.items():
            signal = self.signals[lane_name]
            
            # Vehicle can move if: green light AND more than 3 seconds remaining
            # This allows vehicles to stop when yellow is about to appear
            can_move = (signal.state == TrafficSignal.GREEN and signal.time_remaining > 3.0)
            
            stop_line = lane_data['stop_line']
            
            # Sort vehicles by position to check vehicle ahead
            vehicles = lane_data['vehicles']
            
            # Update each vehicle with collision detection
            vehicles_to_remove = []
            for i, vehicle in enumerate(vehicles):
                # Find the vehicle directly ahead (if any)
                vehicle_ahead = None
                if i > 0:
                    vehicle_ahead = vehicles[i - 1]
                
                vehicle.update(stop_line, can_move, vehicle_ahead, intersection_center)
                
                # Mark vehicles that are off screen
                if vehicle.is_off_screen(self.width, self.height):
                    vehicles_to_remove.append(vehicle)
            
            # Remove off-screen vehicles
            for vehicle in vehicles_to_remove:
                lane_data['vehicles'].remove(vehicle)
    
    def draw_roads(self):
        """Draw the intersection and roads"""
        # Background (grass)
        self.screen.fill(self.bg_color)
        
        # Vertical road
        pygame.draw.rect(self.screen, self.road_color,
                        (self.center_x - self.road_width // 2, 0,
                         self.road_width, self.height))
        
        # Horizontal road
        pygame.draw.rect(self.screen, self.road_color,
                        (0, self.center_y - self.road_width // 2,
                         self.width, self.road_width))
        
        # Lane dividers (dashed lines)
        self._draw_dashed_line((self.center_x, 0), (self.center_x, self.height), True)
        self._draw_dashed_line((0, self.center_y), (self.width, self.center_y), False)
        
        # Stop lines
        line_thickness = 4
        stop_line_length = self.road_width - 20
        
        # North stop line
        pygame.draw.line(self.screen, self.line_color,
                        (self.center_x - stop_line_length // 2, self.stop_lines['north']),
                        (self.center_x + stop_line_length // 2, self.stop_lines['north']),
                        line_thickness)
        
        # South stop line
        pygame.draw.line(self.screen, self.line_color,
                        (self.center_x - stop_line_length // 2, self.stop_lines['south']),
                        (self.center_x + stop_line_length // 2, self.stop_lines['south']),
                        line_thickness)
        
        # East stop line
        pygame.draw.line(self.screen, self.line_color,
                        (self.stop_lines['east'], self.center_y - stop_line_length // 2),
                        (self.stop_lines['east'], self.center_y + stop_line_length // 2),
                        line_thickness)
        
        # West stop line
        pygame.draw.line(self.screen, self.line_color,
                        (self.stop_lines['west'], self.center_y - stop_line_length // 2),
                        (self.stop_lines['west'], self.center_y + stop_line_length // 2),
                        line_thickness)
    
    def _draw_dashed_line(self, start, end, vertical):
        """Draw a dashed line"""
        dash_length = 20
        gap_length = 15
        
        if vertical:
            y = start[1]
            while y < end[1]:
                pygame.draw.line(self.screen, self.line_color,
                               (start[0], y), (start[0], min(y + dash_length, end[1])), 2)
                y += dash_length + gap_length
        else:
            x = start[0]
            while x < end[0]:
                pygame.draw.line(self.screen, self.line_color,
                               (x, start[1]), (min(x + dash_length, end[0]), start[1]), 2)
                x += dash_length + gap_length
    
    def draw_vehicles(self):
        """Draw all vehicles"""
        for lane_data in self.lanes.values():
            for vehicle in lane_data['vehicles']:
                vehicle.draw(self.screen)
    
    def draw_signals(self):
        """Draw all traffic signals"""
        for signal in self.signals.values():
            signal.update()
            signal.draw(self.screen, self.font_small)
    
    def draw_ui(self):
        """Draw user interface elements (statistics)"""
        # Title
        title = self.font_large.render("AI Traffic Management System", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 10))
        
        # Get lane statistics
        stats = self.controller.get_lane_stats()
        
        # Draw statistics panel
        panel_x = 10
        panel_y = 60
        line_height = 25
        
        # Header
        header = self.font_medium.render("Lane Statistics:", True, (255, 255, 255))
        self.screen.blit(header, (panel_x, panel_y))
        panel_y += line_height + 10
        
        # Lane stats
        for lane_name in ['north', 'south', 'east', 'west']:
            if lane_name in stats:
                stat = stats[lane_name]
                
                # Lane name
                lane_text = f"{lane_name.upper()}:"
                color = (0, 255, 0) if stat['signal'] == 'GREEN' else (255, 255, 255)
                text = self.font_small.render(lane_text, True, color)
                self.screen.blit(text, (panel_x, panel_y))
                
                # Vehicle count
                count_text = f"Vehicles: {stat['total']} (Waiting: {stat['waiting']})"
                text = self.font_small.render(count_text, True, (255, 255, 255))
                self.screen.blit(text, (panel_x + 100, panel_y))
                
                # Signal state
                signal_text = f"Signal: {stat['signal']}"
                signal_color = {
                    'RED': (255, 0, 0),
                    'YELLOW': (255, 255, 0),
                    'GREEN': (0, 255, 0)
                }.get(stat['signal'], (255, 255, 255))
                text = self.font_small.render(signal_text, True, signal_color)
                self.screen.blit(text, (panel_x + 350, panel_y))
                
                # Green time assigned
                if stat['green_time'] > 0:
                    time_text = f"Green Time: {stat['green_time']:.1f}s"
                    if stat['signal'] == 'GREEN':
                        time_text += f" (Remaining: {stat['time_remaining']:.1f}s)"
                    text = self.font_small.render(time_text, True, (255, 255, 255))
                    self.screen.blit(text, (panel_x + 500, panel_y))
                
                panel_y += line_height
        
        # Active lane indicator
        panel_y += 20
        if self.controller.active_lane:
            active_text = f"Active Lane: {self.controller.active_lane.upper()}"
            text = self.font_medium.render(active_text, True, (0, 255, 0))
            self.screen.blit(text, (panel_x, panel_y))
        
        # Instructions
        instructions_y = self.height - 30
        instructions = self.font_small.render("Press ESC to exit", True, (255, 255, 255))
        self.screen.blit(instructions, (panel_x, instructions_y))
    
    def run(self):
        """Main simulation loop"""
        # Start the traffic controller
        self.controller.start()
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            # Update simulation
            self.spawn_vehicles()
            self.update_vehicles()
            
            # Draw everything
            self.draw_roads()
            self.draw_vehicles()
            self.draw_signals()
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        # Cleanup
        self.controller.stop()
        pygame.quit()
