from typing import List
from utils import Color, Log, System

class QueryUser():
    def get_selection(options : List[str]) -> int:
        while True:
            print(Color.orange_text("\n\nPlease select one of the following options:") + "\n")
            
            range_of_selections = []
            for o in range(len(options)):
                print(f"  {o + 1}.\t{options[o]}")
                range_of_selections.append(str(o + 1))
            print(f"  q.\tQuit Application")

            selection = input(f"\n  {Color.prompt()} SELECTION: ").lower()
            if selection == "q" or selection == "quit": System.exit()
            try:
                if selection in range_of_selections:
                    return int(selection)
                else:
                    raise ValueError
            except ValueError:
                print()
                Log.NOTE(f"'{selection}' is invalid. Please enter only {range_of_selections} or q\n")


    def get_bool(query : str) -> bool:
        while True:
            print(Color.orange_text(f"\n\n{query}"))
            response = input(f"\n  {Color.prompt()} SELECTION (Y / N) [or q to quit app]: ").lower()
            if response == "y" or response == "yes": return True
            if response == "n" or response == "no": return False
            if response == "q" or response == "quit": System.exit()
            
            print()
            Log.NOTE(f"'{response}' is invalid. Please enter only [y, n or q].\n")
            
                
    def get_int(query : str, min : int, max : int) -> int:
        while True:
            print(Color.orange_text(f"\n\n{query}"))
            response = input("\n  " + Color.prompt() + f" Enter any whole number between {min}-{max} [or 'q' to quit app]: ").lower()
            if response.isdigit() and int(response) >= min and int(response) <= max:
                return int(response)
            if response == "q" or response == "quit": System.exit()
            
            print()
            Log.NOTE(f"'{response}' is invalid. Please only enter a number between {min} - {max}, or 'q' to quit app]\n")
            
            
    def get_float(query: str, min: float) -> float:
        while True:
            print(Color.orange_text(f"\n\n{query}"))
            response = input(f"\n  {Color.prompt()} Enter any number larger than {min} [or 'q' to quit app]: ").lower()
            if response == "q" or response == "quit": System.exit()
            try:
                return float(response)
            except ValueError:
                print()
                Log.NOTE(f"'{response}' is invalid. Please only enter a number greater than {min}, or 'q' to quit app]\n")
                
                
    def get_collection_id(query : str) -> str:
        while True:
            print(Color.orange_text(f"\n\n{query}"))
            response = input(f"\n  {Color.prompt()} Please enter an ID starting with 'col' [or 'q' to quit app]: ").lower()
            response = response.strip(" ")
            if len(response) == 62 and response[0:3] == "col" and response.isalnum():
                return response
            if response == "q" or response == "quit": System.exit()
            
            print()
            Log.NOTE(f"'{response}' is invalid. Please enter a 62 character collection ID starting with 'col', or 'q' to quit app.\n")
            
            
    def get_DID(query : str) -> str:
        while True:
            print(Color.orange_text(f"\n\n{query}"))
            response = input(f"\n  {Color.prompt()} Please enter a DID starting with 'did:chia:' [or 'q' to quit app]: ").lower()
            response = response.strip(" ")
            if len(response) == 68 and response[0:9] == "did:chia:" and response[9:].isalnum():
                return response
            if response == "q" or response == "quit": System.exit()
            
            print()
            Log.NOTE(f"'{response}' is invalid. Please enter a 68 character DID starting with 'did:chia:', or q.\n")