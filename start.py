import os.path as p


class NoConfigFileError(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == "__main__":
    if not p.isfile("config.py"):
        raise NoConfigFileError("You must generate a config file from config.sample.py to start this bot.")

    from src import main
    main.bot.run()
