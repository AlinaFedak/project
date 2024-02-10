from pygame import *
from random import *

class Car(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_dx=4, player_dy=0, color=(255, 0, 0)): #dx=4, dy=0
        ().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_dx = player_dx
        self.player_dy = player_dy
        self.size_x = size_x
        self.size_y =  size_y
        self.color = color
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def fill(self):
        draw.rect(window, self.color, self.rect)

    # def load_image(self, img):
    #     self.image = image.load(img).convert()
    #     self.image.set_colorkey((0,0,0))

    # def draw_image(self):
    #     window.blit(self.image, [self.x, self.y])

    def move_x(self):
        self.rect.x += self.player_dx

    def move_y(self):
        self.rect.y += self.player_dy

    # def draw_rect(self):
    #     draw.rect(window, self.color, [self.x, self.y, self.width, self.height], 0)

    def check_out_of_window(self):
        if self.rect.x+self.size_x > 400 or self.rect.x < 0:
            self.rect.x -= self.player_dx


def check_collision(player_x, player_y, player_width, player_height, car_x, car_y, car_width, car_height):
    if (player_x+player_width > car_x) and (player_x < car_x+car_width) and (player_y < car_y+car_height) and (player_y+player_height > car_y):
        return True
    else:
        return False

win_width, win_height = 400, 700
size = (400, 700)
window = display.set_mode(size)
display.set_caption("Ride the Road")

finish = False

clock = time.Clock()
FPS = 60

player = Car('player.png', 175, 475, 70, 131)#, 0, 0 (255, 0, 0))

collision = True

score = 0

font.init()
font_40 = font.Font(None, 40)
font_30 = font.Font(None, 30)
text_title = font_40.render("Ride the Road", True, (250, 105, 10))
text_ins = font_30.render("Click to Play!", True, (250, 105, 10))


def draw_main_menu():
    window.blit(text_title, [win_width / 2 - 106, win_height / 2 - 100])
    score_text = font_40.render("Score: " + str(score), True, (250, 105, 10))
    window.blit(score_text, [win_width / 2 - 70, win_height / 2 - 30])
    window.blit(text_ins, [win_width / 2 - 85, win_height / 2 + 40])
    display.flip()

cars = []
car_count = 2
for i in range(car_count):
    x = randint(0, 341)
    car = Car('car_pic.png',x, randint(-150, -51), 60, 60, 0, randint(5, 11), (181, 230, 29))
    cars.append(car)

stripes = []
stripe_count = 20
stripe_x = 185
stripe_y = -10
stripe_width = 20
stripe_height = 80
space = 20
for i in range(stripe_count):
    stripes.append([190, stripe_y])
    stripe_y += stripe_height + space

while not finish:
    for e in event.get():
        if e.type == QUIT:
            finish = True

        if collision:
            collision = False
            for i in range(car_count):
                cars[i].rect.y = randint(-150, -51)
                cars[i].rect.x = randint(0, 351)
            player.rect.x = 175
            player.dx = 0
            score = 0
            # mouse.set_visible(False)

        if not collision:
            keys_pressed = key.get_pressed()
            if keys_pressed[K_RIGHT] and player.rect.x < win_width-70:
                player.rect.x += 4
                # player.dx = 4
            elif keys_pressed[K_LEFT] and player.rect.x > 0:
                player.rect.x -= 4
                # player.dx = -4

            # if event.key == K_LEFT:
            #     player.dx = 0
            # elif event.key == K_RIGHT:
            #     player.dx = 0

    window.fill((159, 163, 168))

    if not collision:
        for i in range(stripe_count):
            draw.rect(window, (255, 255, 255), [stripes[i][0], stripes[i][1], stripe_width, stripe_height])
        for i in range(stripe_count):
            stripes[i][1] += 3
            if stripes[i][1] > win_height:
                stripes[i][1] = -40 - stripe_height

        player.reset()
        # player.move_x()
        player.check_out_of_window()

        for i in range(car_count):
            cars[i].fill()
            cars[i].rect.y += cars[i].player_dy
            if cars[i].rect.y > win_height:
                score += 10
                cars[i].rect.y = randint(-150, -51)
                cars[i].rect.x = randint(0, 341)
                cars[i].player_dy = randint(4, 10)

        for i in range(car_count):
            if check_collision(player.rect.x, player.rect.y, player.size_x, player.size_y, cars[i].rect.x, cars[i].rect.y, cars[i].size_x, cars[i].size_y):
                collision = True
                # mouse.set_visible(True)
                break

        txt_score = font_30.render("Score: "+str(score), True, (255,255, 255))
        window.blit(txt_score, [15, 15])

        display.flip()
    else:
        draw_main_menu()

    clock.tick(60)

quit()
