
class Player:  # 玩家类
    def __init__(self, order):
        self.money = 3000
        self.gpa = 3.0
        self.local = 0
        self.stop = 0
        if order == 0:
            self.name = '小E'
        elif order == 1:
            self.name = '皮卡丘'
        elif order == 2:
            self.name = '可达鸭'
        elif order == 3:
            self.name = '小黄鸡'

