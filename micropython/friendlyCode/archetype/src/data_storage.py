import os
import ujson

class DataBase():


    def __init__(self,
                 file_folder: str,
                 filename: str) -> None:

        print('Initializing DataBase...')

        #check if is json file
        if not filename.endswith('.jsonl'):
            raise ValueError('Filename must end with ".json"')

        self.filename = filename
        self.file_folder = file_folder

        #create file if it does not exist
        if self.filename not in os.listdir(self.file_folder):
            self.create_file()
            print('File "{}" created.'.format(self.filename))
        else:
            print('File "{}" already exists.'.format(self.filename))

    def create_file(self) -> None:
        file = open(self.file_folder + self.filename, 'w')
        file.close()

    def read_file(self) -> iter:
        file = open(self.file_folder + self.filename, 'r')
        for line in file:
            yield line
        file.close()

    def write_file(self, data: dict) -> None:
        file = open(self.file_folder + self.filename, 'a')
        file.write(ujson.dumps(data) + '\n')
        file.close()

    def empty_lines(self, lines: list) -> None:
        """
            Deletes the specified lines from the file.

            Input:
                lines: list of line numbers to be deleted.
        """

        #read the file
        file = open(self.file_folder + self.filename, 'r')
        file_lines = file.readlines()
        file.close()

        #delete the lines
        for line in lines:
            del file_lines[line]

        #wipe the file and rewrite it with the remaining lines
        file = open(self.file_folder + self.filename, 'w')
        for line in file_lines:
            file.write(line)
        file.close()

    def delete_file(self) -> None:
        os.remove(self.file_folder + self.filename)