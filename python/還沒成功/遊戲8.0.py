import pygame
from random import randint as ri
from math import floor as fl

pygame.init()
W_change = pygame.display.Info().current_w
H_change = pygame.display.Info().current_h
W, H = 1000, 700
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("遊戲8.0")
clock = pygame.time.Clock()
textlink = "C:\\Windows\\Fonts\\kaiu.ttf"
font = pygame.font.Font(textlink, 20)
b = [ri(0, 255), ri(0, 255), ri(0, 255)]
input_flag = False
fullscreen = 0
inputbox = False
do_something = None


class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.range = (x, y, x + w, y + h)
        self.color = (0, 0, 100)
        self.text = text
        self.txt_surface = pygame.font.Font(textlink, 20).render(text, True, self.color)
        self.active = False

    def handle_mouse(self, x, y, sx, sy):
        if (
            self.range[0] <= x - sx <= self.range[2]
            and self.range[1] <= y - sy <= self.range[3]
        ):
            self.active = not self.active
        else:
            self.active = False
        self.color = (0, 0, 200) if self.active else (0, 0, 100)

    def handle_keydown(self, event):
        global input_text, input_flag
        if self.active:
            if event.key == pygame.K_RETURN:
                input_text = self.text
                input_flag = True
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = pygame.font.Font(textlink, 20).render(
                self.text, True, self.color
            )

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Button:
    def __init__(
        self,
        x,
        y,
        w,
        h,
        text,
        holddown,
        surface,
        do="print(f'button {self.text} is pressed')",
    ):
        self.original_x = x
        self.original_y = y
        self.original_w = w
        self.original_h = h
        self.x_ = self.original_x
        self.y_ = self.original_y
        self.w_ = self.original_w
        self.h_ = self.original_h
        self.text = text
        self.do_something = do
        self.scaling = 0.9
        self.text_color1 = (100, 100, 100)
        self.text_color2 = (200, 200, 200)
        self.button_color = (20, 20, 20)
        self.frame_color = (200, 200, 200)
        self.frame_ = False
        self.text_color_ = self.text_color1
        self.time = 0
        self.holddown = holddown
        self.text_size_original = 20
        self.text_size_ = self.text_size_original
        self.surface = surface

    def check(self, mx, my, start_x, start_y):
        global do_something
        if (
            start_x + self.x_ <= mx <= start_x + self.x_ + self.w_
            and start_y + self.y_ <= my <= start_y + self.y_ + self.h_
            and surface_dict[surface_list[-1]] == self.surface
        ):
            self.text_color_ = self.text_color2
            self.frame_ = True
            if pygame.mouse.get_pressed()[0] and self.time <= 10:
                self.x_ = self.original_x + self.original_w * 0.05
                self.y_ = self.original_y + self.original_h * 0.05
                self.w_ = self.original_w * 0.9
                self.h_ = self.original_h * 0.9
                self.text_size_ = 18
                if self.time <= 0:
                    do_something = (self, self.do_something)
                    if self.holddown:
                        self.time = 20
                if not self.holddown:
                    self.time = 10
            else:
                self.x_ = self.original_x
                self.y_ = self.original_y
                self.w_ = self.original_w
                self.h_ = self.original_h
                self.text_size_ = self.text_size_original
        else:
            self.text_color_ = self.text_color1
            self.frame_ = False
            self.x_ = self.original_x
            self.y_ = self.original_y
            self.w_ = self.original_w
            self.h_ = self.original_h
            self.text_size_ = self.text_size_original

    def display(self):
        pygame.draw.rect(
            self.surface.surface,
            self.button_color,
            (self.x_, self.y_, self.w_, self.h_),
        )
        if self.frame_:
            pygame.draw.rect(
                self.surface.surface,
                self.frame_color,
                (self.x_, self.y_, self.w_, self.h_),
                5,
            )
        text = pygame.font.Font(textlink, self.text_size_).render(
            self.text, True, self.text_color_
        )
        self.surface.surface.blit(
            text,
            text.get_rect(
                center=(fl(self.x_ + self.w_ / 2), fl(self.y_ + self.h_ / 2))
            ),
        )

    def do(self, do_something):
        try:
            exec(do_something)
        except:
            print(do_something)
            exit()


class Surface:
    def __init__(self, name, w, h, object=[]):
        self.name = name
        self.w = w
        self.h = h
        self.object = object
        self.surface = pygame.Surface((w, h)).convert_alpha()

    def display(self):
        self.surface.fill((104, 104, 130, 200))
        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, self.w, self.h), 5)
        for i in self.object:
            i.check(mx, my, W / 2 - self.w / 2, H / 2 - self.h / 2)
            i.display()
        screen.blit(self.surface, (W / 2 - self.w / 2, H / 2 - self.h / 2))


