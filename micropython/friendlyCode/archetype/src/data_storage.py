import os
import json
from machine import Pin, SPI

"""
import os
from src.dependencies import sdcard
from machine import SPI, Pin
spi = SPI(2)
spi.init()
sd = sdcard.SDCard(spi, Pin(5))
vfs = os.VfsFat(sd)
os.mount(vfs, "/fc")
"""

class DataBase():

    def __init__(self,
                 filename: str,
                 sd_card_dir: str = '/sd',) -> None:

        #check if is json file
        if not filename.endswith('.jsonl'):
            raise ValueError('Filename must end with ".json"')

        self.filename = filename
        self.sdcard_dir = sd_card_dir
        self.file_path = "{}/{}".format(self.sdcard_dir, self.filename)
        self.mount_sd_card()

        #create file if it does not exist
        if self.filename not in os.listdir(self.sdcard_dir):
            self.create_file()
            print('\tFile "{}" created.'.format(self.filename))
        else:
            print('\tFile "{}" already exists.'.format(self.filename))
        print('Initialized DataBase.')

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up resources and unmount the SD card
        self.unmount_sd_card()
        self.spi.deinit()

        if exc_type:
            print(f"An error occurred: {exc_val}")

        print("Exiting DataBase.")

    def mount_sd_card(self,
                      spi_group: int = 2,
                      cs: int = 5) -> None:

        from .dependencies import sdcard

        try:
            #old version
            #self.sd = sdcard.SDCard(SPI(spi_group), Pin(cs))
            #os.mount(self.sd, self.sdcard_dir)
            #files = os.listdir('/')

            self.spi = SPI(spi_group)
            self.spi.init()
            self.sd = sdcard.SDCard(self.spi(), Pin(cs))
            vfs = os.VfsFat(self.sd)

            os.mount(vfs, self.sdcard_dir)
            files = os.listdir('/')

        except Exception as e:
            print('Could not mount SD card.')
            print(e)

        else:
            print('\tMounted SD card.')
            print('\tFiles in SD card: {}'.format(files))

    def unmount_sd_card(self):
        try:
            os.umount(self.sdcard_dir)
            print("SD card unmounted successfully.")
        except Exception as e:
            print("Error unmounting SD card:", e)

    def create_file(self) -> None:
        #verify if file exists
        file = open(self.file_path, 'w')
        file.close()

    def read_file(self) -> iter:
        file = open(self.file_path, 'r')
        for line in file:
            yield json.loads(line)
        file.close()

    def write_file(self, data: dict) -> None:
        with open(self.file_path, 'a') as file:
            file.write(json.dumps(data) + '\n')

    def rewrite_file(self, 
                     remove_data: list = None) -> None:
        """
            As memory is limited, we cannot store all data in memory.
            So we create a new file, with a similar name, and write
            all the data we want to keep there. Then we delete the old
            file and rename the new file to the old name.
        """

        #create new file
        new_filename = self.file_path + '.new'
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