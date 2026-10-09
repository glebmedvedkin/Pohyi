import time
import threading
from pynput import mouse, keyboard

class ActivityTracker:
    def __init__(self):
        self.last_activity_time = time.time()
        self.is_active = True
        self._mouse_listener = None
        self._keyboard_listener = None

    def _on_activity(self, *args, **kwargs):
        self.last_activity_time = time.time()
        if not self.is_active:
            print("[Activity] User is back.")
            self.is_active = True

    def start(self):
        print("Starting Activity Tracker...")
        self._mouse_listener = mouse.Listener(
            on_move=self._on_activity,
            on_click=self._on_activity,
            on_scroll=self._on_activity
        )
        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_activity
        )
        self._mouse_listener.start()
        self._keyboard_listener.start()
        
        # Start a background thread to check for inactivity
        threading.Thread(target=self._monitor_inactivity, daemon=True).start()

    def _monitor_inactivity(self):
        while True:
            time.sleep(5)
            if self.is_active and (time.time() - self.last_activity_time > 60):
                print("[Activity] User has been inactive for 1 minute.")
                self.is_active = False

    def stop(self):
        if self._mouse_listener:
            self._mouse_listener.stop()
        if self._keyboard_listener:
            self._keyboard_listener.stop()
