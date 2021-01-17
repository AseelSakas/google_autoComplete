def to_lower(line):
    pass

def seprator_cleanup(line):
    pass

def prepare_line(line):
    line = to_lower(line)
    line = seprator_cleanup(line)
    return line

def is_separator(char):
    pass

class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_word_end = False

        #TODO : add file_data_to_sentence,way to get the orgin sentence

        # a counter indicating how many times a word is inserted
        # (if this node's is_end is True)
        self.appearances = 0

        # a dictionary of child nodes
        # keys are characters, values are nodes
        # key is char -> value is pointer to a node in the trie
        self.children = {}


class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")

    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root

        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        previous_node = None
        for char in word:
            previous_node = node

            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
            if previous_node and char == ' ':
                previous_node.is_word_end = True

            #
            # if is_separator(char):
            #     previous_node.is_word_end = True
            #     #TODO: make sure this works

        # Mark the end of a word
        node.is_word_end = True

        # Increment the counter to indicate that we see this word once more
        node.appearances += 1

    def dfs(self, node, prefix):
        """Depth-first traversal of the trie

        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if node.is_word_end:
            self.output.append((prefix + node.char, node.appearances))

        for child in node.children.values():
            self.dfs(child, prefix + node.char)

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
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return []

        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1])

        # Sort the results in reverse order and return
        return sorted(self.output, key=lambda x: x[1], reverse=True)


tree = Trie()
tree.insert("it will happen")
tree.insert("it willow")
tree.insert("i want burger")
print("done")

