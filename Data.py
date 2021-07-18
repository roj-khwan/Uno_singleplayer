import random
from typing import Counter

Color = ['Red', 'Blue', 'Green', 'Yellow']
Number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Special = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', 'skip']
Wild = ['Color Wild', 'Draw +4 Wild']

def Cards(Normal):
    if Normal:
        return random.choice(Number) + ' ' + random.choice(Color)
    else:
        if bool(random.choice((0, 1))):
            return random.choice(Wild)
        else:
            return random.choice(Special) + ' ' + random.choice(Color)