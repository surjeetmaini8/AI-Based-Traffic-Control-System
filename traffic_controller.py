import threading
import time

class TrafficController:
    
    def __init__(self, signals, lanes):
        
        self.signals = signals
        self.lanes = lanes
        self.active_lane = None
        self.running = False
        self.lock = threading.Lock()
        self.controller_thread = None
        
        self.min_green_time = 15  
        self.max_green_time = 45  
        self.yellow_time = 2      
        
    def start(self):
        """Start the traffic controller in a separate thread"""
        self.running = True
        self.controller_thread = threading.Thread(target=self._control_loop, daemon=True)
        self.controller_thread.start()
    
    def stop(self):
        """Stop the traffic controller"""
        self.running = False
        if self.controller_thread:
            self.controller_thread.join(timeout=2)
    
    def _control_loop(self):
        """Main control loop running in separate thread"""
        # Cycle through opposite lane pairs: North-South, then East-West
        lane_pairs = [
            ('north', 'south'),
            ('east', 'west')
        ]
        
        while self.running:
            for lane_pair in lane_pairs:
                if not self.running:
                    break
                    
                lane_priorities = self._calculate_priorities()
                
                # Calculate combined priority for the lane pair
                pair_priority = sum(lane_priorities.get(lane, 0) for lane in lane_pair)
                
                if pair_priority > 0:
                    # Calculate green duration based on combined vehicle count
                    green_duration = self._calculate_green_duration(pair_priority)
                    
                    # Activate both lanes in the pair
                    self._activate_lane_pair(lane_pair, green_duration)
                    
                    # Wait for the green light duration
                    time.sleep(green_duration)
                    
                    # Yellow light transition for both lanes
                    with self.lock:
                        for lane in lane_pair:
                            if lane in self.signals:
                                self.signals[lane].set_state('YELLOW', self.yellow_time)
                    
                    time.sleep(self.yellow_time)
                else:
                    # No vehicles in this pair, short wait
                    time.sleep(0.5)
    
    def _calculate_priorities(self):
        
        priorities = {}
        
        with self.lock:
            for lane_name, lane_data in self.lanes.items():
                # Count only stopped vehicles (waiting at red light)
                waiting_count = sum(1 for vehicle in lane_data['vehicles'] 
                                   if hasattr(vehicle, 'stopped') and vehicle.stopped)
                
                if waiting_count > 0:
                    priorities[lane_name] = waiting_count
        
        return priorities
    
    def _calculate_green_duration(self, vehicle_count):
        
        if vehicle_count < 10:
            # Low traffic: scale between min and 25 seconds
            max_time = 15
            ratio = vehicle_count / 10.0
        elif vehicle_count < 30:
            # Medium traffic: scale between 25 and 40 seconds
            max_time = 30
            ratio = (vehicle_count - 10) / 20.0
        else:
            # High traffic: scale between 40 and max seconds
            max_time = self.max_green_time
            ratio = min(1.0, (vehicle_count - 30) / 30.0)
        
        duration = self.min_green_time + (max_time - self.min_green_time) * ratio
        return round(duration, 1)
    
    def _activate_lane(self, lane_name, duration):
        
        with self.lock:
            # Set all lanes to RED first (mutual exclusion)
            for name, signal in self.signals.items():
                if name != lane_name:
                    signal.set_state('RED', 0)
            
            # Set selected lane to GREEN
            if lane_name in self.signals:
                self.signals[lane_name].set_state('GREEN', duration)
                self.active_lane = lane_name
    
    def _activate_lane_pair(self, lane_pair, duration):
        """Activate a pair of opposite lanes (both green) and set others to red"""
        with self.lock:
            # Set all lanes to RED first
            for name, signal in self.signals.items():
                signal.set_state('RED', 0)
            
            # Set both lanes in the pair to GREEN
            for lane_name in lane_pair:
                if lane_name in self.signals:
                    self.signals[lane_name].set_state('GREEN', duration)
            
            # Set active lane to the pair (for display)
            self.active_lane = f"{lane_pair[0]}-{lane_pair[1]}"
    
    def get_lane_stats(self):
        
        stats = {}
        
        with self.lock:
            for lane_name, lane_data in self.lanes.items():
                total_vehicles = len(lane_data['vehicles'])
                waiting_vehicles = sum(1 for v in lane_data['vehicles'] 
                                      if hasattr(v, 'stopped') and v.stopped)
                
                signal_state = self.signals[lane_name].state if lane_name in self.signals else 'UNKNOWN'
                green_time = self.signals[lane_name].green_duration if lane_name in self.signals else 0
                
                stats[lane_name] = {
                    'total': total_vehicles,
                    'waiting': waiting_vehicles,
                    'signal': signal_state,
                    'green_time': green_time,
                    'time_remaining': self.signals[lane_name].time_remaining if lane_name in self.signals else 0
                }
        
        return stats
