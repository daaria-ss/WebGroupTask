import os
import sys
import pygame
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PIL import Image
import cv2


SCREEN_SIZE = [800, 800]

def zoom():
    image = cv2.imread('map.png')
    cv2.imwrite('map.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    im = Image.open("map.jpg")
    im1 = Image.new("RGB", (1300, 900), (0, 0, 0))
    pixels = im.load()
    pixels1 = im1.load()
    x, y = im.size
    for i in range(x):  
        for j in range(y):
            r, g, b = pixels[i, j]
            pixels1[i * 2, j * 2] = r, g, b
            pixels1[i * 2 + 1, j * 2] = r, g, b
            pixels1[i * 2, j * 2 + 1] = r, g, b
            pixels1[i * 2 + 1, j * 2 + 1] = r, g, b
    im1.save("map1.png")

def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print('')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

class Example(QWidget):
    def __init__(self):
        super().__init__()
        typemap = ['map', 'sat', 'sat,skl']
        flagtypemap = 0
        pygame.init()
        size = width, height = 1300, 900
        x = '30.268110'
        y = '59.866490'
        screen = pygame.display.set_mode(size)
        running = 1
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = 0
                    if event.key == pygame.K_LEFT:
                        x = str(float(x) - 0.0001)
                        a = y.split('.')
                        x += '0' * (6 - len(a[1]))
                    if event.key == pygame.K_RIGHT:
                        x = str(float(x) + 0.0001)
                        a = y.split('.')
                        x += '0' * (6 - len(a[1]))
                    if event.key == pygame.K_DOWN:
                        y = str(float(y) - 0.0001)
                        a = y.split('.')
                        y += '0' * (6 - len(a[1]))
                    if event.key == pygame.K_UP:
                        y = str(float(y) + 0.0001)
                        a = y.split('.')
                        y += '0' * (6 - len(a[1]))
            screen.fill((0, 0, 0))
            sait = "http://static-maps.yandex.ru/1.x/?ll="
            sait += x
            sait += ','
            sait += y
            sait += "&spn=0.001,0.001&l="
            sait += typemap[flagtypemap]
            sait += "&size="
            sait += str(650)
            sait += ','
            sait += str(450)
            self.getImage(sait)
            #self.initUI()
            all_sprites = pygame.sprite.Group()
            sprite = pygame.sprite.Sprite()
            sprite.image = load_image("map1.png")
            sprite.rect = sprite.image.get_rect()
            all_sprites.add(sprite)
            sprite.rect.x = 0
            sprite.rect.y = 0
            all_sprites.draw(screen)
            pygame.display.flip()
            pygame.time.delay(1)
        pygame.quit()

    def getImage(self, sait):
        map_request = sait
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        zoom()

    def closeEvent(self, event):
        os.remove(self.map_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
