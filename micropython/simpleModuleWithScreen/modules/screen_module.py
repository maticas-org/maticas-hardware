import machine
from time import sleep


from dependencies.uQR import uQR
from dependencies.ssd1306 import SSD1306_I2C
from utils.json_related import *
from utils.internet_connection import *

class ScreenModule():

    def __init__(self, 
                 config_file: str, 
                 screenwidth: int = 128,
                 screenheight: int = 64,
                 scl_pin: int = 5,
                 sda_pin: int = 4):

        with open(config_file) as f:
            config = load(f)
            self.ip = config["ip"]

        self.config_file = config_file
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin

        self.boot_screen()
        self.qr = uQR()

    def boot_screen(self) -> None:
        i2c = machine.I2C(scl=machine.Pin(self.scl_pin), sda=machine.Pin(self.sda_pin))
        self.screen = SSD1306_I2C(128, 64, i2c, 60)
        self.screen.poweron()

    def clear_screen(self) -> None:
        self.screen.fill(0)
        self.screen.show()

    #=================================
    #      BOOT SCREEN RELATED
    #=================================    
    def display_boot_screen(self) -> None:
        self.screen.text("Welcome to Maticas!!!", 0, 0)
        sleep(2)

    #=================================
    #       IP DISPLAY RELATED
    #=================================
    def update_ip(self) -> None:
        """
            Updates the ip address on the screen.
        """
        self.ip = connect2(config_file = self.config_file, doreconnect = False)
        if self.ip == None:
            self.ip = "No internet connection"

        update_json_file(self.config_file, "ip", self.ip)
    
    def display_ip(self) -> None:
        """
            Displays the ip address on the screen.
        """
        self.qr.add_data("http://{}".format(self.ip))
        matrix = self.qr.get_matrix()

        for y in range(len(matrix)*2):                   # Scaling the bitmap by 2
            for x in range(len(matrix[0])*2):            # because my screen is tiny.
                value = not matrix[int(y/2)][int(x/2)]   # Inverting the values because
                self.screen.pixel(x, y, value)                # black is `True` in the matrix.
        self.screen.show()         



