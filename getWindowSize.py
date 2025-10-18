import win32gui
import win32con
import time

def get_window_rect(window_title=""):
    """Get exact window rectangle using Windows API"""
    hwnd = win32gui.FindWindow(None, window_title)
    
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        
        print(f"Window: {window_title}")
        print(f"Left: {left}")
        print(f"Top: {top}")
        print(f"Right: {right}")
        print(f"Bottom: {bottom}")
        print(f"Width: {right - left}")
        print(f"Height: {bottom - top}")
        print(f"Region tuple: ({left}, {top}, {right}, {bottom})")
        
        return rect
    else:
        print(f"Window '{window_title}' not found!")
        return None

# Get AQ3D window coordinates
time.sleep(5)
game_rect = get_window_rect("AQ3D")