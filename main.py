from typing import Counter
from Data import Cards as Cd, Color, Number
from random import choice
import time

Player_Cards = []
Bot_Cards = []
now_Card = 0
plus = 0
enemy = {'Player_Cards':'Bot_Cards', 'Bot_Cards':'Player_Cards'}
enemy_turn = {'player()':'bot()', 'bot()':'player()'}

def checkwin(turn : str):
    if (len(eval(turn)) == 0):
        print("{} Win !!!".format(turn.split('_')[0]))
        input("Enter any Button to Quit : ")
        quit()

def ChangeColour(input_colour):
    if input_colour[0].lower() == 'r':
        output_colour = 'Red'
    if input_colour[0].lower() == 'b':
        output_colour = 'Blue'
    if input_colour[0].lower() == 'g':
        output_colour = 'Green'
    if input_colour[0].lower() == 'y':
        output_colour = 'Yellow'
    return output_colour

def SeparateCard(card : str, turn_card : str, turn : str, color : str):
    global plus
    global now_Card
    global Bot_Cards
    global Player_Cards
    plus = 0
    color_card = card.split()[-1]
    cmd = card.split()[0]
    #check is card wild
    if color_card != 'Wild':
        #check is card +2
        if cmd == '+2':
                plus += 2
                for i in range(plus):
                    plus_card = Cd(False)
                    eval(enemy[turn_card]+'.append(plus_card)')
                checkwin(turn_card)
                now_Card = card
                eval(turn)
        #check is card skip
        elif cmd == 'skip':
            checkwin(turn_card)
            now_Card = card
            eval(turn)
        #card that can be in this else will be normal number card
        else:
            now_Card = card
            checkwin(turn_card)
            eval(enemy_turn[turn])
    else:
        #check is card Draw +4
        if cmd == 'Draw':
            plus += 4
            for i in range(plus):
                plus_card = Cd(False)
                eval(enemy[turn_card]+'.append(plus_card)')
            now_Card = color
            checkwin(turn_card)
            eval(turn)
        #check is card color
        elif cmd == 'Color':
            now_Card = color
            checkwin(turn_card)
            eval(enemy_turn[turn])

def player():
    print('\033[038;2;200;200;0m__Player Turn__\033[0;0m')
    global Player_Cards
    while True:
        color = set(i.split()[-1] for i in Player_Cards)
        cmd = set(i.split()[0] for i in Player_Cards)
        #show the cards in hand
        print('-Bot have-')
        print(len(Bot_Cards), 'Cards')
        print("-You have-")
        print(len(Player_Cards), 'Cards')
        for j, i in enumerate(Player_Cards):
            print('{}) {}'.format(j, i))
            time.sleep(0.1)
        print('Now Card :', now_Card)
        print('You Have Color :', '/'.join(Counter(color).keys()))
        print('You Have Command :', '/'.join(Counter(cmd).keys()))
        #route player can choose
        if (now_Card.split()[-1] in color or now_Card.split()[0] in cmd or 'Wild' in color):
            play = input('Which Card will you Play? : ')
            try:
                #check Index Out of range
                if int(play) > len(Player_Cards)-1:
                    print("\033[038;2;255;77;64mIndex out of range\033[0;0m")
                    continue
            except:pass
            #check draw
            if play[0].lower() == 'd':
                Player_Cards.append(Cd(False))
                break
            #check exit
            elif play[0].lower() == 'e':
                quit()
            #turn play into integer to index the card
            else: play = Player_Cards[int(play)]
            play_color = play.split()[-1]
            play_cmd = play.split()[0]
            #check is play card can play
            if (play_color == 'Wild' or 'Wild' == now_Card.split()[-1] or play_color == now_Card.split()[-1] or play_cmd == now_Card.split()[0]):
                Player_Cards.remove(play)
                if (play_color == 'Wild'):
                    choose_color = ChangeColour(input('Which Color Do you want?(red/blue/green/yellow) : '))
                else:
                    choose_color = 'Wild'
                play = SeparateCard(play, 'Player_Cards', 'player()', choose_color)
                checkwin('Player_Cards')
            else:
                print("Choose card that have the same number of color as now card or choose wild card")
                continue
        #draw when no card
        elif (now_Card.split()[-1] not in color or now_Card.split()[0] not in cmd or 'Wild' not in color):
            print('\033[038;2;200;200;0mYou Don\'t have anycard to play Here!!\033[0;0m')
            Player_Cards.append(Cd(False))
            break

