from rich.console import Console
from wordle import check_letters, confirm_answer, check_word
from wordle import colour, create_table, play, get_clue


class TestCheckLetters:
    """Test class that verifies the letters created correctly
    in check_letters function"""
    def test_check_letters_basic(self):
        """Test to see if function check_letters
        correctly finds which letters should be green
        and which should be yellow"""
        word, letters_exist = check_letters("world","words")
        assert word == ["w","o","r","",""]
        assert letters_exist == {"d"}

    def test_check_letters_s_in_both(self):
        """Test to see if function check_letters
        correctly finds which letters should be green
        and which should be yellow for repeated letters"""
        word, letters_exist = check_letters("press","shoes")
        assert word == ["","","","","s"]
        assert letters_exist == {"s","e"}

    def test_check_letters_correct_guess(self):
        """Tests that the word was guessed fully with all
        letters in the word list and none in the letters_exist set"""
        word, letters_exist = check_letters("press","press")
        assert word == ["p","r","e","s","s"]
        assert letters_exist == set()


class TestConfirmAnswer:
    """Test class for confirming answer"""
    def test_confirm_answer_true(self):
        """Tests that the function identified
        that the answer is correct"""
        assert confirm_answer("press",list("press")) is True

    def test_confirm_answer_false(self):
        """Tests that the function identified
        that the answer is incorrect even with
        the same letters"""
        assert confirm_answer("press",list("ressp")) is False


class TestCheckWord:
    """Test class to verify guess is in correct format"""
    def test_check_word_too_long(self):
        """Test to see that the function correctly
        asserts that the word is in incorrect
        format with more than 5 letters"""
        assert check_word("asdfgt") is False

    def test_check_word_not_all_letters(self):
        """Test to see that the function correctly
        asserts that the word is in incorrect
        format with 4 letters and 1 digit"""
        assert check_word("asd4f") is False

    def test_check_word_wrong_format(self):
        """Test to see that the function correctly
        asserts that the word is in incorrect
        format with 4 letters and 1 dash"""
        assert check_word("as-ft") is False

    def test_check_word_correct(self):
        """Test to see that the function correctly
        asserts that the word is in correct
        format"""
        assert check_word("asdAt") is True


class TestColour:
    """Test class for colour function"""
    def test_colour_all_white(self):
        """Test to see if the function correctly colours
        the letters with white"""
        colours = colour("world",{},["","","","",""])
        assert colours == ["white","white","white","white","white"]

    def test_colour_no_yellow(self):
        """Test to see if the function correctly colours
        the letters with white and green"""
        colours = colour("world",{},["w","","","l",""])
        assert colours == ["green","white","white","green","white"]

    def test_colour_all_colours(self):
        """Test to see if the function correctly colours
        the letters with yellow, white and green"""
        colours = colour("worsd",{"d"},["w","o","r","",""])
        assert colours == ["green","green","green","white","yellow"]

    def test_colour_check_for_same_letter_in_both(self):
        """Test to see if the function correctly colours
        the letters that are the same but where one is green
        and another is yellow"""
        colours = colour("shoes",{"s","e"},["","","","","s"])
        assert colours == ["yellow","white","white","yellow","green"]


class TestCreateTable:
    """Test class for table creation function"""
    def test_create_table(self, capfd):
        """Test to see if the table was created correctly"""
        console = Console()
        guesses = ["words","world"]
        word = [["w","o","r","",""],["w","o","r","l",""]]
        letters_exist = [{"d"},{"d"}]
        table = create_table(word, letters_exist, guesses)
        console.print(table)
        captured = capfd.readouterr()

        assert "s" in captured.out.strip()
        assert "Wordle" in captured.out.strip()
        assert len(table.rows) == 2


class Choice:
    """Class for monkeypatch testing for other classes to inherit
    the function user_chooses"""
    def user_chooses(self, choices: list, monkeypatch) -> None:
        """Monkeypatch function to write user input for tests"""
        answers = iter(choices)
        monkeypatch.setattr('wordle.console.input', lambda name: next(answers))


class TestPlay(Choice):
    """Test class for play function with monkeypatch"""
    def test_play_function_lose(self, monkeypatch, capfd, word_dict_example: dict):
        """Test to see if the user loses not guessing correctly"""
        word_list = word_dict_example
        self.user_chooses(["red","green","numbs","means","horns","dawns","no","burns"], monkeypatch)
        play(word_list)
        captured = capfd.readouterr()

        assert "Game over!" in captured.out.strip()

    def test_play_function_win(self, monkeypatch, capfd, word_dict_example: dict):
        """Test to see if the user wins guessing correctly"""
        word_list = word_dict_example
        self.user_chooses(["red","green","numbs","means","horns","dawns","no","twins"], monkeypatch)
        play(word_list)
        captured = capfd.readouterr()

        assert "You win!" in captured.out.strip()


class TestClue(Choice):
    """Test class for clue function with monkeypatch"""
    def test_clue(self, monkeypatch, capfd):
        """Test to test whether a clue is given
        if the user inputs 'yes' """
        self.user_chooses(["yes"], monkeypatch)
        get_clue("some text")
        captured = capfd.readouterr()

        assert "some text" in captured.out.strip()

    def test_clue_false(self, monkeypatch, capfd):
        """Test to test whether a clue is not given
        if the user inputs 'no' """
        self.user_chooses(["no"], monkeypatch)
        get_clue("some text")
        captured = capfd.readouterr()

        assert "some text" not in captured.out.strip()
