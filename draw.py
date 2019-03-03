import pygame.font

class Button:  # 按钮类
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width = 200
        self.height = 50
        self.button_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        # self.font = pygame.font.SysFont('宋体' , 48)
        self.font = pygame.font.Font('STXINGKA.TTF', 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

def draw_text(screen, center, text, text_size, font_type, bg_color):  # 绘制文本
    text_color = (255, 0, 0)
    bg_color.a = 0
    font = pygame.font.Font(font_type, text_size)
    textSurface = font.render(text, True, text_color, bg_color)
    textRect = textSurface.get_rect()
    textRect.center = center
    screen.blit(textSurface, textRect)

#role_init = [(116, 8), (915, 611), (1015, 85), (8, 542)]
role_score = [(150, 100), (350, 100), (150, 350), (350, 350)]
money_center = [(180, 180), (380, 180), (180, 430), (380, 430)]
gpa_center = [(180, 220), (380, 220), (180, 470), (380, 470)]
map_coordi = [(116, 8), (190, 8), (264, 8), (338, 8), (412, 8),
              (510, 8),
              (619, 8), (693, 8), (767, 8), (841, 8), (915, 8),
              (1015, 8),
              (1015, 85), (1015, 160), (1015, 235),
              (1015, 310),
              (1015, 390), (1015, 465), (1015, 540),
              (1015, 611),
              (915, 611), (841, 611), (767, 611), (693, 611), (619, 611),
              (510, 611),
              (408, 611), (334, 611), (260, 611), (186, 611), (112, 611),
              (8, 611),
              (8, 542), (8,468), (8,394),
              (8, 310),
              (8, 233), (8, 159), (8, 85),
              (8, 8)]

def draw_player(screen, player, role):  # 绘制玩家头像和分数
    for i in range(len(player)):
        screen.blit(role[i], map_coordi[player[i].local])
        screen.blit(role[i], role_score[i])
        draw_text(screen, money_center[i], 'money:%d' % player[i].money, 20, 'BASKVILL.TTF', pygame.Color('gold'))
        draw_text(screen, gpa_center[i], 'gpa:%.1f' % player[i].gpa, 20, 'BASKVILL.TTF', pygame.Color('gold'))

def draw_mapstatus(screen, player, map_status):  # 画某块地被谁买了
    for i in range(len(map_status)):
        if map_status[i].level == 0:
            draw_text(screen, map_status[i].text_local,
                      '￥%d' % map_status[i].value1, 30, 'STXINGKA.TTF', pygame.Color('violet'))
        elif map_status[i].level == 1:
            draw_text(screen, map_status[i].text_local,
                      '%s*' % player[map_status[i].owner].name, 30, 'STXINGKA.TTF', pygame.Color('violet'))
        elif map_status[i].level == 2:
            draw_text(screen, map_status[i].text_local,
                      '%s**' % player[map_status[i].owner].name, 30, 'STXINGKA.TTF', pygame.Color('violet'))