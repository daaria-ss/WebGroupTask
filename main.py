import os
import sys
import pygame
import requests
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import cv2


SCREEN_SIZE = [800, 800]

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
        zoommap = ['0.001', '0.002', '0.003', '0.005', '0.011', '0.021', '0.040', '0.079', '0.157', '0.313', '0.625', '1.249', '2.500', '5.000', '10.000', '20.000', '40.000']
        flagzoom = 0
        pygame.init()
        size = width, height = 650, 450
        x = '30.268110'
        y = '59.866490'
        screen = pygame.display.set_mode(size)
        running = 1
        z = "0.001"
        
        font = pygame.font.Font(None, 24)
        input_box = pygame.Rect(10, 10, 140, 32)
        input_box_adress = pygame.Rect(10, 400, 140, 25)
        color_inactive = pygame.Color((150, 150, 150))
        color_active = pygame.Color((50, 50, 50))
        color = color_inactive
        color_adress = pygame.Color((50, 50, 50))
        active = False
        active_adress = False
        text = 'Поиск'
        text_adress = '198096'
        flagmetka = 0
        xmetka = 0
        ymetka = 0
        flagindex = 1
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                    if event.pos[0] >= 415 and event.pos[0] <= 440:
                        if event.pos[1] >= 10 and event.pos[1] <= 45:
                            text = ''
                            flagmetka = 0
                    if event.pos[0] >= 160 and event.pos[0] <= 390:
                        if event.pos[1] >= 390 and event.pos[1] <= 440:
                            if flagindex == 0:
                                flagindex = 1
                            else:
                                if flagindex == 1:
                                    flagindex = 0
                    if event.pos[0] >= 470 and event.pos[0] <= 570:
                        if event.pos[1] >= 10 and event.pos[1] <= 45:
                            geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode="
                            text1 = text.replace(' ', '')
                            geocoder_request += text1
                            geocoder_request += "&format=json"
                            response = requests.get(geocoder_request)
                            if response:
                                json_response = response.json()
                                try:
                                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                                except:
                                    pass
                                try:
                                    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
                                    toponym_coodrinates = toponym["Point"]["pos"]
                                    toponym_coodrinates = toponym_coodrinates.split(' ')
                                    toponym_address = toponym_address.split(', ')
                                    x = toponym_coodrinates[0]
                                    y = toponym_coodrinates[1]
                                    xmetka = x
                                    ymetka = y
                                    text = ''
                                    for i in range(len(toponym_address)):
                                        text += toponym_address[i]
                                        text += ' '
                                    if len(toponym_address) >= 3:
                                        flagzoom = 2
                                    if len(toponym_address) == 2:
                                        flagzoom = 7
                                    if len(toponym_address) == 1:
                                        flagzoom = 15
                                    if flagindex == 1:
                                        text1 = text.replace(' ', ', ')
                                        json_data  = {"query":text1,"limit":5,"fromBound":"CITY"}
                                        resp = requests.post('https://www.pochta.ru/suggestions/v2/suggestion.find-addresses', json=json_data)
                                        resp.json()
                                        try:
                                            text_adress = resp.json()[0]['postalCode']
                                        except:
                                            text_adress = ''
                                    flagmetka = 1
                                except:
                                    text = 'Error'
                                    flagmetka = 0
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                    if event.key == pygame.K_ESCAPE:
                        running = 0
                    if event.key == pygame.K_LEFT:
                        x = str(float(x) - float(float(zoommap[flagzoom]) / 10))
                        a = y.split('.')
                        x += '0' * (6 - len(a[1]))
                    if event.key == pygame.K_RIGHT:
                        x = str(float(x) + float(float(zoommap[flagzoom]) / 10))
                        a = y.split('.')
                        x += '0' * (6 - len(a[1]))
                    if event.key == pygame.K_DOWN:
                        y = str(float(y) - float(float(zoommap[flagzoom]) / 10))
                        a = y.split('.')
                        y += '0' * (6 - len(a[1]))
                    if event.key == pygame.K_UP:
                        y = str(float(y) + float(float(zoommap[flagzoom]) / 10))
                        a = y.split('.')
                        y += '0' * (6 - len(a[1]))
                    if event.key == pygame.K_TAB:
                        flagtypemap += 1
                        if flagtypemap > 2:
                            flagtypemap = 0
                    if event.key == pygame.K_PAGEUP:
                        if flagzoom < len(zoommap) - 1:
                            flagzoom += 1
                    if event.key == pygame.K_PAGEDOWN:
                        if flagzoom > 0:
                            flagzoom -= 1
            screen.fill((0, 0, 0))
            sait = "http://static-maps.yandex.ru/1.x/?ll="
            sait += x
            sait += ","
            sait += y
            sait += "&spn="
            sait += zoommap[flagzoom]
            sait += ","
            sait += zoommap[flagzoom]
            sait += "&l="
            sait += typemap[flagtypemap]
            sait += "&size="
            sait += str(650)
            sait += ','
            sait += str(450)
            if flagmetka == 1:
                sait += "&pt="
                sait += xmetka
                sait += ","
                sait += ymetka
                sait += ",pm2rdl"
            self.getImage(sait)
            all_sprites = pygame.sprite.Group()
            sprite = pygame.sprite.Sprite()
            sprite.image = load_image("map.png")
            sprite.rect = sprite.image.get_rect()
            all_sprites.add(sprite)
            sprite.rect.x = 0
            sprite.rect.y = 0
            sprite1 = pygame.sprite.Sprite()
            sprite1.image = load_image("Button.png")
            sprite1.rect = sprite1.image.get_rect()
            all_sprites.add(sprite1)
            sprite1.rect.x = 470
            sprite1.rect.y = 10
            sprite2 = pygame.sprite.Sprite()
            sprite2.image = load_image("X.png")
            sprite2.rect = sprite2.image.get_rect()
            all_sprites.add(sprite2)
            sprite2.rect.x = 415
            sprite2.rect.y = 10
            sprite3 = pygame.sprite.Sprite()
            sprite3.image = load_image("Button1.png")
            sprite3.rect = sprite3.image.get_rect()
            all_sprites.add(sprite3)
            sprite3.rect.x = 160
            sprite3.rect.y = 390
            all_sprites.draw(screen)
            txt_surface = font.render(text, True, color)
            txt_surface_adress = font.render(text_adress, True, color_adress)
            width = max(400, txt_surface.get_width()+10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(screen, color, input_box, 2)
            if flagindex == 1:
                screen.blit(txt_surface_adress, (input_box_adress.x+5, input_box_adress.y+5))
                pygame.draw.rect(screen, color_adress, input_box_adress, 2)
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

    def closeEvent(self, event):
        os.remove(self.map_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
