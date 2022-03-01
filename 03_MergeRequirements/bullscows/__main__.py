from bullscows import gameplay, ask, inform
import urllib.request
import sys
from . import *


if len(sys.argv) < 2:
    quit()
elif len(sys.argv) == 2:
    arg_len = 5
else:
    arg_len = sys.argv[2]

try:
    with open(sys.argv[1]) as url:
        my_dict = url.read().split('\n')
except FileNotFoundError:
    print("FileNotFoundError")
    pass

try:
    dct = urllib.request.urlopen(sys.argv[1])
    my_dict = dct.read().decode('utf-8').split('\n')
except ValueError:
    print("ValueError")
    pass
if words:
    words = my_dict.split()
    words = list(filter(lambda x: len(x) == arg_len, words))
    print("Number of attempts: ", gameplay(ask, inform, words))

