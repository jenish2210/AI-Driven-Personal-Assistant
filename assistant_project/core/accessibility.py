import keyboard
from .utils import speak

# def setup_keyboard_shortcuts():
#     """
#     Set up keyboard shortcuts for visually impaired users to trigger TTS.
#     """
#     # Example: Press 'Ctrl+S' to speak a predefined text
#     keyboard.add_hotkey('ctrl+s', lambda: speak("This is a keyboard shortcut test."))

#     # Example: Press 'Ctrl+R' to speak a reminder
#     keyboard.add_hotkey('ctrl+r', lambda: speak("This is your reminder."))

#     # Keep listening to the keyboard
#     keyboard.wait()

import threading
import keyboard

def setup_keyboard_shortcuts():
    def monitor_shortcuts():
        print("Keyboard shortcut listener started.")
        keyboard.wait('esc')  # Replace 'esc' with your desired key or shortcut.
        print("Keyboard shortcut triggered!")
    
    # Run the keyboard listener in a separate thread
    listener_thread = threading.Thread(target=monitor_shortcuts, daemon=True)
    listener_thread.start()
