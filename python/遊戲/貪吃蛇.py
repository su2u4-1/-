import pygame
from random import randint as ri

# 設定pygame
pygame.init()
pygame.display.set_caption("貪吃蛇")
W = pygame.display.Info().current_w
H = pygame.display.Info().current_h
W = round(W / 10) - 1
H = round(H / 10) - 3
screen = pygame.display.set_mode((W * 10, H * 10), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

# 設定變數
gameRun = True
score = 0
snake = [[1, 1], [1, 2], [1, 3]]
tail = [1, 0]
dire = (0, 0)
color = []
apple = []
for i in range(W):
    a = []
    for j in range(H):
        a.append(ri(150, 200))
    color.append(a)

# 主迴圈
while True:
    # 事件處理迴圈
    for event in pygame.event.get():
        # 如果視窗被關掉就關閉pygame與程式
        if event.type == pygame.QUIT:
            pygame.quit()
            # 印出分數
            print("score:", score)
            exit()
        # 如果鍵盤被按下
        if event.type == pygame.KEYDOWN:
            match event.key:
                # w鍵或上鍵
                case pygame.K_w | pygame.K_UP:
                    dire = (0, -1)
                # a鍵或左鍵
                case pygame.K_a | pygame.K_LEFT:
                    dire = (-1, 0)
                # s鍵或下鍵
                case pygame.K_s | pygame.K_DOWN:
                    dire = (0, 1)
                # d鍵或右鍵
                case pygame.K_d | pygame.K_RIGHT:
                    dire = (1, 0)
                # b鍵
                case pygame.K_b:
                    dire = (0, 0)
                # esc鍵
                case pygame.K_ESCAPE:
                    pygame.quit()
                    print("score:", score)
                    exit()

    # 如果方向不是停且遊戲執行中
    if dire != (0, 0) and gameRun:
        # 從頭部往移動方向延伸一格
        head = snake[-1].copy()
        head[0] += dire[0]
        head[1] += dire[1]
        snake.append(head)
        # 去掉尾巴一格
        tail = snake.pop(0)

    # 如果有蘋果被蛇碰到了
    for i in apple:
        if i in snake and gameRun:
            # 分數加一
            score += 1
            # 尾巴長出一格
            snake = [tail] + snake
            # 移除蘋果
            apple.remove(i)
            break

    # 如果蘋果數量未到上限就新增蘋果
    if len(apple) <= (W * H / 500) - (len(snake) / 10) and gameRun:
        a = [ri(0, W - 1), ri(0, H - 1)]
        if a not in snake and a not in apple and (a[0] > 15 or a[1] > 1):
            apple.append(a)

    # 如果蛇撞到自己或撞到邊緣就停止遊戲
    if snake[-1] in snake[:-1]:
        gameRun = False
    if snake[-1][0] < 0 or snake[-1][0] >= W or snake[-1][1] < 0 or snake[-1][1] >= H:
        gameRun = False

    # 清除畫面
    screen.fill((0, 0, 0))
    # 畫地板
    for i in range(W):
        for j in range(H):
            pygame.draw.rect(screen, (50, color[i][j], 0), (i * 10 + 1, j * 10 + 1, 8, 8))
    # 畫蘋果
    for i in apple:
        pygame.draw.rect(screen, (200, 0, 0), (i[0] * 10 + 1, i[1] * 10 + 1, 8, 8))
    # 畫蛇
    for i in snake:
        if i == snake[-1]:
            pygame.draw.rect(screen, (0, 0, 0), (i[0] * 10 + 1, i[1] * 10 + 1, 8, 8))
        else:
            pygame.draw.rect(screen, (color[i[0]][i[1]], color[i[0]][i[1]], 0), (i[0] * 10 + 1, i[1] * 10 + 1, 8, 8))
    # 顯示文字
    screen.blit(font.render(f"score:{score},apple:{len(apple)}", True, (255, 255, 255), (0, 0, 0)), (0, 0))
    # 如果遊戲結束就顯示分數
    if not gameRun:
        screen.blit(font.render("GAMEOVER", True, (255, 0, 0), (255, 255, 255)), (W / 2 * 10 - 40, H / 2 * 10 - 40))
        screen.blit(font.render(f"score:{score}", True, (255, 0, 0), (255, 255, 255)), (W / 2 * 10 - 40, H / 2 * 10 - 20))

    # 更新畫面
    pygame.display.update()
    clock.tick(10)
