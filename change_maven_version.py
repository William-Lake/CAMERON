import glob
import logging
from pathlib import Path
import os
import subprocess


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

    maven_dirs = []

    for dir in Path(r"C:\Program Files").iterdir():

        if not dir.is_dir() or not dir.stem.startswith("apache"):
            continue

        potential_mvn_files = [dir for dir in dir.glob("**/mvn") if not dir.is_dir()]

        is_maven_dir = len(potential_mvn_files) > 0

        if is_maven_dir:

            maven_dirs.append(dir)

    return maven_dirs


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    print(
        "!!!!! THIS SCRIPT NEEDS TO BE RAN FROM AN ADMIN COMMAND PROMPT FOR IT TO WORK !!!!!\n\n\n"
    )

    maven_home = None

    try:

        maven_home = os.environ["MAVEN_HOME"]

    except KeyError as e:

        logging.error(
            "No MAVEN_HOME environment variable found. Set this variable, then try again."
        )

        exit(1)

    maven_dirs = collect_maven_dirs()

    if not maven_dirs:

        logging.error(
            "No Maven directory found. What? How did this even...never mind. Just install Maven then get back to me."
        )

        exit(1)

    print(f"\t---  Current Maven Home is {maven_home}  ---\n\n\n")

    new_maven_home = select_maven_home(maven_dirs)

    try:

        subprocess.run(
            ["setx", "MAVEN_HOME", "-m", f"{new_maven_home.absolute().as_posix()}"],
            shell=True,
            check=True,
        )

    except:

        logging.error(
            "Error thrown when trying to set environment variable. You may need to run this script from an admin prompt."
        )

        exit(1)
