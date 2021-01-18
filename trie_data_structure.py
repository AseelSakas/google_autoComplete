from preparator_utilities import preparator_utilities


class PositionData:
    def __init__(self, file_path, line):
        self.file_path = file_path
        self.line_index = line


class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char, file_path=None, line_num=None):
        # the character stored in this node
        self.char = char
        self.positions = []

        #todo add max_appearnces_in_children
        # a dictionary of child nodes
        # keys are characters, values are nodes
        # key is char -> value is pointer to a node in the trie
        self.children = {}

    def add_position(self,file_path,line_num):
        self.positions.append(PositionData(file_path, line_num))


class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")
        self.output = []
        self.scores = []

    def insert(self, word, line_num, file_location):
        """Insert a word into the trie"""
        node = self.root

        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for i in range(len(word)):
            char = word[i]
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
                self.insert(word[i+1:], line_num, file_location)
                previous_node.is_word_end = True
        # its the node of end of a sentence , add the position of this sentence
        node.add_position(file_location,line_num)

    # check if this line is already in the suggestions
    def in_scores(self, position):
        for pos in self.scores:
            if pos[0] == position:
                return True
        return False

    def get_positions(self, curr_node, score, top):

        for position in curr_node.positions:
            if (len(self.scores) >= top):
                return
            if not self.in_scores(position):
                self.scores.append((position, score))
        for child in curr_node.children.values():
            self.get_positions(child, score, top)
        return

    # searches for the phrase in the suffix trie
    def query(self, phrase,top, start_node=None, idx =0, score =0, fixed_letter= False):

        node = start_node
        if len(self.scores) >= top:
            return
        if idx == len(phrase):
            if node != self.root:
                self.get_positions(node,score,top)
            return

        char = phrase[idx]
        if char in node.children:
            # full match
            self.query(phrase, top, node.children[char], idx + 1, score + 2)
        if not fixed_letter:
            # exchange
            exchange_tax = preparator_utilities.get_exchange_tax(idx)
            deletion_tax = preparator_utilities.get_deletion_tax(idx)


            for char in node.children.keys():
                # letter_exchange
                self.query(phrase, top,  node.children[char], idx + 1, score - exchange_tax, True)
                # letter_deletion
                self.query(phrase, top, node.children[char], idx, score - deletion_tax, True)

            #letter_insirtion
            self.query(phrase, top, node, idx + 1, score - deletion_tax, True)
        return

    #search in suffixTrie and save each match with apprpoiat score in self.score list, sorted
    def get_sugg_from_trie(self, phrase, top=5):
        self.query(phrase,top, self.root)
        # return sorted(self.scores, key=lambda x: x["score"],)
        self.scores = self.scores
        return self.scores

    # def optimize(self,x):
    #     pass
    #     #optimizations:
    #         # if there is a strand for only 1 word we can take the word instead of the letters
    #         #have the children in priority queue depending on the max_appearnaces

def get_line_from_file(positions):
    results = []
    for position in positions:
        file_location = position.file_path
        file1 = open(file_location, 'r')
        lines = file1.readlines()
        line_index = position.line_index
        file1.close()
        if line_index >= len(lines):
            raise Exception("wrong line_index or wrong file_path")
        results.append(lines[line_index])
    return results


def get_suggestions_lines(suggDictList):
    suggestions = []
    for suggDict in suggDictList:
        positions = suggDict["node"].positions
        suggestions.extend(get_line_from_file(positions))
    return suggestions

def get_suggestions(tree, searchPhrase, top=None):
    clean_searchPhrase = preparator_utilities.prepare_line(searchPhrase)
    match_results = tree.get_sugg_from_trie(clean_searchPhrase)
    get_suggestions_lines(match_results)
    return set(get_suggestions_lines(tree.scores))








