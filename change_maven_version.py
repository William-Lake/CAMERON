from argparse import ArgumentParser,RawTextHelpFormatter
import ctypes
from pathlib import Path
import platform
import os
import subprocess
import traceback
from sys import exit

import colorama
from colorama import Fore, Back, Style


def convert_to_num(user_selection):

    try:

        return int(user_selection.strip())

    except:

        return None


def select_maven_home(maven_dirs):

    user_selection = None

    while user_selection is None:

        print("Please select one of the following as your new MAVEN_HOME:\n")

        for idx, d in enumerate(maven_dirs):

            print(f"[{idx + 1}] : {d.absolute()}")

        user_selection = convert_to_num(input("\n\n\n?"))

        if user_selection is not None and (
            0 < user_selection and user_selection <= len(maven_dirs)
        ):

            return maven_dirs[user_selection - 1]

        print("PLEASE PROVIDE VALID INPUT" + os.linesep * 6)


def collect_maven_dirs():

    # TODO Use subprocess and run "where mvn"

    maven_dirs = []

    for dir in Path(r"C:\Program Files").iterdir():

        if not dir.is_dir() or not dir.stem.startswith("apache"):
            continue

        potential_mvn_files = [dir for dir in dir.glob("**/mvn") if not dir.is_dir()]

        is_maven_dir = len(potential_mvn_files) > 0

        if is_maven_dir:

            maven_dirs.append(dir)

    return maven_dirs


def main(args):

    maven_home = os.environ["MAVEN_HOME"]

    print(f"\t---  Current Maven Home is {maven_home}  ---\n\n\n")

    maven_dirs = collect_maven_dirs()

    # TODO Is there a better way to perform this check?
    if not maven_dirs:

        exit_with_error(
            "No Maven directory found. What? How did this even...never mind. Just install Maven then get back to me."
        )

    new_maven_home = select_maven_home(maven_dirs)

    try:

        subprocess.run(
            ["setx", "MAVEN_HOME", "-m", f"{new_maven_home.absolute().as_posix()}"],
            shell=True,
            check=True,
        )

    except:

        error_message = f"""{Fore.RED}
Exception thrown while trying to change MAVEN_HOME environment variable from

    {Fore.GREEN}{maven_home.absolute().__str__()}{Fore.RED}

to

    {Fore.GREEN}{new_maven_home.absolute().__str__()}{Fore.RED}

The error was:{Fore.YELLOW}

{traceback.format_exc()}
"""

        exit_with_error(error_message, add_color=False)


def is_admin():  # https://raccoon.ninja/en/dev/using-python-to-check-if-the-application-is-running-as-an-administrator/

    try:

        is_admin = os.getuid() == 0

    except AttributeError:

        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin


def exit_with_error(error_message, add_color=True):

    addl_color = Fore.RED if add_color else ""

    print(addl_color + error_message)

    exit(1)


def review_requirements():

    error_message_requirement_check_dict = {
        "This script has only been set up to work on Windows, sorry.": lambda: "Windows"
        in platform.system(),
        "!!!!! THIS SCRIPT NEEDS TO BE RAN FROM AN ADMIN COMMAND PROMPT FOR IT TO WORK !!!!!": lambda: is_admin(),
        "No MAVEN_HOME environment variable found. Set this variable, then try again.": lambda: "MAVEN_HOME"
        in os.environ.keys(),
    }

    for (
        error_message,
        requirement_check,
    ) in error_message_requirement_check_dict.items():

        if not requirement_check():

            exit_with_error(error_message)


def print_banner():

    print(
        f"""
{Fore.GREEN}
                                           
 _____ _____ _____ _____ _____ _____ _____ 
|     |  _  |     |   __| __  |     |   | |
|   --|     | | | |   __|    -|  |  | | | |
|_____|__|__|_|_|_|_____|__|__|_____|_|___|
                                           
{Fore.YELLOW}ChAnge Maven vERsiON{Fore.RESET}
"""
    )
    
def gather_args():
    
    arg_parser = ArgumentParser(description='Changes your maven version.',formatter_class=RawTextHelpFormatter,prog="CAMERON.exe")
    
    arg_parser.add_argument('-v',action='store_true',dest='verbose',help='Whether to log verbose actions.') # TODO
    
    return arg_parser.parse_args()

if __name__ == "__main__":

    colorama.init()

    print_banner()
    
    args = gather_args()

    review_requirements()

    main(args)
