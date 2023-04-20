from typing import List
from utils import Color, Formatter, System
import sys


class QueryUser():
    def get_selection(self) -> int:
        while True:
            print(
                Color.orange_text("\n\nPlease select one of the following options:") +
                "\n")

            range_of_selections = []
            for o in range(len(self)):
                print(f"  {o + 1}.\t{self[o]}")
                range_of_selections.append(str(o + 1))
            print(f"  q.\tQuit Application")

            selection = input(f"\n  {Color.prompt()} SELECTION: ").lower()
            if selection in ["q", "quit"]:
                sys.exit()
            try:
                if selection in range_of_selections:
                    return int(selection)
                else:
                    raise ValueError
            except ValueError:
                Formatter.note(
                    f"\n'{selection}' is invalid. Please enter only {range_of_selections} or q\n")

    def get_bool(self) -> bool:
        while True:
            print(Color.orange_text(f"\n\n{self}"))
            response = input(
                f"\n  {Color.prompt()} SELECTION (Y / N) [or q to quit app]: ").lower()
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            elif response in ["q", "quit"]:
                sys.exit()
            else:
                Formatter.note(
                    f"\n'{response}' is invalid. Please enter only [y, n or q].\n")

    def get_int(self, min: int, max: int) -> int:
        while True:
            print(Color.orange_text(f"\n\n{self}"))
            response = input(
                "\n  " +
                Color.prompt() +
                f" Enter any whole number between {min}-{max} [or 'q' to quit app]: ").lower()
            if response.isdigit() and int(response) >= min and int(response) <= max:
                return int(response)
            if response in ["q", "quit"]:
                sys.exit()
            else:
                Formatter.note(
                    f"\n'{response}' is invalid. Please only enter a number between {min} - {max}, or 'q' to quit app]\n")

    def get_float(self, min: float) -> float:
        while True:
            print(Color.orange_text(f"\n\n{self}"))
            response = input(
                f"\n  {Color.prompt()} Enter any number larger than {min} [or 'q' to quit app]: ").lower()
            if response in ["q", "quit"]:
                System.exit()
            try:
                return float(response)
            except ValueError:
                Formatter.note(
                    f"\n'{response}' is invalid. Please only enter a number greater than {min}, or 'q' to quit app]\n")

    def get_collection_id(self) -> str:
        while True:
            print(Color.orange_text(f"\n\n{self}"))
            response = input(
                f"\n  {Color.prompt()} Please enter an ID starting with 'col' [or 'q' to quit app]: ").lower()
            response = response.strip(" ")
            if (
                len(response) == 62
                and response[:3] == "col"
                and response.isalnum()
            ):
                return response
            if response in ["q", "quit"]:
                sys.exit()
            else:
                Formatter.note(
                    f"\n'{response}' is invalid. Please enter a 62 character collection ID starting with 'col', or 'q' to quit app.\n")

    def get_did(self) -> str:
        while True:
            print(Color.orange_text(f"\n\n{self}"))
            response = input(
                f"\n  {Color.prompt()} Please enter a DID starting with 'did:chia:' [or 'q' to quit app]: ").lower()
            response = response.strip(" ")
            if (
                len(response) == 68
                and response[:9] == "did:chia:"
                and response[9:].isalnum()
            ):
                return response
            if response in ["q", "quit"]:
                sys.exit()
            else:
                print(response)
                Formatter.note(
                    f"'{response}' is invalid. Please enter a 68 character DID starting with 'did:chia:', or q.\n")
