class BotResponder:
    def __init__(self, commands_data):
        self.commands_data = commands_data

    def process_command(self, command):
        for cmd_data in self.commands_data:
            if command == cmd_data["bot_call"]:
                return "\n".join(cmd_data["reply"])
        return "Không hiểu lệnh, vui lòng thử lại."