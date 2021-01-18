
class preparator_utilities:

    @staticmethod
    def prepare_line(i_line):
        i_line.strip()
        letters_and_spaces = ''.join(letter for letter in i_line if (letter.isalnum() or letter == ' '))
        letters_and_spaces = letters_and_spaces.lower()
        return letters_and_spaces

    @staticmethod
    def is_separator(char):
        return (not char.isalnum())


