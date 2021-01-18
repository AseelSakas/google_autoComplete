from db_importer import DB_importer

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    importer = DB_importer()
    importer.import_from_file("trial_text.txt")
    print(importer.get_suggestions("ocupIed kafr yasif"))
    print(importer.get_suggestions("and wounding to others"))
    print(importer.get_suggestions("The village cotained a stone"))
    print("done")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
