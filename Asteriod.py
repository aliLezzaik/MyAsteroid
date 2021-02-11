import pygame
import math
import random
import time


class Stone:
    def __init__(self):
        self.image = pygame.image.load("img/spaceParts_082.png")
        self.x = random.randint(0, 1024)
        self.y = random.randint(0, 768)
        self.image = pygame.transform.scale(self.image, (random.randint(1, 40), random.randint(1, 40)))
        self.should_be_destroyed = False
        self.xspeed = random.randint(-90, 90) * 0.1
        self.yspeed = random.randint(-90, 90) * 0.1

    def update(self, player):
        if self.x > 1024 or self.x < 0 or self.y < 0 or self.y > 768:
            self.should_be_destroyed = True
        self.x += self.xspeed
        self.y += self.yspeed
        self.should_be_destroyed = self.collided_with_player(player)
        if self.should_be_destroyed:
            exit(0)

    def collided_with_player(self, player):
        if player.x <= self.x <= player.x + player.image.get_rect().width:
            if player.y <= self.y <= player.y + player.image.get_rect().height:
                return True
        # if player.x >= self.x and player.x+player.image.get_rect().width <= self.x + self.image.get_rect().width:
        #     if player.y >= self.y and player.y+player.image.get_rect().height <= self.y + self.image.get_rect().height:
        #         print("Collided")
        #         return True
        return False

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.image.load("img/spaceParts_082.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.should_be_destroyed = False
        self.velx = math.cos(math.radians(self.angle)) * 10
        self.vely = -math.sin(math.radians(self.angle)) * 10

    def collided_with_stones(self, stones: []):
        for s in stones:
            print(1)
            if self.x <= s.x <= self.x + self.image.get_rect().width:
                if self.y <= s.y <= self.y + self.image.get_rect().height:
                    print("Shot")
                    self.should_be_destroyed = True
                    s.should_be_destroyed = True

    def update(self,stones):
        self.x += self.velx
        self.y += self.vely
        self.collided_with_stones(stones)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.image = pygame.image.load("img/spaceShips_005.png")
        self.velx = 0
        self.vely = 0
        self.anglevel = 0
        self.bullets = []

    def __left_key(self):
        self.anglevel = -5

    def __right_key(self):
        self.anglevel = 5

    def __up_key(self):
        self.velx = math.cos(math.radians(self.angle)) * 5
        # self.x += math.cos(self.angle)
        self.vely = -math.sin(math.radians(self.angle)) * 5
        # self.y += math.sin(self.angle)

    def __space(self):
        self.bullets.append(Bullet(self.x+10, self.y+10, self.angle))

    def update(self, stones):
        self.x += self.velx
        self.y += self.vely
        self.angle += self.anglevel
        if self.x + self.image.get_rect().width < 0:
            self.x = 1024
        if self.x > 1024:
            self.x = -self.image.get_rect().width
        if self.y > 768:
            self.y = 0
        if self.y + self.image.get_rect().height < 0:
            self.y = 768
        for b in self.bullets:
            b.update(stones)
            if b.should_be_destroyed:
                self.bullets.remove(b)


    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.__up_key()
            if event.key == pygame.K_LEFT:
                self.__left_key()
            if event.key == pygame.K_RIGHT:
                self.__right_key()
            if event.key == pygame.K_SPACE:
                self.__space()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.vely = 0
                self.velx = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.anglevel = 0


    def render(self, screen):
        new_image = pygame.transform.rotate(self.image, self.angle - 90)
        # self.image = pygame.transform.rotate(self.image, self.angle)
        # self.image = new_image
        self.image.get_rect().center = new_image.get_rect().center
        screen.blit(new_image, (self.x, self.y))
        for b in self.bullets:
            b.render(screen)


def main():
    screen = pygame.display.set_mode([1024, 768])
    clock = pygame.time.Clock()
    running = True
    screen.fill((0, 0, 0))
    player = Player(10, 10)
    stones = []
    for i in range(2):
        stones.append(Stone())
    initial = time.time()
    print(initial)
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            player.handle(e)
        player.update(stones)
        now = time.time()
        # print(now)
        if now - initial > 4:
            stones.append(Stone())
            initial = now
        for s in stones:
            if s.should_be_destroyed:
                stones.remove(s)
            s.update(player)
        screen.fill((0, 0, 0))
        for s in stones:
            s.render(screen)
        player.render(screen)
        pygame.display.update()
        clock.tick(40)


if __name__ == '__main__':
    main()
