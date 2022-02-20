if __name__ == '__main__':
    from figdate.date import date
    from sys import argv
    import locale

    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    if   len(argv) == 1: print(date())
    elif len(argv) == 2: print(date(argv[1]))
    else: print(date(argv[1], argv[2]))
