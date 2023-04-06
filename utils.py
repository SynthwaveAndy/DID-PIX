from sys import exit
import os

class ProgressBar():
    ## Helper function for generating progress bars    
    def create(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#', printEnd = "\r"):
        total = len(iterable)
        
        # Progress Bar Printing Function
        def printProgressBar (iteration):
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print(f'\r{Color.white_highlight("INFO   ")}{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
            
        # Initial Call
        printProgressBar(0)
        
        # Update Progress Bar
        for i, item in enumerate(iterable):
            yield item
            printProgressBar(i + 1)
        
        # Print New Line on Complete
        print()
    
    
class Color():
    def red_text(msg : str): return f"\033[1;31;40m{msg}\033[0m"
    def green_text(msg : str): return f"\033[1;32;40m{msg}\033[0m"
    def blue_text(msg : str): return f"\033[1;34;40m{msg}\033[0m"
    def orange_text(msg : str): return f"\033[1;33;40m{msg}\033[0m"
    
    def white_highlight(msg : str):return f"\033[1;30;47m{msg}\033[0m "
    
    def yellow_highlight(msg : str): return f"\033[1;30;43m{msg}\033[0m "
    def green_highlight(msg : str): return f"\033[1;37;42m{msg}\033[0m "
    def red_highlight(msg : str): return f"\033[1;30;41m{msg}\033[0m "
    
    def prompt(): return f"\033[1;30;47m>>\033[0m "
    

class Log():
    def INFO(msg : str): print(Color.white_highlight("INFO   ") + msg)
    def WARN(msg : str): print(Color.yellow_highlight("WARNING") + msg)
    def NOTE(msg : str): print(Color.yellow_highlight("NOTICE ") + msg)
    def PASS(msg : str): print(Color.green_highlight("SUCCESS") + msg)
    def ERR(msg : str): print(Color.red_highlight("ERROR  ") + msg)
        
        
class System():
    def clear():
        if os.name == 'nt': os.system('cls') # Clear command for Windows
        else: os.system('clear') # Clear command for Unix/Linux/MacOS
    
    def exit(msg : str = "Elected to Quit Application"):
        print("\n")
        Log.NOTE(f"{msg}\n\n {Color.prompt()} Press Enter to exit..")
        input()
        exit()
