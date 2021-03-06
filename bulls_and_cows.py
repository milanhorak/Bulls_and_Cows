#!/usr/bin/env python3

import os
import random
import sys
import time


def cl_scr():
    """cleans the terminal"""
    if sys.platform == "linux" or sys.platform == "darwin":
        os.system("clear")
    else:
        os.system("cls")


def greater(sepa: str) -> None:
    """ welcomes in the game with the possible display of rules """
    cl_scr()
    print("", sepa, "Welcome to Bulls and Cows game".center(len(sepa)), sepa, sep="\n")
    while True:
        rule = input("\n\n\"Enter\" to continue..., \"r\" to read game rules: ").lower()
        if rule == "":
            cl_scr()
            break
        elif rule == "r":
            rules(sepa)
            break


def rules(sepa: str) -> None:
    """ prints out game instruction """
    cl_scr()
    print("",
          sepa,
          "GAME RULES".center(len(sepa)),
          sepa,
          "The 4 digits secret number was generated by app.\n",
          "Your task is to guess this number.",
          "This number has no duplicities.",
          "And of course it doesn't start with zero.",
          sepa,
          sep="\n")
    input("\n\"Enter\" to continue...")

    cl_scr()
    print("",
          sepa,
          "Upon making a guess, Bulls and Cows will be provided.",
          "\nBulls indicate the number of correct digits in",
          "the correct position and cows indicate",
          "the number of correct digits in the wrong position.",
          "\nFor example, if the secret number is 1234",
          "and the guessed number is 1246 then we have:",
          "* 2 BULLS for the exact matches of digits 1 and 2",
          "* 1 COW for the match of digit 4 in the wrong position",
          sepa,
          sep="\n")
    input("\n\"Enter\" to continue...")

    cl_scr()
    print("",
          sepa,
          "The game ends if you:",
          "* ran out of tries or,",
          "* guess the secret number.",
          sepa,
          sep="\n")
    input("\n\"Enter\" to continue...")

    cl_scr()
    print("", sepa, "Let's play the game.".center(len(sepa)), sepa, sep="\n")
    input("\n\"Enter\" to continue...")
    cl_scr()


def gen_number() -> int:
    """ generates random integer without duplicate digits """
    while True:
        num = random.randint(1_000, 9_999)
        if no_duplicities(num):
            return num


def no_duplicities(num: int) -> bool:
    """ checks if number contains duplicates"""

    if len(str(num)) == len(set(str(num))):
        return True
    else:
        return False


def en_int(prompt: str, digits: str = "", ) -> int:
    """
    takes input as an integer and check number of digits
    :param prompt: adjusts input prompt
    :param digits: a whole positive number as a string
                    default: digits_ = "" means no exact number of digits for integer
                    e.g. digits_ = "4 " means input must be 4 digit integer
    :return: positive integer
    """
    while True:
        try:
            num = int(input(f"\nEnter {digits}{prompt}: "))

            if digits == "":
                if num > 0:
                    return num
                else:
                    print("Enter number bigger than 0, please")
            elif digits != "":
                if not num > 0:
                    print("Enter number bigger than 0, please")
                elif not no_duplicities(num):
                    print("The number should not has duplicity digits.")
                elif num not in range(1_000, 10_000):
                    print(f"Enter {digits}digit number only, please.")
                else:
                    return num

        except (NameError, ValueError):
            print("Enter a whole positive number, please.")


def get_bulls_cows(num: int, guess: int) -> list:
    """
    Finds the common digits with exact matches (bulls) and the common digits in the wrong position (cows)
    :param num: the number to be guessed
    :param guess: the player's guess
    :return: [bulls, cows]
    """
    bull_cows = [0, 0]
    num_str = str(num)
    guess_str = str(guess)
    for index, item in enumerate(guess_str):

        # item in num_str
        if item in num_str:

            # item match position
            if item == num_str[index]:
                bull_cows[0] += 1
            # item not match position
            else:
                bull_cows[1] += 1

    return bull_cows


def show_bulls_cows(bulls_cows: list) -> None:
    """
    adjusted print of bulls_cows list
    :param bulls_cows: list bulls_cows
    :return: nothing
    """
    b = "bull"
    c = "cow"
    if bulls_cows[0] > 1:
        b = "bulls"
    if bulls_cows[1] > 1:
        c = "cows"

    print(bulls_cows[0], b + ",", bulls_cows[1], c)


def end(player, sepa) -> bool:
    """ evaluates user input to continue or quit the program """
    while True:
        user_input = input("\n\n\'Enter\' to play another game...\'q\' to quit ").lower()
        if user_input == "q":
            cl_scr()
            print("", sepa, f"{player}, thank you for the game.".center(len(sepa)), sepa, "", sep="\n")
            return True
        elif user_input == "":
            return False


def wr_to_file(game_row: dict) -> None:
    """ writes game statistic into file """
    try:
        with open('bac_results.txt', 'r+') as f:
            pom = f.read()
            f.seek(0)
            f.write(f'{game_row}\n')
            f.write(f'{pom}')
            f.flush()
            f.close()
            print("\nGame statistics saved into 'bac_results.txt'.")

    except FileNotFoundError:
        with open('bac_results.txt', 'w') as f:
            f.write(f'{game_row}')
            f.close()
            print("\nCreated 'bac_results.txt' with game statistics.")


def name() -> str:
    """ takes player's name """
    while True:
        user_input = input("\nEnter your name: ").title()
        if len(user_input) < 3:
            print("The name should has 3 letters at least.")
        elif not user_input.isalpha():
            print("The name should consist of alphabetic characters only.")
        else:
            return user_input
        print("Try again please.")


def main():
    sepa: str = "-" * 55
    """ greater """
    greater(sepa)
    player = name()

    while True:
        """setting variables"""
        cl_scr()
        guesses: int = 0
        num: int = gen_number()
        tries: int = en_int("number of tries")
        cl_scr()
        game_id: str = time.strftime("%a %d.%m.%Y %H:%M:%S")
        game_row: dict = {
            game_id: {
                "player": player,
                "result": None,
                "num": None,
                "tries": tries,
                "guesses": None,
                "duration": None,
                "row_guesses": {}
            }
        }

        """play game"""
        game_start: float = time.time()
        while tries > 0:

            """player's guess"""
            guess: int = en_int("digit guess", "4 ")
            bulls_cows: list = get_bulls_cows(num, guess)
            show_bulls_cows(bulls_cows)
            print(sepa)
            tries -= 1
            guesses += 1

            game_row[game_id]["row_guesses"][f"guess_{str(guesses)}"] = (guess, bulls_cows)

            """evaluation of guess"""
            if guess == num:
                game_row[game_id]["result"] = "WON"

                print("Congrats!!!", end="", flush=True)
                time.sleep(1)
                print(f"\rYou guessed right in {guesses} guesses!!!", "")
                break
        else:
            game_row[game_id]["result"] = "LOST"
            print(f"You've ran out of tries. The number was {num}.")

        """duration of the game"""
        game_stop: float = time.time()
        duration_sec: float = game_stop - game_start
        duration: str = time.strftime("%H:%M:%S", time.gmtime(duration_sec))
        print("Game duration: " + duration, sep="\n")

        """update game_row"""
        game_row[game_id]["num"] = num
        game_row[game_id]["duration"] = duration
        game_row[game_id]["guesses"] = guesses

        """ writes game record to the file """
        wr_to_file(game_row)
        print(sepa)

        if end(player, sepa):
            break


if __name__ == '__main__':
    main()
