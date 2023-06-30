import json, string, random
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.style import Style

console = Console()

def open_word_list() -> any:
    with open("words.json", "r") as file:
        word_data = json.load(file)
        return word_data

def generate_random_word(word_data: list[dict]) -> list:
    i = random.randint(0,len(word_data))
    return word_data[i]

def show_game(word: list[list[str]], letters_exist: list[set[str]], guess_list: list[str]) -> Table:
    
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
    colour_list = []
    for indx,letter in enumerate(guess):
        if letter in letters_exist:
            colour_list.append("yellow")
        elif word[indx]:
            colour_list.append("green")
        else:
            colour_list.append("blue")
    return colour_list

def guess_word():
    return input("Word guess: ")

def check_word(guess: str) -> bool:
    letters_list = string.ascii_lowercase

    if len(guess) != 5:
        return False
    for letter in guess:
        if not letter.lower() in letters_list:
            return False
    return True

def check_letters(answer: str, guess:str) -> tuple[list[str],set]:
    word = ["","","","",""]
    letters_exist = set()
    for indx,letter in enumerate(guess):
        if letter in answer:
            if answer[indx] == guess[indx]:
                word[indx] = letter
            else:
                letters_exist.add(letter)
    return word, letters_exist

def confirm_answer(answer: str, guess:list[str]) -> bool:
    if "".join(guess) == answer:
        return True
    return False

def play(word_data:list[dict]) -> None:
    random_word_dict = generate_random_word(word_data)
    #random_word_dict = {"curls": "A piece or lock of curling hair; a ringlet."}
    random_word = list(random_word_dict.keys())[0]
    guesses = 0
    console.print("*", style="green", end=" - Correct place and letter\n")
    console.print("*", style="yellow", end=" - Correct letter only\n")
    currently_guessed, letters_exist, guess_list = [], [], []
    while guesses < 5:
        if guesses == 4:
            clue = input("Would you like a clue: ")
            if "n" not in clue:
                print(list(random_word_dict.values())[0])
        possible_guess = guess_word()
        if not check_word(possible_guess):
            print("Wrong input format")
            continue
        guess_list.append(possible_guess)
        one_currently_guessed, one_letters_exist = check_letters(random_word, guess_list[guesses])
        currently_guessed.append(one_currently_guessed)
        letters_exist.append(one_letters_exist)
        table = (show_game(currently_guessed, letters_exist, guess_list))
        console.print(table)
        if confirm_answer(random_word, currently_guessed[-1]):
            print("You win!")
            return
        else:
            guesses += 1
    print("Game over!")
    print(f"The correct word was {random_word}")
    return

if __name__ == "__main__":
    word_data = open_word_list()
    game = True
    while game == True:
        play(word_data)
        print("Thank you for playing.")
        play_game = input("Would you like to play again?")
        if "n" in play_game or "q" in play_game or "f" in play_game:
            game = False
