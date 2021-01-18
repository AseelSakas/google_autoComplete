from preparator_utilities import preparator_utilities


class DB_importer:

    def __init__(self, i_tri_to_import_to):
        self.import_to = i_tri_to_import_to

    def mock_import_from_file(self):
        example_text = "{}\n{}\n{}\n{}\n{}\n{}\n".format("i want", "I wAnt To Be Happy",
                                                         "nothing is Better, than now",
                                                         "what comes up must go down",
                                                         "i want to be happy together",
                                                         "i want banana"
                                                         )
        text_seperated_by_newline = example_text.split('\n')
        for line in text_seperated_by_newline:
            clean_line = preparator_utilities.prepare_line(line)
            self.import_to.insert(clean_line)

    def import_from_file(self, file_location):
        file1 = open(file_location, 'r')
        line = file1.readline()
        line_num = 0
        while line:
            clean_line = preparator_utilities.prepare_line(line)
            self.import_to.insert(clean_line, line_num, file_location)
            line = file1.readline()
            line_num += 1

        file1.close()
