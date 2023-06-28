import json, string, random
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

console = Console()

def open_word_list() -> any:
    with open("words.json", "r") as file:
        word_data = json.load(file)
        return word_data

def generate_random_word(word_data: list[dict]) -> list:
    i = random.randint(0,len(word_data))
    return word_data[i]

def show_game(word: list[str], letters_exist: set[str], guess: str) -> Table:
    
    table = Table(show_header=False, show_lines=True)

    for _ in range (5):
        table.add_column()

    table.add_row(guess[0],guess[1],guess[2],guess[3],guess[4])

    for indx, cell in enumerate(table.columns):
        if guess[indx] in letters_exist and guess[indx] not in word:
            cell.style = "yellow"
        if word[indx]:
            cell.style = "green"

    return table

def combine_tables(table_list:list[Table]) -> Table:
    table = Table(title="Wordle", show_header=False, show_lines=True)
    for _ in range(5):
        table.add_column()
    for t in table_list:
        row_cells = []
        for col in t.columns:
            cel_list = list(col.cells)
            row_cells.append(str(cel_list[0]))
        table.add_row(*row_cells)
    return table

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
    print(answer)
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
    random_word_dict = {"curls": "A piece or lock of curling hair; a ringlet."}
    random_word = list(random_word_dict.keys())[0]
    guesses = 0
    console.print("*", style="green", end=" - Correct place and letter\n")
    console.print("*", style="yellow", end=" - Correct letter only\n")
    guess = []
    table_list = []
    while guesses < 5:
        guess = guess_word()
        print(guesses)
        if not check_word(guess):
            print("Wrong input format")
            continue
        word, letters_exist = check_letters(random_word, guess)
        if confirm_answer(random_word, word):
            table_list.append(show_game(word, letters_exist, guess))
            table1 = combine_tables(table_list)
            console.print(table1)
            print("You win!")
            return
        else:
            table_list.append((show_game(word, letters_exist, guess)))
            table1 = combine_tables(table_list)
            console.print(table1)
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
        if "n" or "q" in play_game:
            game = False
