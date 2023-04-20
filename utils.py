import os


class Color():
    """Helper class for defining colored text"""

    @staticmethod
    def red_text(text):
        return f"\033[1;31;40m{text}\033[0m"

    @staticmethod
    def green_text(text):
        return f"\033[1;32;40m{text}\033[0m"

    @staticmethod
    def blue_text(text):
        return f"\033[1;34;40m{text}\033[0m"

    @staticmethod
    def orange_text(text):
        return f"\033[1;33;40m{text}\033[0m"

    @staticmethod
    def white_highlight(text):
        return f"\033[1;30;47m{text}\033[0m "

    @staticmethod
    def yellow_highlight(text):
        return f"\033[1;30;43m{text}\033[0m "

    @staticmethod
    def green_highlight(text):
        return f"\033[1;37;42m{text}\033[0m "

    @staticmethod
    def red_highlight(text):
        return f"\033[1;30;41m{text}\033[0m "

    @staticmethod
    def prompt():
        return f"\033[1;30;47m>>\033[0m "


class Formatter():
    """Helper class for formatting messages"""

    @staticmethod
    def info(message):
        print(Color.white_highlight("INFO       ") + message)

    @staticmethod
    def warning(message):
        print(Color.yellow_highlight("WARNING") + message)

    @staticmethod
    def note(message):
        print(Color.yellow_highlight("NOTICE ") + message)

    @staticmethod
    def success(message):
        print(Color.green_highlight("SUCCESS    ") + message)

    @staticmethod
    def error(message):
        print(Color.red_highlight("ERROR  ") + message)


class System():
    """Helper class for system-related tasks"""

    @staticmethod
    def clear():
        if os.name == 'nt':
            os.system('cls')  # Clear command for Windows
        else:
            os.system('clear')  # Clear command for Unix/Linux/MacOS