def back_ground_color(w, h):
    back_ground = []
    for _ in range(fl(w / 10)):
        a = []
        for _ in range(fl(h / 10)):
            a.append((b[0], b[1], b[2]))
            b[ri(0, 2)] += ri(-1, 1)
            for i in range(3):
                b[i] = b[i] if b[i] < 255 else 255
                b[i] = b[i] if b[i] > 0 else 0
        back_ground.append(a)
    return back_ground


def add_surface(surface_name):
    f = True
    match surface_name:
        case "Start":
            surface = Surface(surface_name, 400, 240)
            surface.object.append(
                Button(
                    50,
                    50,
                    100,
                    40,
                    "開新遊戲",
                    False,
                    surface,
                    "print(f'button {self.text} is pressed')\nadd_surface('CreateCharacter')",
                )
            )
            surface.object.append(
                Button(
                    250,
                    50,
                    100,
                    40,
                    "開啟舊檔",
                    False,
                    surface,
                    "print(f'button {self.text} is pressed')",
                )
            )
            surface.object.append(
                Button(
                    50,
                    150,
                    100,
                    40,
                    "儲存遊戲",
                    False,
                    surface,
                    "print(f'button {self.text} is pressed')",
                )
            )
            surface.object.append(
                Button(
                    250,
                    150,
                    100,
                    40,
                    "離開遊戲",
                    False,
                    surface,
                    "print(f'button {self.text} is pressed')\nadd_surface('LeaveTheGameConfirmation')",
                )
            )
        case "LeaveTheGameConfirmation":
            surface = Surface(surface_name, 400, 140)
            surface.object.append(
                Button(
                    50,
                    50,
                    100,
                    40,
                    "確認",
                    False,
                    surface,
                    "print(f'button {self.text} is pressed')\npygame.quit()\nexit()",
                )
            )
            surface.object.append(
                Button(
                    250,
                    50,
                    100,
                    40,
                    "取消",
                    False,
                    surface,
                    "print(f'button {self.text} is pressed')\nremove_surface('LeaveTheGameConfirmation')",
                )
            )
        case "CreateCharacter":  #
            surface = Surface(surface_name, 400, 300)
            surface.object.append(
                Button(
                    50,
                    50,
                    100,
                    40,
                    "確認",
                    False,
                    surface,
                    "print(f'button {self.text} is pressed')\nadd_surface('InitialAttributes')\nremove_surface('CreateCharacter')\nremove_surface('Start')",
                )
            )
            surface.object.append(
                Button(
                    250,
                    50,
                    100,
                    40,
                    "取消",
                    False,
                    surface,
                    "print(f'button {self.text} is pressed')\nremove_surface('CreateCharacter')",
                )
            )
        case _:
            print("這個功能尚未製作完成")
            f = False
    if f:
        surface_dict[surface_name] = surface
        surface_list.append(surface_name)


def remove_surface(surface_name):
    surface_list.remove(surface_name)
    del surface_dict[surface_name]


input_box = InputBox(0, 0, 300, 40, "請輸入名字")
back_ground = back_ground_color(W, H)
surface_dict = {}
surface_list = []
add_surface("Start")

while True:
    mx, my = pygame.mouse.get_pos()
    for j in surface_list:
        for i in surface_dict[j].object:
            if i.time > 0:
                i.time -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if inputbox:
                input_box.handle_keydown(event)
                inputbox = False
            if event.key == pygame.K_F11:
                fullscreen += 1
                if fullscreen % 2 == 1:
                    W = W_change
                    H = H_change
                    screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
                    back_ground = back_ground_color(W, H)
                else:
                    W, H = 1000, 700
                    screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
                    back_ground = back_ground_color(W, H)
        elif event.type == pygame.MOUSEBUTTONUP:
            if do_something is not None:
                do_something[0].do(do_something[1])
                do_something = None
            if inputbox:
                input_box.handle_mouse(mx, my, sx, sy)
                inputbox = False
                sx, sy = 0, 0

    screen.fill((0, 0, 0))
    for x in range(fl(W / 10)):
        for y in range(fl(H / 10)):
            pygame.draw.rect(screen, back_ground[x][y], (x * 10, y * 10, 10, 10), 0)
    screen.blit(font.render(f"{mx},{my}", True, (0, 0, 0)), [0, 0])

    for i in surface_list:
        surface_dict[i].display()
    pygame.display.update()
    clock.tick(100)

"""
開始:Start
建角色:CreateCharacter
初始屬性:InitialAttributes
基地:Base
倉庫:Warehouse
合成:Synthesis
角色:Character
地圖:Map
設定:Settings
背包:Inventory
訓練:Training
屬性:Attributes
技能:Skills
裝備介面:EquipmentInterface
物品介面:ItemInterface
合成介面:SynthesisInterface
怪物:Monsters
資源:Resources
強化:Enhancement
附魔:Enchantment
鑲嵌:Socketing
鍛造:Forging
離開遊戲確認:LeaveTheGameConfirmation
"""
