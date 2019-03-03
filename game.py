import random


class Map:  # 记录地产信息
    def __init__(self, order):
        if order == 2 or order == 3 or order == 6 or order == 7:
            self.value1 = 300
            self.rent1 = 30
            self.value2 = 600
            self.rent2 = 60
        else:
            self.value1 = 500
            self.rent1 = 50
            self.value2 = 1000
            self.rent2 = 100
        self.owner = -1
        self.level = 0
        if order == 0:
            self.text_local = (290, 100)
        elif order == 1:
            self.text_local = (800, 100)
        elif order == 2:
            self.text_local = (940, 200)
        elif order == 3:
            self.text_local = (940, 500)
        elif order == 4:
            self.text_local = (790, 580)
        elif order == 5:
            self.text_local = (285, 580)
        elif order == 6:
            self.text_local = (138, 500)
        elif order == 7:
            self.text_local = (138, 265)

def get_dice():
    return random.randint(1, 6)

def Special(pos):
    if pos == 5 or pos == 11 or pos == 15 or pos == 19 or pos == 25 or pos == 31 or pos == 35 or pos == 39:
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

def full_somewhere(num_local, player):
    flag = 0
    for i in range(len(player)):
        if player[i].local == num_local:
            flag = 1
    if flag == 0:
        return True
    else:
        return False

def local2order(local):
    if 0 <= local < 5:
        return 0
    elif 6 <= local < 11:
        return 1
    elif 12 <= local < 15:
        return 2
    elif 16 <= local < 19:
        return 3
    elif 20 <= local < 25:
        return 4
    elif 26 <= local < 31:
        return 5
    elif 32 <= local < 35:
        return 6
    elif 36 <= local < 39:
        return 7

def game_over(player):  # 判断游戏是否结束
    for i in range(len(player)):
        if player[i].money < 0 or player[i].gpa < 1.0:
            return - (i + 1)
        if player[i].gpa > 4.0:
            return i + 1
    return 0