def bot():
    checkwin('Bot_Cards')
    print('\033[038;2;200;200;0m__Bot Turn__\033[0;0m')
    global Bot_Cards
    color = list(set(i.split()[-1] for i in Bot_Cards))
    cmd = set(i.split()[0] for i in Bot_Cards)
    number = [i for i in Bot_Cards if i.split()[0] in Number]
    Choose_color = now_Card.split()[-1]
    print('-Bot have-')
    print(len(Bot_Cards), 'Cards')
    print("-You have-")
    print(len(Player_Cards), 'Cards')
    for j, i in enumerate(Bot_Cards):
        print('{}) {}'.format(j, i))
        time.sleep(0.1)
    print('Now Card :', now_Card)
    if ('Draw +4 Wild' in Bot_Cards):
        print('Wild Draw Card Route')
        play = 'Draw +4 Wild'
        color = [i for i in color if i in Color]
        if color == []:
            Choose_color = choice(Color)
        else:pass
        print(Counter(color))
        Choose_color = max(Counter(color))
    elif ('Color Wild' in Bot_Cards) and (now_Card.split()[-1] not in color):
        print('Wild Color Card Route')
        play = 'Color Wild'
        color = [i for i in color if i in Color]
        if color == []:
            Choose_color = choice(Color)
        else:
            print(Counter(color))
            Choose_color = max(Counter(color))
    elif ('+2' in cmd)and ([i for i in Bot_Cards if i.split()[0] == '+2' and i.split()[-1] == now_Card.split()[-1]] != []):
        print('+2 Route')
        card = [i for i in Bot_Cards if i.split()[0] == '+2' and i.split()[-1] == now_Card.split()[-1]]
        play = choice(card)
        print(card)
    elif any(i.split()[0] == now_Card.split()[0] for i in number):
        print('Number Card Route')
        number_only = [i for i in number if i.split()[0] == now_Card.split()[0]]
        play = choice(number_only)
    elif any(i.split()[-1] == now_Card.split()[-1] for i in number):
        print('Color Card Route')
        number_only = [i for i in number if i.split()[-1] == now_Card.split()[-1]]
        print(number_only)
        play = choice(number_only)
    elif ('skip' in cmd)and ([i for i in Bot_Cards if i.split()[0] == 'skip' and i.split()[-1] == now_Card.split()[-1]] != []):
        print('Skip Route')
        card = [i for i in Bot_Cards if i.split()[0] == 'skip' and i.split()[-1] == now_Card.split()[-1]]
        play = choice(card)
        print(card)
    else:
        Bot_Cards.append(Cd(False))
        play = False
    if isinstance(play, bool):
        pass
    else:
        Bot_Cards.remove(play)
        print('Bot Play :', play)
        SeparateCard(play, 'Bot_Cards', 'bot()', Choose_color)
        checkwin('Bot_Cards')



def main():
    global Player_Cards
    global Bot_Cards
    global now_Card
    n = 5
    Player_Cards = [Cd(False) for i in range(n)]
    Bot_Cards = [Cd(False) for i in range(n)]
    now_Card = Cd(True)
    print('Player - 0\nBot - 1')
    first = int(input('Who Do You Want To Play First? : '))
    play = list(enemy_turn.keys())
    eval(play[first])

if __name__ == '__main__':
    main()