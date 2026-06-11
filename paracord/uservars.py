"""User Variable Storage System"""

import json
import os
from pathlib import Path

class UserVarManager:
    def __init__(self, storage_file="uservars.json"):
        """Initialize user variable manager with JSON storage"""
        self.storage_file = storage_file
        self.data = {}
        self.load()
    
    def load(self):
        """Load user variables from JSON file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load user variables: {e}")
                self.data = {}
        else:
            self.data = {}
    
    def save(self):
        """Save user variables to JSON file"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Failed to save user variables: {e}")
    
    def set_var(self, user_id, var_name, value):
        """
        Set user variable with support for:
        - Direct value: "100"
        - Negative value: "-50"
        - Addition: "+50"
        - Subtraction: "-50"
        - Multiplication: "*2"
        - Division: "/2"
        - String values: "username"
        """
        user_id = str(user_id)
        
        # Initialize user data if not exists
        if user_id not in self.data:
            self.data[user_id] = {}
        
        # Get current value (default to 0 for numbers, "" for strings)
        current = self.data[user_id].get(var_name, 0)
        
        # Convert value to string for processing
        value_str = str(value).strip()
        
        # Try to process as number operation
        try:
            # Check if it's a math operation
            if value_str.startswith(('+', '*', '/')):
                # Get operation and operand
                op = value_str[0]
                operand = float(value_str[1:])
                
                # Convert current to number
                if isinstance(current, str):
                    try:
                        current = float(current)
                    except ValueError:
                        current = 0
                else:
                    current = float(current)
                
                # Perform operation
                if op == '+':
                    result = current + operand
                elif op == '*':
                    result = current * operand
                elif op == '/':
                    if operand != 0:
                        result = current / operand
                    else:
                        result = current
                
                # Store as int if no decimal, else as float
                if result == int(result):
                    self.data[user_id][var_name] = int(result)
                else:
                    self.data[user_id][var_name] = result
            
            elif value_str.startswith('-') and len(value_str) > 1:
                # Check if it's subtraction or negative number
                try:
                    operand = float(value_str[1:])
                    
                    # If current value exists and is a number, treat as subtraction
                    if var_name in self.data[user_id]:
                        if isinstance(current, str):
                            try:
                                current = float(current)
                            except ValueError:
                                current = 0
                        else:
                            current = float(current)
                        
                        result = current - operand
                        
                        # Store as int if no decimal
                        if result == int(result):
                            self.data[user_id][var_name] = int(result)
                        else:
                            self.data[user_id][var_name] = result
                    else:
                        # New variable, treat as negative number
                        num = -operand
                        if num == int(num):
                            self.data[user_id][var_name] = int(num)
                        else:
                            self.data[user_id][var_name] = num
                except ValueError:
                    # Not a number, store as string
                    self.data[user_id][var_name] = value_str
            
            else:
                # Try to parse as number
                try:
                    num = float(value_str)
                    # Store as int if no decimal
                    if num == int(num):
                        self.data[user_id][var_name] = int(num)
                    else:
                        self.data[user_id][var_name] = num
                except ValueError:
                    # Not a number, store as string
                    self.data[user_id][var_name] = value_str
        
        except Exception:
            # Fallback: store as string
            self.data[user_id][var_name] = value_str
        
        # Auto-save after each set
        self.save()
    
    def get_var(self, user_id, var_name, default="0"):
        """Get user variable, return default if not exists"""
        user_id = str(user_id)
        
        if user_id not in self.data:
            return default
        
        return str(self.data[user_id].get(var_name, default))
    
    def delete_var(self, user_id, var_name):
        """Delete a user variable"""
        user_id = str(user_id)
        
        if user_id in self.data and var_name in self.data[user_id]:
            del self.data[user_id][var_name]
            self.save()
            return True
        return False
    
    def get_all_vars(self, user_id):
        """Get all variables for a user"""
        user_id = str(user_id)
        return self.data.get(user_id, {})
    
    def clear_user(self, user_id):
        """Clear all variables for a user"""
        user_id = str(user_id)
        if user_id in self.data:
            del self.data[user_id]
            self.save()
            return True
        return False
