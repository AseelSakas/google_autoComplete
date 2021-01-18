from preparator_utilities import preparator_utilities
from trie_data_structure import Trie

class DB_importer:

    def __init__(self):
        self.suffixTrie = Trie()

    def import_from_file(self, file_location):
        file1 = open(file_location, 'r')
        line = file1.readline()
        line_num = 0
        while line:
            clean_line = preparator_utilities.prepare_line(line)
            self.suffixTrie.insert(clean_line, line_num, file_location)
            line = file1.readline()
            line_num += 1
        file1.close()

    def get_line_from_file(self,position):
        results = []
        file_location = position.file_path
        file1 = open(file_location, 'r')
        lines = file1.readlines()
        line_index = position.line_index
        file1.close()
        if line_index >= len(lines):
            raise Exception("wrong line_index or wrong file_path")
        return lines[line_index]
            # results.append(lines[line_index])

    def get_suggestions_lines(self, suggDictList):
        suggestions = []
        for suggDict in suggDictList:
            position = suggDict["position"]
            suggestions.append(self.get_line_from_file(position))
        return suggestions

    def get_suggestions(self, searchPhrase, top=None):
        match_results = self.suffixTrie.get_sugg_from_trie(searchPhrase)
        self.get_suggestions_lines(match_results)
        res = set(self.get_suggestions_lines(self.suffixTrie.scores))
        self.suffixTrie.scores = []

        return res
