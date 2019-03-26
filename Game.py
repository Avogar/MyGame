import pygame,random, sys
pygame.init()

class direction():
    right = 1
    left = 2
    straight_r = 3
    straight_l = 4

class figure:
    def __init__(self,x,y,dx,dy,color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
    def draw(self):
        if self.color == brown:
            screen.blit(image_brick,[self.x,self.y])
        elif self.color == yellow:
            screen.blit(image_coin,[self.x,self.y])
        else:
            pygame.draw.rect(screen,self.color,[self.x,self.y,self.dx,self.dy],0)
    def ishit(self,main):
        if main.x < self.x + self.dx and main.x + main.dx  > self.x and main.y < self.y + self.dy and main.y + main.dy > self.y:
            return True
        return False

class character(figure):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.dx = 15
        self.d = 5
        self.dy = 50
        self.speed_x = 2
        self.speed_y = 0
        self.jump = False
        self.fall = False
        self.create = False
        self.create_k = 0
        self.destroy = False
        self.color = red
        self.direction = direction.straight_r
        self.move_count = 1
        self.collect_coins = 0
        self.t = 1
        self.floor = []
    def f(self):
        return int(7 * self.t - 0.25 * self.t ** 2)
    def move(self):
        if self.direction == direction.right:
            self.move_count += 0.2
            self.x += self.speed_x
        if self.direction == direction.left:
            self.x -= self.speed_x
            self.move_count += 0.2
        if self.move_count >= 5:
            self.move_count = 1
        if self.floor == [] or self.x > self.floor.x + self.floor.dx or self.x + self.dx < self.floor.x:
            self.floor = []
            if not(self.jump):
                self.t = 13
                self.speed_y = self.f()
                self.t += 1
                self.jump = True
        if self.jump:
            self.y += self.speed_y
            self.speed_y =  self.f()
            self.y -= self.speed_y
            self.t += 1
            if self.floor != [] and self.y >= self.floor.y - self.dy:
                self.jump = False
                self.y = self.floor.y - self.dy
                self.speed_y = 0
                self.t = 1
    def new_block(self):
        y = self.y + self.dy // self.create_k
        if self.direction == direction.right or self.direction == direction.straight_r:
            x = self.x + self.dx
        else:
            x = self.x - self.dx - 2*self.d
        self.create = False
        return [x, y, self.dx + 2*self.d, self.dy//2, brown]
    def key_down(self,key):
        if key == pygame.K_RIGHT:
            self.direction = direction.right
        elif key == pygame.K_LEFT:
            self.direction = direction.left
        if key == pygame.K_SPACE:
            self.jump = True
        if key == pygame.K_q:
            self.create = True
            self.create_k = 2
        if key == pygame.K_w:
            self.create = True
            self.create_k = 1
        if key == pygame.K_e:
            self.destroy = True
    def key_up(self,key):
        if key == pygame.K_LEFT and self.direction == direction.left:
            self.direction = direction.straight_l
            self.move_count = 1
        elif key == pygame.K_RIGHT and self.direction == direction.right:
            self.direction = direction.straight_r
            self.move_count = 1
    def draw(self):
        draw_x = self.x - self.d
        if self.jump:
            if self.direction == direction.right or self.direction == direction.straight_r:
                screen.blit(image_jump_r,[draw_x, self.y])
            else:
                screen.blit(image_jump_l,[draw_x, self.y])
        elif self.direction == direction.straight_l:
            screen.blit(image_stay_l,[draw_x,self.y])
        elif self.direction == direction.straight_r:
            screen.blit(image_stay_r,[draw_x,self.y])
        elif self.direction == direction.right:
            if 1 <= self.move_count < 2:
                screen.blit(image_run1_r,[draw_x,self.y])
            elif 2 <= self.move_count < 3:
                screen.blit(image_run2_r,[draw_x,self.y])
            elif 3 <= self.move_count < 4:
                screen.blit(image_run3_r,[draw_x,self.y])
            elif 4 <= self.move_count < 5:
                screen.blit(image_run4_r,[draw_x,self.y])
        elif self.direction == direction.left:
            if 1 <= self.move_count < 2:
                screen.blit(image_run1_l,[draw_x,self.y])
            elif 2 <= self.move_count < 3:
                screen.blit(image_run2_l,[draw_x,self.y])
            elif 3 <= self.move_count < 4:
                screen.blit(image_run3_l,[draw_x,self.y])
            elif 4 <= self.move_count < 5:
                screen.blit(image_run4_l,[draw_x,self.y])
    def get_next_pos(self):
        pers = character(self.x, self.y)
        pers.direction, pers.jump, pers.t, pers.floor, pers.speed_y = self.direction, self.jump, self.t, self.floor, self.speed_y
        pers.move()
        return  pers
    def ishit(self,block):
        if block.ishit(self.get_next_pos()):
            if block.color == yellow:
                all_blocks.destroy(block)
                self.collect_coins += 1
            else:
                if self.y + self.dy <= block.y:
                    self.floor = block
                elif self.x >= block.x + block.dx:
                    self.direction = direction.straight_l
                elif self.x + self.dx <= block.x:
                    self.direction = direction.straight_r
                elif self.y >= block.y + block.dy:
                    self.t += (14 - self.t) * 2 - 1
                    self.speed_y = self.f()
                    self.t += 1
                else:
                    if self.direction == direction.right or self.direction == direction.straight_r:
                        self.x = block.x - self.dx
                    else:
                        self.x = block.x + block.dx
            return True
        return False

class blocks:
    def __init__(self):
        self.list = []
    def draw(self):
        for i in self.list:
            i.draw()
    def ishit(self,block):
        for i in self.list:
            if block.ishit(i):
                return True
    def destroy(self,block):
        self.list.remove(block)
        return False

def create_coins():
    block_points = figure(10,10,size[0]-20,30,black)
    all_blocks.list.append(block_points)
    def create_coin():
        coin_d = 15
        x = random.randrange(size[0] - coin_d + 1)
        y = random.randrange(size[1] - coin_d + 1)
        coin = figure(x, y, coin_d,coin_d, yellow)
        return coin
    for i in range(coins_n):
        coin = create_coin()
        while all_blocks.ishit(coin):
            coin = create_coin()
        all_blocks.list.append(coin)
    all_blocks.list.remove(block_points)

def create_all_blocks():
    y = (size[1] - (size[1]//120 - 2)*120)//2
    dy = 10
    dx = 80
    for i in range(size[1]//120 - 1):
        n = random.randrange(3, 5)
        for j in range(n):
            x = random.randrange(j * size[0] // n + 3, (j + 1) * size[0] // n - dx)
            elem = figure(x, y, dx, dy, black)
            all_blocks.list.append(elem)
        y += 120



def create_block(mas):
    brick = figure(mas[0],mas[1],mas[2],mas[3],mas[4])
    if not(all_blocks.ishit(brick)):
        all_blocks.list.append(brick)

def destroy_block():
    for item in all_blocks.list:
        if item.color == brown and 0 <= item.y - pers.y <= pers.dy // 2 + 10 and (
                0 <= item.x - pers.x - pers.dx <= 1 or - 1 <= item.x + item.dx - pers.x <= 0):
            all_blocks.destroy(item)
            break

def draw_fon():
    screen.blit(image_fon,[0,0])

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
yellow = (255,255,0)
sky = (200,255,255)
grey = (190,190,190)
orange = (255,165,0)
brown = (139,69,19)
purple = (160,32,240)
DarkGreen = (0,128,0)

trip = sys.path[0]

image_fon = pygame.image.load(trip + '/data/fon.png')

image_run1_r = pygame.image.load(trip + '/data/run1r.png')
image_run1_r.set_colorkey(white)
image_run2_r = pygame.image.load(trip + '/data/run2r.png')
image_run2_r.set_colorkey(white)
image_run3_r = pygame.image.load(trip + '/data/run3r.png')
image_run3_r.set_colorkey(white)
image_run4_r = pygame.image.load(trip + '/data/run4r.png')
image_run4_r.set_colorkey(white)
image_stay_r = pygame.image.load(trip + '/data/stayr.png')
image_stay_r.set_colorkey(white)
image_jump_r = pygame.image.load(trip + '/data/jumpr.png')
image_jump_r.set_colorkey(white)

image_run1_l = pygame.image.load(trip + '/data/run1l.png')
image_run1_l.set_colorkey(white)
image_run2_l = pygame.image.load(trip + '/data/run2l.png')
image_run2_l.set_colorkey(white)
image_run3_l = pygame.image.load(trip + '/data/run3l.png')
image_run3_l.set_colorkey(white)
image_run4_l = pygame.image.load(trip + '/data/run4l.png')
image_run4_l.set_colorkey(white)
image_stay_l = pygame.image.load(trip + '/data/stayl.png')
image_stay_l.set_colorkey(white)
image_jump_l = pygame.image.load(trip + '/data/jumpl.png')
image_jump_l.set_colorkey(white)

image_coin = pygame.image.load(trip + '/data/coin.png')
image_coin.set_colorkey(white)

image_brick = pygame.image.load(trip + '/data/brick.png')

size = [700,700]
block_d = 10
screen = pygame.display.set_mode(size)
pygame.display.set_caption('New Game')

clock = pygame.time.Clock()
done2 = True
while done2:
    all_blocks = blocks()
    all_blocks.list = [figure(0,size[1]-3,size[0],block_d,black),figure(0,-7,size[0],block_d,black),figure(-7,0,block_d,size[1],black),figure(size[0]-3,0,block_d,size[1],black)]
    create_all_blocks()
    pers = character(100,520)
    coins_n = random.randrange(30, 50)
    create_coins()
    done = True
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
                done2 = False
            if event.type == pygame.KEYDOWN:
                pers.key_down(event.key)
            if event.type == pygame.KEYUP:
                pers.key_up(event.key)

        if pers.collect_coins == coins_n:
            done = False
        if pers.destroy:
            destroy_block()
            pers.destroy = False
        if pers.create:
            create_block(pers.new_block())
        all_blocks.ishit(pers)
        pers.move()

        screen.fill(sky)
        all_blocks.draw()
        pers.draw()
        pygame.display.flip()

        clock.tick(60)
pygame.quit()