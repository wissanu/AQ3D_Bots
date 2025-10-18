import time
import random
import cv2
import numpy as np
from PIL import ImageGrab
from pynput.mouse import Button 
from pynput.mouse import Controller as mc
from pynput.keyboard import Key
from pynput.keyboard import Controller as kc

class AQ3DBot:
    def __init__(self):
        self.mouse = mc()
        self.keyboard = kc()
        self.game_region = None  # (left, top, right, bottom)
        self.setup_game_region()
        
    def setup_game_region(self):
        """Set the game window coordinates using getWindowSize script to manually custom."""
        self.game_region = (0, 0, 1920, 1080)  # Example coordinates
        
    def screenshot(self):
        """Capture game screen"""
        return np.array(ImageGrab.grab(bbox=self.game_region))
    
    def find_template(self, template_path, threshold=0.8):
        """Find image template on screen"""
        screenshot = self.screenshot()
        template = cv2.imread(template_path)
        
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            # Convert to absolute screen coordinates
            x = max_loc[0] + self.game_region[0] + template.shape[1] // 2
            y = max_loc[1] + self.game_region[1] + template.shape[0] // 2
            return (x, y)
        return None
    
    def human_click(self, x, y, button='left'):
        """Human-like click with randomness"""
        # Add small random offset
        target_x = x + random.randint(-2, 2)
        target_y = y + random.randint(-2, 2)
        
        # Move to position
        self.mouse.position = (target_x, target_y)
        time.sleep(random.uniform(0.1, 0.3))
        
        # Click
        if button == 'left':
            self.mouse.click(Button.left)
        else:
            self.mouse.click(Button.right)
            
        # Small random movement after click
        time.sleep(random.uniform(0.1, 0.2))
        self.mouse.move(
            random.randint(-3, 3), 
            random.randint(-3, 3)
        )
    
    def farm_attack_loop(self):
        """Main farming loop"""
        print("Starting farming bot...")
        
        while True:
            try:
                # Look for enemy to attack
                enemy_pos = self.find_template('enemy_template.png')
                if enemy_pos:
                    print(f"Found enemy at {enemy_pos}")
                    self.human_click(enemy_pos[0], enemy_pos[1])
                    time.sleep(random.uniform(1.5, 2.5))
                
                # Use attack skills (F1, F2, etc.)
                self.press_random_skill()
                
                # Look for loot
                loot_pos = self.find_template('loot_template.png')
                if loot_pos:
                    print(f"Found loot at {loot_pos}")
                    self.human_click(loot_pos[0], loot_pos[1])
                    time.sleep(random.uniform(0.5, 1.0))
                
                # Random short break
                if random.random() < 0.02:  # 2% chance
                    time.sleep(random.uniform(2, 5))
                    
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)
    
    def press_random_skill(self):
        """Press random skill key"""
        skills = ['1', '2', '3', '4']
        skill = random.choice(skills)
        self.keyboard.press(skill)
        self.keyboard.release(skill)
        print(f"Using random skill: {skill}")
    
    def press_skill(self, key="1"):
        """Press skill key"""
        skills = ['1', '2', '3', '4']
        skill = key if key in skills else '1'
        self.keyboard.press(skill)
        self.keyboard.release(skill)
        print(f"Using skill: {skill}")

# Usage
if __name__ == "__main__":
    bot = AQ3DBot()
    
    time.sleep(5)
    print("----- start ------")

    # Test click
    bot.human_click(500, 500)
    bot.press_random_skill()
    time.sleep(2)
    bot.press_skill('2')
    
    # Start farming
    # bot.farm_attack_loop()