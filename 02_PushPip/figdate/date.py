import pyfiglet
import time

def date(fmt='%Y %d %b, %A', font='graceful'):
    return pyfiglet.figlet_format(time.strftime(fmt), font=font)

