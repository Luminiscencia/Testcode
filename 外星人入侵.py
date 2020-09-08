import sys
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group


class Ship():
    def __init__(self,ai_settings,screen):
        '''初始化飞船并设置其初始位置 '''
        self.screen=screen
        self.ai_settings=ai_settings




        #加载飞船图像并获取其外接矩形
        self.image=pygame.image.load('feiji/ship.png')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom

        #在飞船的属性center中存储小数值
        self.center_x=float(self.rect.centerx)
        self.center_y=float(self.rect.centery)

        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    def update(self):
        '''根据移动标志调整飞船位置'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x+=self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center_x-=self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.center_y-=self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center_y+=self.ai_settings.ship_speed_factor

        #根据self.center更新rect对象（根据上述if指令改变图像坐标值）
        self.rect.centerx=self.center_x
        self.rect.centery=self.center_y


    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image,self.rect)

class Settings():
    '''
    存储《外星人入侵》的所有设置类
    '''
    def __init__(self):
        '''初始化游戏设置'''
        #屏幕显示设置
        self.screen_wide_px=1200
        self.screen_height_px=800
        self.bg_color= (230, 230, 230)
        self.screen = pygame.display.set_mode(size=(self.screen_wide_px,self.screen_height_px))
        pygame.display.set_caption('Alien Invation')
        #飞船速度设置
        self.ship_speed_factor = 1.5

        #子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60


class Bullet(Sprite):
    '''一个对飞船发射得的子弹进行管理的类'''
    def __init__(self,ship,ai_settings):
        '''在飞船所处位置创建一个子弹对象'''
        super(Bullet, self).__init__()
        self.screen=ai_settings.screen

        #在（0,0）处创建一个表示子弹的矩形
        self.rect=pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)

        #子弹由飞机顶部开始发射
        self.rect.centerx=ship.rect.centerx


        #用于储存小数表示的子弹位置
        self.y=float(self.rect.y)

        self.color= ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def bullet_update(self):
        '''向上移动子弹'''
        #更新表示位置的小数值
        self.y -= self.speed_factor
        #更新表示子弹rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        '''在屏幕上绘制子弹'''
        pygame.draw.rect(self.screen,self.color,self.rect)


def check_keydown_event(event,ship,bullets,ai_settings):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        #创建一个子弹并将其加入到编组bullet中
        new_bullet = Bullet(ship,ai_settings)
        bullets.add(new_bullet)






def check_keyup_event(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_event(ship,ai_settings,bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_event(event,ship,bullets,ai_settings)
        elif event.type==pygame.KEYUP:
            check_keyup_event(event,ship)




def update_screen(ship,ai_settings,bullets):
    '''更新屏幕上的图像并切换到新屏幕'''
    # 每次循环时都重绘屏幕
    ai_settings.screen.fill(ai_settings.bg_color)
    #在飞船后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    #让最近绘制的屏幕可见
    pygame.display.flip()
    pass

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    #创建一个用于存储子弹的编组
    bullets = Group()
    ship = Ship(ai_settings,ai_settings.screen)


    #开始游戏的主循环
    while True:
        check_event(ship,ai_settings,bullets)
        ship.update()
        bullets.update()

        update_screen(ship,ai_settings,bullets)

        pass
    pass

run_game()