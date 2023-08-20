import gc
import machine
from time import sleep


from dependencies.uQR import QRCode
from dependencies.ssd1306 import SSD1306_I2C
from utils.json_related import *
from utils.internet_connection import *
from utils.time_management_module import *

class ScreenModule():

    def __init__(self, 
                 config_file: str, 
                 screenwidth: int = 128,
                 screenheight: int = 64,
                 scl_pin: int = 22,
                 sda_pin: int = 21):

        with open(config_file) as f:
            config = load(f)
            self.ip = config["ip"]
            self.update_screen_every_some_time = Time(*config["screen"]["update_every_some_time"])
            self.last_screen_update = Time(-100, 0, 0)

        self.config_file = config_file
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin

        self.boot_screen()
        self.qr = QRCode(border=1, box_size=2)
        self.display_boot_screen()

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
        self.screen.fill(1)
        self.screen.text("Bienvenido a", self.screenwidth//8, self.screenheight//8, 0)
        sleep(1)
        self.screen.text("Maticas :D", self.screenwidth//4, self.screenheight//2, 0)
        self.screen.show()
        sleep(3.5)
    
    #=================================
    #      RESTART SCREEN RELATED
    #=================================
    def display_need_to_update_screen(self) -> None:
        self.screen.fill(1)
        self.screen.text("Guardando", self.screenwidth//8, self.screenheight//8, 0)
        self.screen.text("Cambios...", self.screenwidth//8, self.screenheight//4, 0)
        self.screen.show()
        sleep(0.85)
        self.screen.text("Reiniciando...", self.screenwidth//8, 3*self.screenheight//4, 0)
        self.screen.show()
        sleep(0.85)
    
    def display_overflow_screen(self) -> None:
        self.screen.fill(1)
        self.screen.text("RAM llena", self.screenwidth//8, self.screenheight//8, 0)
        self.screen.text("Reiniciando...", self.screenwidth//8, self.screenheight//4, 0)
        self.screen.show()
        sleep(0.85)

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

        update_json_field(self.config_file, "ip", self.ip)
    
    def display_ip(self, now: Time) -> None:
        """
            Displays the ip address on the screen.
        """

        if (now - self.last_screen_update) > self.update_screen_every_some_time:
            self.update_ip() 
            self.clear_screen()
            self.last_screen_update = now

            self.qr.clear()
            self.qr.add_data("http://{}".format(self.ip))
            matrix = self.qr.get_matrix()
            paddingx = int(self.screenwidth/4)
            paddingy = 5

            for y in range(len(matrix)*2):                   # Scaling the bitmap by 2
                for x in range(len(matrix[0])*2):            # because my screen is tiny.
                    value = not matrix[int(y/2)][int(x/2)]   # Inverting the values because
                    self.screen.pixel(x + paddingx, y + paddingy, value)                # black is `True` in the matrix.
                gc.collect()
            self.screen.show()         

            print("screen update.")