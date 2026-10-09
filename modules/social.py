class MessengerPlugin:
    def send_message(self, recipient: str, message: str):
        raise NotImplementedError
    
    def receive_message(self):
        raise NotImplementedError

class TelegramStub(MessengerPlugin):
    def send_message(self, recipient: str, message: str):
        print(f"[TelegramStub] Sending to {recipient}: {message}")

class DiscordStub(MessengerPlugin):
    def send_message(self, recipient: str, message: str):
        print(f"[DiscordStub] Sending to {recipient}: {message}")

class SocialManager:
    def __init__(self):
        self.plugins = {
            "telegram": TelegramStub(),
            "discord": DiscordStub()
        }

    def notify_all(self, message: str):
        for name, plugin in self.plugins.items():
            plugin.send_message("admin", message)
