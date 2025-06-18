# Implementation of the Display class

#pygame
import pygame

class Display():
    def __init__(self):
        self.SCALE = 10
        self.WIDTH = 64
        self.HEIGHT = 32
        self.FPS = 60
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WIDTH*self.SCALE, self.HEIGHT*self.SCALE))
        pygame.display.set_caption('My CHIP8 Emulator')
        self.clock = pygame.time.Clock()
        self.pixels = [[0 for x in range(self.HEIGHT)] for y in range(self.WIDTH)]

    def clearScreen(self):
        #this go through each pixel and change it's value from 1(On) to 0(Off)
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                self.pixels[x][y] = 0

    def draw_pixel(self, x, y, value=1):
        # XOR to pixel's value, like CHIP-8 does
        self.pixels[x][y] ^= value
        return not self.pixels[x][y]  # return True if the pixel was turn off

    def render(self):
        #this renders the screen, and makes the scale works
        self.SCREEN.fill("black")  # Background black

        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                if self.pixels[x][y]:
                    rect = pygame.Rect(x * self.SCALE, y * self.SCALE, self.SCALE, self.SCALE) # draws a rectangle because we need the scale
                    pygame.draw.rect(self.SCREEN, (255, 255, 255), rect)

        pygame.display.update()

    def drawMyName(self):
        # Letra A (empezando en 5,5)
        self.draw_pixel(6, 5)
        self.draw_pixel(7, 5)

        self.draw_pixel(5, 6)
        self.draw_pixel(8, 6)

        self.draw_pixel(5, 7)
        self.draw_pixel(6, 7)
        self.draw_pixel(7, 7)
        self.draw_pixel(8, 7)

        self.draw_pixel(5, 8)
        self.draw_pixel(8, 8)

        self.draw_pixel(5, 9)
        self.draw_pixel(8, 9)

        # Letra L (empezando en 10,5)
        self.draw_pixel(10, 5)
        self.draw_pixel(10, 6)
        self.draw_pixel(10, 7)
        self.draw_pixel(10, 8)
        self.draw_pixel(10, 9)
        self.draw_pixel(11, 9)
        self.draw_pixel(12, 9)
        self.draw_pixel(13, 9)

        # Letra E (empezando en 15,5)
        self.draw_pixel(15, 5)
        self.draw_pixel(16, 5)
        self.draw_pixel(17, 5)
        self.draw_pixel(18, 5)

        self.draw_pixel(15, 6)

        self.draw_pixel(15, 7)
        self.draw_pixel(16, 7)
        self.draw_pixel(17, 7)

        self.draw_pixel(15, 8)

        self.draw_pixel(15, 9)
        self.draw_pixel(16, 9)
        self.draw_pixel(17, 9)
        self.draw_pixel(18, 9)

        # Letra X (empezando en 20,5)
        self.draw_pixel(20, 5)
        self.draw_pixel(23, 5)

        self.draw_pixel(21, 6)
        self.draw_pixel(22, 6)

        self.draw_pixel(21, 7)
        self.draw_pixel(22, 7)

        self.draw_pixel(20, 8)
        self.draw_pixel(23, 8)

        self.draw_pixel(20, 9)
        self.draw_pixel(23, 9)
        self.render()
