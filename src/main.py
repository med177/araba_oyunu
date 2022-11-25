import sys
import pygame
import random
from pygame.locals import *

# %%


class Game:
    def __init__(self):
        self.running = False
        self.stop = True
        self.displaySurface = None
        self.size = self.width, self.height = 400, 700
        self.font = None
        self.scoreText = "Başlamak için bir yukarı ok tuşuna basın"
        self.myCarOnRight = True
        self.speedLevel = 1
        self.counter = 0
        self.life = 3
        self.info = f"Kalan Hakkın: {self.life} Seviye: {float(self.speedLevel):.2f}"

    def on_init(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 16)
        self.displaySurface = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Zeyd'in Araba Oyunu")
        self.displaySurface.fill((115, 185, 96))

        playerImg = pygame.image.load("src/img/player.png")
        myCarImg = pygame.image.load("src/img/car.png")
        otherCarImg = pygame.image.load("src/img/car2.png")

        self.player = self.setImg(playerImg, 1)
        self.playerLoc = self.player.get_rect()
        self.playerLoc.center = (52, 52)

        self.myCar = self.setImg(myCarImg, 3)
        self.myCarLoc = self.myCar.get_rect()
        self.myCarLoc.center = (
            self.width//2+self.myCarLoc.width-15, self.height-100)

        self.otherCar = self.setImg(otherCarImg, 3)
        self.otherCarLoc = self.otherCar.get_rect()
        self.leftLane = self.width//2-(self.otherCarLoc.width-15)
        self.rightLane = self.width//2+(self.otherCarLoc.width-15)
        self.otherCarLoc.center = (self.leftLane, 50)

        self.running = True

    def on_loop(self):
        frameWeight = 3

        road = pygame.draw.rect(self.displaySurface, (0, 0, 0),
                                (100, frameWeight, self.width-200, self.height-frameWeight*2))
        line = pygame.draw.rect(self.displaySurface, (255, 255, 255),
                                ((self.width-10)//2, frameWeight, 10, self.height-frameWeight*2))
        for i in range(20):
            pygame.draw.rect(self.displaySurface, (0, 0, 0),
                             ((self.width-10)//2, frameWeight+i*50, 10, 15))

        if self.life == 0:
            self.scoreText = "Oyun Bitti"

        if self.stop == False:
            self.counter += 1
            if self.counter == 3000:
                self.counter = 0
                self.speedLevel += 0.1
                self.scoreText = self.info

            if self.myCarLoc.colliderect(self.otherCarLoc):
                self.life -= 1
                self.scoreText = f"Kalan Hakkın: {self.life} devam etmek için bir yukarı ok tuşuna basın"
                self.otherCarLoc[1] = -self.otherCarLoc[3]
                self.stop = True

            self.otherCarLoc[1] += self.speedLevel
            if self.otherCarLoc[1] > self.height:
                if random.randint(0, 1) == 0:
                    self.otherCarLoc.center = (self.leftLane, 50)
                else:
                    self.otherCarLoc.center = (self.rightLane, 50)

                self.otherCarLoc[1] = -self.otherCarLoc[3]

            # araçları göster
            self.displaySurface.blit(self.myCar, self.myCarLoc)
            self.displaySurface.blit(self.otherCar, self.otherCarLoc)
            self.displaySurface.blit(self.player, self.playerLoc)

        frame = pygame.draw.rect(self.displaySurface, (39, 98, 22),
                                 (0, 0, self.width, self.height), frameWeight)
        score = pygame.draw.rect(self.displaySurface,
                                 (39, 98, 22), (0, self.height-20, self.width, 20))
        scoreText = self.font.render(self.scoreText, False, (197, 221, 190))
        self.displaySurface.blit(
            scoreText, ((self.width-scoreText.get_width())//2, self.height-19))

        playerArea = pygame.draw.circle(self.displaySurface, (0, 0, 0),
                                        self.playerLoc.center, 50-frameWeight+2, frameWeight+2)
        playerText = self.font.render(
            "Sürücü Zeyd", False, (255, 255, 255))
        self.displaySurface.blit(
            playerText, (10, 100))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_UP:
                if self.stop == True and self.life > 0:
                    self.stop = False
                    self.scoreText = self.info
                else:
                    self.stop = True
                    self.scoreText = f"Oyun Durduruldu"

            elif event.key == pygame.K_LEFT and self.myCarOnRight:
                self.myCarLoc = self.myCarLoc.move(
                    [-(self.myCarLoc.width+35), 0])
                self.myCarOnRight = False
            elif event.key == pygame.K_RIGHT and not self.myCarOnRight:
                self.myCarLoc = self.myCarLoc.move(
                    [(self.myCarLoc.width+35), 0])
                self.myCarOnRight = True

    def setImg(self, img: pygame.Surface, rate: float = 2):
        scaledImg = pygame.transform.scale(
            img, (img.get_width()/rate, img.get_height()/rate))
        return scaledImg

    def on_render(self):
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()


Game().on_execute()
