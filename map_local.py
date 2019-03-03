import pygame
import sys

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
test_local = 39
pygame.init()
screen_size = (1080, 680)  # 第一个是宽度，第二个是高度
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("大富翁")
map_screen = pygame.image.load('image/地图.bmp')
map_screen = pygame.transform.scale(map_screen, screen_size)
screen.blit(map_screen, (0, 0))
role = pygame.image.load('image/role/小e.jpg')
role_size = (60, 60)
role = pygame.transform.scale(role, role_size)
screen.blit(role, map_coordi[test_local])
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
