import locale
import datetime
import pyfiglet
import sys

def date(form="%Y %d %b, %A", shr='graceful'):
    locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
    date = datetime.datetime.today()
    pf = pyfiglet.figlet_format(date.strftime(form), font=shr)
    return pf

if __name__ == '__main__':
    if len(sys.argv) < 4:
        if len(sys.argv) == 1:
            print(date())
        elif len(sys.argv) == 2:
            print(date(sys.argv[1]))
        elif len(sys.argv) == 3:
            print(date(sys.argv[1],sys.argv[2]))
    else:
        print("please, check input format")
