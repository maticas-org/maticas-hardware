import os
import json

class DataBase():

    def __init__(self,
                 filename: str) -> None:

        #check if is json file
        if not filename.endswith('.jsonl'):
            raise ValueError('Filename must end with ".json"')

        self.filename = filename

        #create file if it does not exist
        if self.filename not in os.listdir('.'):
            self.create_file()
            print('File "{}" created.'.format(self.filename))
        else:
            print('File "{}" already exists.'.format(self.filename))
        print('Initialized DataBase.')

    def create_file(self) -> None:
        file = open(self.filename, 'w')
        file.close()

    def read_file(self) -> iter:
        file = open(self.filename, 'r')
        for line in file:
            yield json.loads(line)
        file.close()

    def write_file(self, data: dict) -> None:
        file = open(self.filename, 'a')
        file.write(json.dumps(data) + '\n')
        file.close()

    def rewrite_file(self, 
                     remove_data: list = None) -> None:
        """
            As memory is limited, we cannot store all data in memory.
            So we create a new file, with a similar name, and write
            all the data we want to keep there. Then we delete the old
            file and rename the new file to the old name.
        """

        #create new file
        new_filename = self.filename + '.new'
        new_file = open(new_filename, 'w')

        #write data to new file
        for data in self.read_file():
            if data not in remove_data:
                new_file.write(data)

        #close new file
        new_file.close()

        #delete old file
        self.delete_file()

        #rename new file to old name
        os.rename(new_filename, self.filename)

    def delete_file(self) -> None:
        os.remove(self.filename)