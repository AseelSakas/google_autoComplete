from db_importer import DB_importer

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    importer = DB_importer()
    importer.import_from_file("words.txt")
    print(importer.get_suggestions("want"))
    print("done")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
