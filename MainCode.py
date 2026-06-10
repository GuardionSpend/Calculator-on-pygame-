import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 400, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Калькулятор")
clock = pygame.time.Clock()

BG = (30, 30, 30)
DISPLAY_BG = (45, 45, 45)
TEXT = (255, 255, 255)
NUM_BTN = (60, 60, 60)
OP_BTN = (255, 150, 50)
EQ_BTN = (50, 150, 255)
CLR_BTN = (220, 60, 60)

font_btn = pygame.font.SysFont('Arial', 32, bold=True)
font_disp = pygame.font.SysFont('Arial', 44, bold=True)

current_expr = "0"
prev_num = None
op = None
new_num_started = True
error = None

class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover = False

    def draw(self, surface):
        col = tuple(min(ch + 25, 255) for ch in self.color) if self.hover else self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=8)
        txt = font_btn.render(self.text, True, TEXT)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

btns = []
w, h = 80, 70
gap = 10
sx, sy = 20, 130

btns.append(Button(sx, sy, w*4 + gap*3, h, "C", CLR_BTN))

layout = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '+', '=']
]
for r, row in enumerate(layout):
    for c, txt in enumerate(row):
        x = sx + c * (w + gap)
        y = sy + (r + 1) * (h + gap)
        if txt in '+-*/': col = OP_BTN
        elif txt == '=': col = EQ_BTN
        else: col = NUM_BTN
        btns.append(Button(x, y, w, h, txt, col))

def calculate():
    global current_expr, prev_num, op, new_num_started, error
    if prev_num is None or op is None or current_expr == "":
        return
    try:
        curr = float(current_expr)
        if op == '+': res = prev_num + curr
        elif op == '-': res = prev_num - curr
        elif op == '*': res = prev_num * curr
        elif op == '/':
            if curr == 0:
                error = "На 0 не делят, гений"
                return
            res = prev_num / curr
        res = round(res, 10)
        current_expr = str(res)
        if current_expr.endswith('.0'):
            current_expr = current_expr[:-2]
        prev_num = res
        op = None
        new_num_started = True
        error = None
    except Exception:
        error = "Error"

running = True
while running:
    screen.fill(BG)

    disp_rect = pygame.Rect(10, 10, WIDTH - 20, 100)
    pygame.draw.rect(screen, DISPLAY_BG, disp_rect, border_radius=10)
    display_text = error if error else (current_expr if current_expr != "" else "0")
    surf = font_disp.render(display_text, True, TEXT)
    tx_rect = surf.get_rect(right=disp_rect.right - 15, centery=disp_rect.centery)
    screen.blit(surf, tx_rect)

    mouse_pos = pygame.mouse.get_pos()
    for b in btns:
        b.hover = b.rect.collidepoint(mouse_pos)
        b.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = None
            for b in btns:
                if b.rect.collidepoint(event.pos):
                    clicked = b.text
                    break
            if not clicked:
                continue

            if error and clicked != 'C':
                current_expr = "0"; prev_num = None; op = None; new_num_started = True; error = None

            if clicked == 'C':
                current_expr = "0"; prev_num = None; op = None; new_num_started = True; error = None
            elif clicked in '0123456789.':
                if new_num_started or current_expr == "0":
                    if clicked == '.':
                        current_expr = "0."
                    else:
                        current_expr = clicked
                    new_num_started = False
                elif clicked == '.':
                    if '.' not in current_expr:
                        current_expr += '.'
                else:
                    current_expr += clicked
            elif clicked in '+-*/':
                if not new_num_started:
                    if prev_num is not None and op is not None:
                        calculate()
                    else:
                        prev_num = float(current_expr)
                    op = clicked
                    new_num_started = True
            elif clicked == '=':
                calculate()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

