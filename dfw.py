import pygame
import sys
from draw import *
from game import *
from player import Player


pygame.init()

screen_size = (1080, 680)  # 第一个是宽度，第二个是高度
role_size = (60, 60)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("大富翁")

map_screen = pygame.image.load('地图.bmp')
picture_dice = []
for i in range(6):
    picture_dice.append = pygame.image.load('dice/%d.jpg'%(i+1))

map_screen = pygame.transform.scale(map_screen, screen_size)

screen.blit(map_screen, (0, 0))

play_button = Button(screen, '开始游戏')  # 绘制开始游戏按钮
play_button.draw_button()

status = 0  #控制游戏进程 0：游戏未开始 1：掷骰子 2：触发事件
cur_player = 0  #当前玩家
player = []
role = []
fps = 300

role_init = [(116, 8), (915, 611), (1015, 85), (8, 542)]
role_score = [(150, 100), (350, 100), (150, 350), (350, 350)]
money_center = [(180, 180), (380, 180), (180, 430), (380, 430)]
gpa_center = [(180, 220), (380, 220), (180, 470), (380, 470)]

while True:
    if status == 0:  # 游戏未开始
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = event.pos
                print(mouse_x, mouse_y)
                if click_button(mouse_x, mouse_y):
                    #print('ISbutton ok')
                    num_player_button = Button(screen, '请输入游戏人数（2~4）')
                    num_player_button.draw_button()
                    status = 1
        pygame.display.update()
    elif status == 1:  # 选择游戏人数
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if 258 <= event.key <= 260:
                    role.append(pygame.image.load('role/小e.jpg'))
                    role.append(pygame.image.load('role/皮卡丘.jpg'))
                    if event.key >= 259:
                        role.append(pygame.image.load('role/可达鸭.jpg'))
                        if event.key == 260:
                            role.append(pygame.image.load('role/小黄鸡.jpg'))
                screen.blit(map_screen, (0, 0))
                for i in range(len(role)): # 绘制角色头像
                    role[i] = pygame.transform.scale(role[i], role_size)
                    screen.blit(role[i], role_init[i])
                    screen.blit(role[i], role_score[i])
                    player.append(Player())
                for i in range(len(role)):
                    draw_text(screen, money_center[i], 'money:%d'%player[i].money, 20)
                    draw_text(screen, gpa_center[i], 'gpa:%.1f'%player[i].gpa, 20)
                status = 2
        #fclock_tick(fps)
        for i in range(6):
            screen.blit()
            pygame.display.update()
    elif status == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dice_answer = get_dice()
                draw_walk(cur_player, dice_answer)
                if Special(player[cur_player]):
                    status = 3
        pygame.display.update()
    elif status == 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                chances = get_chances()
        pygame.display.update()
