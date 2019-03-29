import pygame
import sys
import time

from draw import Button, draw_text, draw_mapstatus, draw_player
from game import *
from player import Player


pygame.init()

screen_size = (1080, 680)  # 第一个是宽度，第二个是高度
role_size = (60, 60)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("大富翁——清华之旅")
map_screen = pygame.image.load('image/地图.bmp')
stop_picture = pygame.image.load('image/禁止.jpg')
stop_picture = pygame.transform.scale(stop_picture, (20, 20))

lose_sound = pygame.mixer.Sound('sound/失败.wav')  # 载入音效
win_sound = pygame.mixer.Sound('sound/胜利.wav')
up_sound = pygame.mixer.Sound('sound/升级.wav')
click_sound = pygame.mixer.Sound('sound/按键.wav')
chances_sound = pygame.mixer.Sound('sound/事件.wav')

picture_dice = []
for i in range(6):
    picture_dice.append(pygame.image.load('image/dice/%d.jpg'%(i+1)))

map_screen = pygame.transform.scale(map_screen, screen_size)

screen.blit(map_screen, (0, 0))

play_button = Button(screen, '开始游戏')  # 绘制开始游戏按钮
play_button.draw_button()

status = 0  # 控制游戏进程 0：游戏未开始 1：选择游戏人数 2：掷骰子 3：玩家行走 4：触发事件 5：买地建房 6：游戏结束
cur_player = 0  # 当前玩家
dice_answer = 1 # 掷骰子结果
player = []
role = []

local_init = [0, 20, 12, 32]  # 四位玩家最初的位置
map_status = []
for i in range(8):
    map_status.append(Map(i))  # 存储地产信息，包括所有者、价值、租金等

