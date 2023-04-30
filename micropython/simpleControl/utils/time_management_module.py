import urequests
import re


from machine import Pin
from time 	 import sleep
from math    import fabs

def get_current_time():

    response = urequests.get('http://worldtimeapi.org/api/timezone/America/Bogota')

    if (response.status_code == 200):
        parsed  = response.json()
        h, m, s = parse_datetime_time(parsed["datetime"])

        return (h, m, s)


def parse_datetime_time(datetime_str):
    
    start = 11
    end = -7
    
    txt = datetime_str.strip()
    txt = txt[start:end]
    time_str = txt.split(":")
    
    hour = int(time_str[0])
    minute = int(time_str[1])
    second = float(time_str[2])
    
    return hour, minute, second




class Time:
    def __init__(self, hour=0, min=0, sec=0):
        """
        Initializes a new Time object with the specified hour, minute, and second values.

        Args:
            hour (int): The hour value (0-23). Default is 0.
            min (int): The minute value (0-59). Default is 0.
            sec (int): The second value (0-59). Default is 0.
        """
        self.hour = hour
        self.min = min
        self.sec = sec
        
    def __gt__(self, other):
        """
        Overload the '>' operator to allow comparison between two Time objects.

        Args:
            other (Time): The Time object to compare with.

        Returns:
            bool: True if this Time object is greater than the specified Time object, False otherwise.
        """
        if self.hour > other.hour:
            return True
        elif self.hour == other.hour and self.min > other.min:
            return True
        elif self.hour == other.hour and self.min == other.min and self.sec > other.sec:
            return True
        else:
            return False
        
    def __lt__(self, other):
        """
        Overload the '<' operator to allow comparison between two Time objects.

        Args:
            other (Time): The Time object to compare with.

        Returns:
            bool: True if this Time object is less than the specified Time object, False otherwise.
        """
        if self.hour < other.hour:
            return True
        elif self.hour == other.hour and self.min < other.min:
            return True
        elif self.hour == other.hour and self.min == other.min and self.sec < other.sec:
            return True
        else:
            return False
        
    def __eq__(self, other):
        """
        Overload the '==' operator to allow comparison between two Time objects.

        Args:
            other (Time): The Time object to compare with.

        Returns:
            bool: True if this Time object is equal to the specified Time object, False otherwise.
        """
        if self.hour == other.hour and self.min == other.min and self.sec == other.sec:
            return True
        else:
            return False
        
    def __sub__(self, other):
        """
        Overload the '-' operator to allow subtraction between two Time objects.

        Args:
            other (Time): The Time object to subtract from this Time object.

        Returns:
            Time: A new Time object representing the difference between this Time object and the specified Time object.
        """
        seconds1 = self.hour*3600 + self.min*60 + self.sec
        seconds2 = other.hour*3600 + other.min*60 + other.sec
        diff = seconds1 - seconds2
        return Time(diff // 3600, (diff % 3600) // 60, diff % 60)
        
    def __add__(self, other):
        """
        Overload the '+' operator to allow addition between two Time objects.

        Args:
            other (Time): The Time object to add to this Time object.

        Returns:
            Time: A new Time object representing the sum of this Time object and the specified Time object.
        """
        seconds1 = self.hour*3600 + self.min*60 + self.sec
        seconds2 = other.hour*3600 + other.min*60 + other.sec

        
    def __str__(self):
        """
        Overload the str() function to print only the time in hh:mm:ss format.

        Returns:
            str: A string representing the time in hh:mm:ss format.
        """
        return "{}:{}:{}".format(self.hour, self.min, self.sec)

