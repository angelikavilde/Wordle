import json, string, random

def open_word_list():
    with open("words.json", "r") as file:
        word_data = json.load(file)
        return word_data

def generate_random_word(word_data): #add str or list
    return random.choice(word_data)

def show_game(word: list, letters_exist: set, guess: str, random_word: str):
    pass

def guess_word():
    return input("Word guess: ")

def check_word(guess: str):
    letters_list = string.ascii_lowercase

    if len(guess) != 5:
        raise ValueError("Wrong length of input. Only 5 letters allowed.")
    for value in guess:
        if not value.lower() in letters_list:
            raise ValueError("Wrong input")
    return True

def check_letters(answer: str, guess:str):
    word = ["","","","",""]
    letters_exist = set()
    for indx,letter in enumerate(guess):
        if letter in answer:
            if answer[indx] == guess[indx]:
                word[indx] = letter
            else:
                letters_exist.append(letter)
    return word, letters_exist

def confirm_answer(answer: str, guess:list) -> bool:
    if "".join(guess) == answer:
        return True
    return False

def play(word_data) -> None:
    random_word = generate_random_word(word_data)
    guesses = 0
    while guesses <= 5:
        guess = guess_word()
        if not check_word(guess):
            continue
        else:
            word, letters_exist = check_letters(random_word, guess)
            if confirm_answer(random_word, word):
                show_game(word, letters_exist, guess, random_word)
                print("You win!")
                return
            else:
                show_game(word, letters_exist, guess, random_word)
                guesses += 1
    print("Game over!")
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