while True:
    if status == 0:  # 游戏未开始
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = event.pos
                #print(mouse_x, mouse_y)
                if click_button(mouse_x, mouse_y, 0):
                    click_sound.play()
                    num_player_button = Button(screen, '请输入游戏人数（2~4）')
                    num_player_button.draw_button()
                    draw_text(screen, (540, 440), '操作指南：按↑掷骰子、购买地产',
                              50, 'STXINGKA.TTF', pygame.Color('gold'))
                    status = 1
        pygame.display.update()
    elif status == 1:  # 选择游戏人数
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if 258 <= event.key <= 260 or 50 <= event.key <= 52: #载入相应数量的角色
                    click_sound.play()
                    role.append(pygame.image.load('image/role/小e.jpg'))
                    role.append(pygame.image.load('image/role/皮卡丘.jpg'))
                    if event.key == 259 or event.key == 51:
                        role.append(pygame.image.load('image/role/可达鸭.jpg'))
                    elif event.key == 260 or event.key == 52:
                        role.append(pygame.image.load('image/role/可达鸭.jpg'))
                        role.append(pygame.image.load('image/role/小黄鸡.jpg'))
                    screen.blit(map_screen, (0, 0))
                    for i in range(len(role)): #初始化游戏玩家
                        role[i] = pygame.transform.scale(role[i], role_size)
                        player.append(Player(i))
                        player[i].local = local_init[i]
                    draw_player(screen, player, role, stop_picture)
                    status = 2
    elif status == 2: #掷骰子
        for i in range(6):  # 绘制骰子动画
            screen.blit(picture_dice[i], (500, 400))
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 273:
                    dice_answer = get_dice()
                    status = 3
        pygame.display.update()
    elif status == 3: #玩家行走
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for i in range(dice_answer):
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            player[cur_player].local = (player[cur_player].local + 1) % 40
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            click_sound.play()
            pygame.display.update()
            time.sleep(0.5)
        if Special(player[cur_player].local): #判断是否触发特殊事件
            status = 4
        else:  # 普通地段，判断需要买地或交租金
            local = player[cur_player].local
            if map_status[local2order(local)].owner == -1:
                chances_sound.play()
                draw_text(screen, (800, 340), '是否买下这块地?（￥%d）' % map_status[local2order(local)].value1, 30,
                          'STXINGKA.TTF', pygame.Color('grey'))
                status = 5
            elif map_status[local2order(local)].owner == cur_player and map_status[local2order(local)].level == 1:
                chances_sound.play()
                draw_text(screen, (800, 340), '是否要加盖建筑?（￥%d）' % map_status[local2order(local)].value2, 30,
                          'STXINGKA.TTF', pygame.Color('grey'))
                status = 5
            elif map_status[local2order(local)].owner == cur_player and map_status[local2order(local)].level == 2:
                cur_player = (cur_player + 1) % len(player)  # 下一个玩家掷骰子
                while player[cur_player].stop == 1:
                    player[cur_player].stop = 0
                    cur_player = (cur_player + 1) % len(player)
                status = 2
            else:
                if map_status[local2order(local)].level == 1:
                    player[cur_player].money -= map_status[local2order(local)].rent1
                    player[map_status[local2order(local)].owner].money += map_status[local2order(local)].rent1
                    screen.blit(map_screen, (0, 0))
                    screen.blit(picture_dice[dice_answer - 1], (500, 400))
                    draw_mapstatus(screen, player, map_status)
                    draw_player(screen, player, role, stop_picture)
                    draw_text(screen, (800, 340), '支付租金（￥%d）' % map_status[local2order(local)].rent1, 30,
                              'STXINGKA.TTF', pygame.Color('grey'))
                    chances_sound.play()
                elif map_status[local2order(local)].level == 2:
                    player[cur_player].money -= map_status[local2order(local)].rent2
                    player[map_status[local2order(local)].owner].money += map_status[local2order(local)].rent2
                    screen.blit(map_screen, (0, 0))
                    screen.blit(picture_dice[dice_answer - 1], (500, 400))
                    draw_mapstatus(screen, player, map_status)
                    draw_player(screen, player, role, stop_picture)
                    draw_text(screen, (800, 340), '支付租金（￥%d）' % map_status[local2order(local)].rent2, 30,
                              'STXINGKA.TTF', pygame.Color('grey'))
                    chances_sound.play()
                cur_player = (cur_player + 1) % len(player)  # 下一个玩家掷骰子
                while player[cur_player].stop == 1:
                    player[cur_player].stop = 0
                    cur_player = (cur_player + 1) % len(player)
                if not game_over(player) == 0:
                    if game_over(player) > 0:
                        win_sound.play()
                    else:
                        lose_sound.play()
                    status = 6
                else:
                    status = 2
            pygame.display.update()
    elif status == 4: #触发特殊事件
        if player[cur_player].local == 5: #C楼
            player[cur_player].money -= 100
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (800, 340), '去C楼购物，金钱-100', 30, 'STXINGKA.TTF', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 11: #紫操
            player[cur_player].money += 100
            if full_somewhere(35, player):
                player[cur_player].gpa += 0.2
                screen.blit(map_screen, (0, 0))
                screen.blit(picture_dice[dice_answer - 1], (500, 400))
                draw_mapstatus(screen, player, map_status)
                draw_player(screen, player, role, stop_picture)
                draw_text(screen, (800, 340), '坚持紫操夜跑，绩点+0.2', 30, 'STXINGKA.TTF', pygame.Color('grey'))
                chances_sound.play()
            else:
                player[cur_player].local = 35
                player[cur_player].stop = 1
                screen.blit(map_screen, (0, 0))
                screen.blit(picture_dice[dice_answer - 1], (500, 400))
                draw_mapstatus(screen, player, map_status)
                draw_player(screen, player, role, stop_picture)
                draw_text(screen, (800, 340), '紫操踢球受伤住院', 30, 'STXINGKA.TTF', pygame.Color('grey'))
                chances_sound.play()
        elif player[cur_player].local == 15: #罗姆楼
            if cur_player == 0:
                player[0].stop = 1
                player[0].gpa += 0.2
                screen.blit(map_screen, (0, 0))
                screen.blit(picture_dice[dice_answer - 1], (500, 400))
                draw_mapstatus(screen, player, map_status)
                draw_player(screen, player, role, stop_picture)
                draw_text(screen, (750, 340), '小E在系馆学习一天，绩点+0.2', 30, 'STXINGKA.TTF', pygame.Color('grey'))
                chances_sound.play()
        elif player[cur_player].local == 19: #主楼
            player[cur_player].gpa += 0.3
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (750, 340), '观看特将答辩受到鼓舞，绩点+0.3', 30, 'STXINGKA.TTF', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 25: #新清
            player[cur_player].money -= 200
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (800, 340), '去新清看演出，金钱-200', 30, 'STXINGKA.TTF', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 31: #二校门
            player[cur_player].money += 500
            player[cur_player].gpa -= 1.0
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (750, 340), '找到校外实习，金钱+500，绩点-1.0', 30, 'STXINGKA.TTF', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 35: #校医院
            player[cur_player].stop = 1
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (800, 340), '住院一天', 30, 'STXINGKA.TTF', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 39: #图书馆
            if not cur_player == 2:
                player[cur_player].stop = 1
                player[cur_player].gpa += 0.2
                screen.blit(map_screen, (0, 0))
                screen.blit(picture_dice[dice_answer - 1], (500, 400))
                draw_mapstatus(screen, player, map_status)
                draw_player(screen, player, role, stop_picture)
                draw_text(screen, (800, 340), '泡在图书馆一天，绩点+0.2', 30, 'STXINGKA.TTF', pygame.Color('grey'))
                chances_sound.play()
        cur_player = (cur_player + 1) % len(player) #下一个玩家掷骰子
        while player[cur_player].stop == 1:
            player[cur_player].stop = 0
            cur_player = (cur_player + 1) % len(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        if not game_over(player) == 0:
            if game_over(player) > 0:
                win_sound.play()
            else:
                lose_sound.play()
            status = 6
        else:
            status = 2
    elif status == 5: #买地建房
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 273:
                    if map_status[local2order(player[cur_player].local)].level == 0:
                        player[cur_player].money -= map_status[local2order(player[cur_player].local)].value1
                        map_status[local2order(player[cur_player].local)].owner = cur_player
                        map_status[local2order(player[cur_player].local)].level = 1
                    elif map_status[local2order(player[cur_player].local)].level == 1:
                        player[cur_player].money -= map_status[local2order(player[cur_player].local)].value2
                        map_status[local2order(player[cur_player].local)].level = 2
                cur_player = (cur_player + 1) % len(player)  # 下一个玩家掷骰子
                while player[cur_player].stop == 1:
                    player[cur_player].stop = 0
                    cur_player = (cur_player + 1) % len(player)
                status = 2
                screen.blit(map_screen, (0, 0))
                screen.blit(picture_dice[dice_answer - 1], (500, 400))
                draw_player(screen, player, role, stop_picture)
                draw_mapstatus(screen, player, map_status)
                up_sound.play()
                if not game_over(player) == 0:
                    if game_over(player) > 0:
                        win_sound.play()
                    else:
                        lose_sound.play()
                    status = 6
        pygame.display.update()
    elif status == 6:  # 游戏结束
        if game_over(player) > 0:
            draw_text(screen, (540, 340), '游戏结束，%s胜利' % player[game_over(player)-1].name,
                      50, 'STXINGKA.TTF', pygame.Color('darkgreen'))
            draw_text(screen, (540, 440), '再来一局',
                      50, 'STXINGKA.TTF', pygame.Color('darkgreen'))

        else :
            draw_text(screen, (540, 340), '游戏结束，%s失败' % player[- game_over(player) - 1].name,
                      50, 'STXINGKA.TTF', pygame.Color('darkgreen'))
            draw_text(screen, (540, 440), '再来一局',
                      50, 'STXINGKA.TTF', pygame.Color('darkgreen'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = event.pos
                if click_button(mouse_x, mouse_y, 1):
                    player = []
                    role = []
                    map_status = []
                    for i in range(8):
                        map_status.append(Map(i))
                    cur_player = 0
                    click_sound.play()
                    screen.blit(map_screen, (0, 0))
                    num_player_button = Button(screen, '请输入游戏人数（2~4）')
                    num_player_button.draw_button()
                    draw_text(screen, (540, 440), '操作指南：按↑掷骰子、购买地产',
                              50, 'STXINGKA.TTF', pygame.Color('gold'))
                    status = 1
        pygame.display.update()

