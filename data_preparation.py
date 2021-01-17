class PositionData:
    def __init__(self, file_path, line):
        self.file_path = file_path
        self.line = line

class preparator_utilities:
    
    @staticmethod    
    def prepare_line(i_line):
        i_line.strip()
        letters_and_spaces= ''.join(letter for letter in i_line if (letter.isalnum() or  letter ==' '))
        letters_and_spaces=letters_and_spaces.lower()
        return letters_and_spaces

    @staticmethod
    def is_separator(char):
        return (not char.isalnum())



import os
import sys
class DB_importer:

    def __init__(self, i_tri_to_import_to):
        self.import_to = i_tri_to_import_to

    def mock_import_from_file(self):
        example_text ="{}\n{}\n{}\n{}\n{}\n{}\n".format("i want","I wAnt To Be Happy",
                                                    "nothing is Better, than now",
                                                    "what comes up must go down",
                                                    "i want to be happy together",
                                                    "i want banana"
                                                    )
        text_seperated_by_newline = example_text.split('\n')
        for line in text_seperated_by_newline:
            clean_line = preparator_utilities.prepare_line(line)
            self.import_to.insert(clean_line)

    def import_from_file(self,file_location):
        file1 = open(file_location, 'r') 
        line = file1.readline()
        line_num = 0
        while line: 
            clean_line = preparator_utilities.prepare_line(line)
            self.import_to.insert(clean_line, line_num, file_location)
            line = file1.readline()
            line_num += 1
  
        file1.close() 

class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char, file_path=None, line_num=None):
        # the character stored in this node
        self.char = char
        self.data = [PositionData(file_path, line_num)]


        # whether this can be the end of a word
        self.is_word_end = False




        #  to add later
        self.is_sentence_end = False
        #if issetnecence_end --> add metadata class--->  origin_file_name , line_number , offset




        #TODO : add file_data_to_sentence,way to get the orgin sentence

        # a counter indicating how many times a word is inserted
        # (if this node's is_end is True)
        self.appearances = 0

        #todo add max_appearnces_in_children
        # a dictionary of child nodes
        # keys are characters, values are nodes
        # key is char -> value is pointer to a node in the trie
        self.children = {}
        #TODO  change this to a priority queue depending on the max_appearances


class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")

    def insert(self, word, line_num, file_location, offset=0):
        """Insert a word into the trie"""
        node = self.root

        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        previous_node = None
        for i in range(len(word)):
            char = word[i]
            previous_node = node

            if char in node.children:
                node.data.append(PositionData(file_location, line_num))
                node = node.children[char]
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char, file_location, line_num)
                node.children[char] = new_node
                node = new_node
            if previous_node and char == ' ':
                self.insert(word[i+1:], line_num, file_location)
                previous_node.is_word_end = True

            if node.is_word_end:
                 # Increment the counter to indicate that we see this word once more
                node.appearances += 1

            #
            # if is_separator(char):
            #     previous_node.is_word_end = True
            #     #TODO: make sure this works

        # Mark the end of a word
        node.is_word_end = True
        node.is_sentence_end = True
         # Increment the counter to indicate that we see this word once more
        node.appearances += 1
       

    def dfs(self, node, prefix, score):
        """Depth-first traversal of the trie

        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if node.is_sentence_end:
            for position in node.data:
                self.output.append((prefix + node.char, score, position.line))

        for child in node.children.values():
            self.dfs(child, prefix + node.char, score)

    def query(self, x):
        """Given an input (a prefix), retrieve all words stored in
        the trie with that prefix, sort the words by the number of
        times they have been inserted
        """
        # Use a variable within the class to keep all possible outputs
        # As there can be more than one word with such prefix
        self.output = []
        node = self.root

        # Check if the prefix is in the trie
        score = 0
        for char in x:
            if char in node.children:
                node = node.children[char]
                score += 2
            else:


                # cannot found the prefix, return empty list, try changing letter and
                return []

        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1], score)

        # Sort the results in reverse order and return
        return sorted(self.output, key=lambda x: x[0], reverse=True)


    def optimize(self,x):
        pass
        #optimizations:
            # if there is a strand for only 1 word we can take the word instead of the letters
            #have the children in priority queue depending on the max_appearnaces

tree = Trie()
importer = DB_importer(tree)
importer.import_from_file("words.txt")
print(tree.query("want"))
print("done")

