"""Wordle in the terminal"""

import json
import string
import random
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.style import Style

console = Console()

def open_word_list() -> any:
    """Function that opens the json file with words"""
    with open("words.json", "r", encoding='utf8') as file:
        word_data = json.load(file)
        return word_data

def generate_random_word(word_data: list[dict]) -> list:
    """Function that pics a random word and its 
    definition for the game"""
    i = random.randint(0,len(word_data)-1)
    return word_data[i]

def create_table(word: list[list[str]], letters_exist: list[set[str]], guess_list: list[str]) -> Table:
    """Function to create a table with rich library colouring each letter"""
    table = Table(title="Wordle", show_header=False, show_lines=True)
    for _ in range (5):
        table.add_column()
    for i,guess in enumerate(guess_list):
        colour_list = colour(guess, letters_exist[i], word[i])
        table.add_row(Text(guess[0],Style(color=colour_list[0])),Text(guess[1],\
        Style(color=colour_list[1])),Text(guess[2],Style(color=colour_list[2])),Text(guess[3]\
        ,Style(color=colour_list[3])),Text(guess[4],Style(color=colour_list[4])))
    return table

def colour(guess: str, letters_exist: set[str], word: list[str]) -> list:
    """Function that determines which colour should
    a letter be coloured in following the game rules"""
    colour_list = []
    for indx,letter in enumerate(guess):
        if word[indx]:
            colour_list.append("green")
        elif letter in letters_exist:
            colour_list.append("yellow")
        else:
            colour_list.append("white")
    return colour_list

def guess_word() -> str:
    """Prompt for a word guess in colour"""
    return console.input("Word guess: ")

def check_word(guess: str) -> bool:
    """Function that verifies that user's
    input for a guess was in the correct format"""
    letters_list = string.ascii_lowercase
    if len(guess) != 5:
        return False
    for letter in guess:
        if not letter.lower() in letters_list:
            return False
    return True

def get_clue(clue: str) -> None:
    """Function to display a clue
    if user chose to do so"""
    text = Text("Would you like a clue: ", style="bright_magenta")
    choice = console.input(text)
    if "n" not in choice:
        clue = "Clue: " + clue
        console.print(clue)

def check_letters(answer: str, guess:str) -> tuple[list[str],set]:
    """Function that returns a tuple of the list currently correctly
    guessed letters in the right place and a set of letters
    that were only correctly guessed"""
    word = ["","","","",""]
    letters_exist = set()
    for indx,letter in enumerate(guess):
        if letter in answer:
            if answer[indx] == guess[indx]:
                word[indx] = letter
            else:
                if answer.count(letter) > 1 or not letter in word:
                    letters_exist.add(letter)
    return word, letters_exist

def confirm_answer(answer: str, guess:list[str]) -> bool:
    """Function that determines if the word
    was correctly guessed"""
    if "".join(guess) == answer:
        return True
    return False

def play(word_data:list[dict]) -> None:
    """Main game function that uses connects
    all other function to run the game"""
    random_word_dict = generate_random_word(word_data)
    random_word = list(random_word_dict.keys())[0]
    guesses = 0
    console.print("*", style="green", end=" - Correct place and letter\n")
    console.print("*", style="yellow", end=" - Correct letter only\n")
    currently_guessed, letters_exist, guess_list = [], [], []
    while guesses < 6:
        if guesses == 5:
            get_clue(list(random_word_dict.values())[0])
        possible_guess = guess_word()
        if not check_word(possible_guess):
            console.print("Wrong input format", style = "red")
            continue
        guess_list.append(possible_guess)
        one_currently_guessed, one_letters_exist = check_letters(random_word, guess_list[guesses])
        currently_guessed.append(one_currently_guessed)
        letters_exist.append(one_letters_exist)
        table = create_table(currently_guessed, letters_exist, guess_list)
        console.print(table)
        if confirm_answer(random_word, currently_guessed[-1]):
            console.print("You win!", style="bright_cyan")
            return
        guesses += 1
    console.print("Game over!", style="bright_cyan")
    console.print(f"The correct word was {random_word}")
    return

if __name__ == "__main__":
    word_data = open_word_list()
    game = True
    while game is True:
        play(word_data)
        console.print("Thank you for playing.")
        play_game = console.input("Would you like to play again?")
        if "n" in play_game or "q" in play_game or "f" in play_game:
            game = False
