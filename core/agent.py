import subprocess
import os

class PohyiBrain:
    def __init__(self):
        # We use the absolute path because the installation just finished 
        # and the PATH variable might not be updated in all running processes yet.
        user_profile = os.environ.get('USERPROFILE', 'C:\\Users\\antik')
        self.agy_path = os.path.join(user_profile, 'AppData', 'Local', 'agy', 'bin', 'agy.exe')
        print(f"[Brain] Initialized using local Antigravity CLI at {self.agy_path}.")

    def analyze_event(self, event_description: str):
        prompt = (
            "You are Pohyi, an autonomous desktop agent. "
            "Analyze this system event and decide what to do next:\n"
            f"Event: {event_description}\nDecision:"
        )
        
        try:
            # Invoking Antigravity CLI directly via absolute path
            result = subprocess.run(
                [self.agy_path, prompt],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"[Brain] Error calling agy CLI: {e.stderr}")
            return "Error calling local AI CLI."
        except FileNotFoundError:
            print(f"[Brain] 'agy' command not found at {self.agy_path}. Make sure it is installed.")
            return "AI CLI not found."
