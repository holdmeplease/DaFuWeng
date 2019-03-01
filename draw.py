import pygame.font


class Button:
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()  # 引入整个大屏幕的参数
        self.width = 200
        self.height = 50
        self.button_color = (255, 0, 0)
        self.text_color = (255, 255, 255)  # 设置参数，在下面会调用，都是简单的数据类型而已。
        # self.font = pygame.font.SysFont('宋体' , 48)  # None是字体类型，48是字体大小
        self.font = pygame.font.Font('STXINGKA.TTF', 48)  # None是字体类型，48是字体大小
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # 设置矩形大小
        self.rect.center = self.screen_rect.center  # 将矩形放到屏幕中间
        self.prep_msg(msg)

    def prep_msg(self, msg):
        # 要打印的字符串，是否抗锯齿，字体颜色，矩形颜色
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()  # 不解释
        self.msg_image_rect.center = self.rect.center  # 将该矩形放到中间去

    def draw_button(self):  # 绘制的时候调用该函数
        self.screen.fill(self.button_color, self.rect)  # 绘制出一个矩形作为背景
        self.screen.blit(self.msg_image,self.msg_image_rect)  # 在一个矩形中绘制出文本信息


def draw_walk(cur_player, dice_answer):
    print(cur_player)
    print(dice_answer)

def draw_text(screen, center, text, text_size):
    text_color = (255, 0, 0)
    bg_color = pygame.Color('gold')
    bg_color.a = 1
    font = pygame.font.Font('BASKVILL.TTF', text_size)  # 通过字体文件获得字体对象
    textSurface = font.render(text, True, text_color, bg_color)  # 配置要显示的文字
    textRect = textSurface.get_rect()  # 获得要显示的对象的rect
    textRect.center = center  # 设置显示对象的坐标
    screen.blit(textSurface, textRect)  # 绘制字体