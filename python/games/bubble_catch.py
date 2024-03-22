import pygame
import random
import time

pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("bubble catch!")
pygame.display.set_icon(pygame.image.load("assets\\bubble.png"))
clock = pygame.time.Clock()
font = pygame.font.Font("assets\\fonts\\chewy\\Chewy-Regular.ttf", 60)
black = pygame.Color(0,0,0)
start_img = pygame.image.load("assets\\bubble_catch_start.png")

class Vals:
    drops = []
    score = 0
    mode = "start"
    lives = 3
    prev_score = 0
    buttons = []

class Droppable:
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=(random.randint(30,570), random.randint(-75,-25)))
        self.id = random.randint(100000,999999)
        self.v = 0.05
        self.count = 0
    def update(self, bowl):
        self.rect.y += self.v
        self.v += 0.005
        if self.rect.colliderect(bowl.rect):
            pygame.mixer.music.load("assets\\sounds\\pop.mp3")
            self.image = pygame.image.load("assets\\popped_bubble.png")
            self.draw()
            self.count += 1
            if self.count > 2:
                Vals.score += 1
                pygame.mixer.music.play(1)
                for id, _ in enumerate(Vals.drops):
                    if _.id == self.id:
                        Vals.drops.pop(id)
        if self.rect.y > 600:
            pygame.mixer.music.load("assets\\sounds\\Crunch.mp3")
            pygame.mixer.music.set_volume(5.0)
            pygame.mixer.music.play()
            Vals.lives -= 1
            for id, _ in enumerate(Vals.drops):
                if _.id == self.id:
                    Vals.drops.pop(id)
    def draw(self):
        screen.blit(self.image, self.rect)

def show_lives():
    if Vals.lives >= 0:
        src = f"assets\\lives_png\\{Vals.lives}.png"
        img = pygame.image.load(src)
        r = img.get_rect(center=(60,50))
        screen.blit(img, r)

        if Vals.lives == 0:
            Vals.lives -= 1
    else:
        time.sleep(2)
        Vals.mode = "gameover"
        Vals.prev_score = Vals.score
        Vals.score = 0
        Vals.drops = []
        Vals.lives = 3
        

hand = pygame.image.load("assets\\hand.png")
class Bowl:
    def __init__(self):
        self.rect = hand.get_rect(center=(300,568))

def draw_text(txt: str, fontsize: int, center: tuple[int, int] = (300, 300), colour=black):
    the_font = pygame.font.Font("assets\\fonts\\chewy\\Chewy-Regular.ttf", fontsize)
    the_text = the_font.render(txt, True, colour)
    textRect = the_text.get_rect()
    textRect.center = center
    screen.blit(the_text, textRect)

class Button:
    def __init__(self, text, color: pygame.Color, w, h, x, y):
        self.text = text
        self.color = color
        self.rect = pygame.Rect(x, y, w, h)
        self.hovered = False
    def ishovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def draw(self):
        if self.hovered == False:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
            draw_text(self.text, self.rect.height // 2, self.rect.center, pygame.Color(255,255,255))
        else:
            hovered_color = pygame.Color(self.color.r + 10, self.color.g + 10, self.color.b)
            pygame.draw.rect(screen, hovered_color, self.rect, border_radius=10)
            draw_text(self.text, self.rect.height // 2, self.rect.center, pygame.Color(255,255,255))
bowl = Bowl()

running = True
while running:
    if Vals.mode == "game":
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bowl.rect.x = mouse_x - 50
        screen.fill(pygame.Color(255,255,255))
        screen.blit(hand, bowl.rect)
        for droppable in Vals.drops:
            droppable.draw()
            droppable.update(bowl)
        draw_text(str(Vals.score), 60, (300, 100))
        show_lives()
        pygame.display.flip()
        clock.tick(60)
        if random.randint(1,100) == 1:
            Vals.drops.append(Droppable("assets\\bubble.png"))
    if Vals.mode == "start":
        screen.blit(start_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for id, v in enumerate(Vals.buttons):
                    if v.ishovered() == True:
                        if id == 0:
                            Vals.mode = "game"
                            Vals.score = 0
                            Vals.drops = []
                            Vals.buttons = []
                            Vals.lives = 3
                        if id == 1:
                            running = False
        draw_text("Bubble Catch!", 80, (300, 100))
        Vals.buttons = [
            Button("start", pygame.Color(153, 204, 255), 250, 50, 175, 200),
            Button("quit", pygame.Color(153, 204, 255), 250, 50, 175, 275)
        ]
        for button in Vals.buttons:
            _ = button.ishovered()
            button.draw()
        pygame.display.flip()
        clock.tick(60)
    if Vals.mode == "gameover":
        screen.fill(pygame.Color(255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Vals.score = 0
                    Vals.mode = "game"
        draw_text(str(Vals.prev_score), 100, (300, 350))
        draw_text("Good Job!", 120, (300, 100))
        draw_text("your score:", 36, (300, 180))
        draw_text("press space to try again...", 36, (300, 500))
        pygame.display.flip()
        clock.tick(60)
pygame.quit()