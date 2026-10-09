import time
import os
import threading
from dotenv import load_dotenv

from modules.file_manager import start_file_monitor
from modules.activity_tracker import ActivityTracker

# Load environment variables
load_dotenv()

def main():
    print("Starting Pohyi Agent...")
    print("Initializing File Manager and Activity Tracker...")
    
    # Start File Monitor (watching a target directory, e.g., current dir or Documents)
    # For now, let's watch the 'data' folder or current directory as a test
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    os.makedirs(target_dir, exist_ok=True)
    
    observer = start_file_monitor(target_dir)
    
    # Start Activity Tracker
    tracker = ActivityTracker()
    tracker.start()
    
    try:
        print("Pohyi is running in the background. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping Pohyi Agent...")
        observer.stop()
        tracker.stop()
    
    observer.join()

if __name__ == "__main__":
    main()
