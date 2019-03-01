import random


def get_dice():
    return random.randint(1, 6)

def Special(pos):
    if pos == 5:
        return True
    else:
        return False

def get_chances():
    chances_list = ['得到', '失去']
    return chances_list[random.randint(0, len(chances_list) - 1)]

def click_button(pos_x, pos_y):
    if 440 <= pos_x <= 640 and 315 <= pos_y <= 365:
        #print('true')
        return True
    else:
        #print('false')
        return False