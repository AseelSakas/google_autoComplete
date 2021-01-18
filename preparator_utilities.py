
class preparator_utilities:


    def prepare_line(i_line):
        i_line.strip()
        letters_and_spaces = ''.join(letter for letter in i_line if (letter.isalnum() or letter == ' '))
        letters_and_spaces = letters_and_spaces.lower()
        return letters_and_spaces

    def is_separator(char):
        return (not char.isalnum())

    def get_exchange_tax(idx):
        if idx > 3 :
            return 1
        else:
            return 5-idx

    def get_deletion_tax(idx):
        if idx > 3:
            return 2
        else:
            return 10 - (2*idx)



