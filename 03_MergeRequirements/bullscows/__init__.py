import textdistance 

def bullscows(guess, secret):
    bulls, cows = 0, 0
    bulls = textdistance.hamming.similarity(guess, secret)
    cows = textdistance.bag.similarity(guess, secret)
    return (bulls, cows)

def gameplay(ask: callable, inform: callable, words: list[str]):
    w = random.choice(words)
    attempts = 1
    while True:
        bulls, cows = bullscows( ask("Введите слово: ", words), w)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        if bulls == len(w):
            break
        attempts += 1
    return attempts

def ask(prompt: str, valid: list[str] = None):
    w = input(prompt)
    if valid:
        while True:
            if w in valid:
                break
            w = input(prompt)
    return w

def inform(format_string: str, bulls: int, cows: int):
    print(format_string.format(bulls, cows))
