"""Cooldown manager for commands"""

import time
from collections import defaultdict

class CooldownManager:
    def __init__(self):
        # Store last use time: {command_name: {user_id: timestamp}}
        self.cooldowns = defaultdict(dict)
    
    def parse_time(self, time_str):
        """Parse time string like '60s', '5m', '1h' to seconds"""
        time_str = time_str.strip().lower()
        
        if time_str.endswith('s'):
            return int(time_str[:-1])
        elif time_str.endswith('m'):
            return int(time_str[:-1]) * 60
        elif time_str.endswith('h'):
            return int(time_str[:-1]) * 3600
        elif time_str.endswith('d'):
            return int(time_str[:-1]) * 86400
        else:
            # Assume seconds if no unit
            return int(time_str)
    
    def check_cooldown(self, command_name, user_id, cooldown_seconds):
        """
        Check if user is on cooldown for command.
        Returns (on_cooldown: bool, remaining_seconds: float)
        """
        if command_name not in self.cooldowns:
            return False, 0
        
        if user_id not in self.cooldowns[command_name]:
            return False, 0
        
        last_use = self.cooldowns[command_name][user_id]
        elapsed = time.time() - last_use
        
        if elapsed < cooldown_seconds:
            remaining = cooldown_seconds - elapsed
            return True, remaining
        
        return False, 0
    
    def set_cooldown(self, command_name, user_id):
        """Set cooldown for user on command"""
        self.cooldowns[command_name][user_id] = time.time()
    
    def format_time(self, seconds):
        """Format seconds into human-readable string"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s" if secs > 0 else f"{minutes}m"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m" if minutes > 0 else f"{hours}h"
