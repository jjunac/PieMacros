from pathlib import Path
import pyautogui
import yaml

SCREEN_W, SCREEN_H = pyautogui.size()
MOUSE_POS = pyautogui.position()

SIZE        = int(SCREEN_W*.25)
CENTER      = int(SIZE/2)
BORDER      = 2
RADIUS      = int(CENTER - BORDER)
BACK_RADIUS = int(RADIUS*.3)

MATERIAL_COLORS = yaml.safe_load(Path("material_colors.yaml").read_text())
SELECTOR_COLORS = ["red", "pink", "purple", "deepPurple", "indigo", "blue", "lightBlue", "cyan", "teal", "green", 
                   "lightGreen", "lime", "yellow", "amber", "orange", "deepOrange"]