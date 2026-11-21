import pygame
import json
import os
pygame .init ()
pygame .joystick .init ()
SCREEN_WIDTH =800
SCREEN_HEIGHT =600
CUBE_SIZE =30
GRAVITY =0.5
JUMP_FORCE =-12
MOVE_SPEED =5
BLACK =(0 ,0 ,0 )
WHITE =(255 ,255 ,255 )
RED =(255 ,0 ,0 )
BLUE =(0 ,0 ,255 )
GREEN =(0 ,255 ,0 )
GRAY =(128 ,128 ,128 )
LIGHT_GRAY =(200 ,200 ,200 )
class Settings :
    def __init__ (self ):
        self .config_file ="joystick_config.json"
        self .load_config ()
    def load_config (self ):
        default_config ={
        "joystick_enabled":True ,
        "joystick_id":0 ,
        "dead_zone":0.1 ,
        "keyboard_controls":{
        "up":pygame .K_w ,
        "down":pygame .K_s ,
        "left":pygame .K_a ,
        "right":pygame .K_d ,
        "jump":pygame .K_SPACE
        },
        "joystick_controls":{
        "jump_button":0 ,
        "axis_x":0 ,
        "axis_y":1
        }
        }
        try :
            if os .path .exists (self .config_file ):
                with open (self .config_file ,'r')as f :
                    self .config =json .load (f )
            else :
                self .config =default_config
                self .save_config ()
        except :
            self .config =default_config
    def save_config (self ):
        try :
            with open (self .config_file ,'w')as f :
                json .dump (self .config ,f ,indent =4 )
        except :
            print ("Ошибка сохранения конфигурации")
class Cube :
    def __init__ (self ,x ,y ):
        self .x =x
        self .y =y
        self .vel_x =0
        self .vel_y =0
        self .on_ground =False
        self .color =RED
    def update (self ):
        self .vel_y +=GRAVITY
        self .x +=self .vel_x
        self .y +=self .vel_y
        if self .x <0 :
            self .x =0
        elif self .x >SCREEN_WIDTH -CUBE_SIZE :
            self .x =SCREEN_WIDTH -CUBE_SIZE
        if self .y >=SCREEN_HEIGHT -CUBE_SIZE -50 :
            self .y =SCREEN_HEIGHT -CUBE_SIZE -50
            self .vel_y =0
            self .on_ground =True
        else :
            self .on_ground =False
        self .vel_x *=0.8
    def move (self ,dx ,dy ):
        self .vel_x +=dx
        if self .vel_x >MOVE_SPEED :
            self .vel_x =MOVE_SPEED
        elif self .vel_x <-MOVE_SPEED :
            self .vel_x =-MOVE_SPEED
    def jump (self ):
        if self .on_ground :
            self .vel_y =JUMP_FORCE
            self .on_ground =False
    def draw (self ,screen ):
        pygame .draw .rect (screen ,self .color ,(self .x ,self .y ,CUBE_SIZE ,CUBE_SIZE ))
        pygame .draw .rect (screen ,GRAY ,(self .x +2 ,self .y +2 ,CUBE_SIZE ,CUBE_SIZE ))
class Game :
    def __init__ (self ):
        self .screen =pygame .display .set_mode ((SCREEN_WIDTH ,SCREEN_HEIGHT ))
        pygame .display .set_caption ("Кубик с джойстиком")
        self .clock =pygame .time .Clock ()
        self .running =True
        self .settings =Settings ()
        self .joystick =None
        self .init_joystick ()
        self .cube =Cube (SCREEN_WIDTH //2 ,SCREEN_HEIGHT //2 )
        self .font =pygame .font .Font (None ,24 )
        self .show_settings =False
    def init_joystick (self ):
        if self .settings .config ["joystick_enabled"]and pygame .joystick .get_count ()>0 :
            joystick_id =min (self .settings .config ["joystick_id"],pygame .joystick .get_count ()-1 )
            self .joystick =pygame .joystick .Joystick (joystick_id )
            self .joystick .init ()
            print (f"Подключен джойстик: {self .joystick .get_name ()}")
        else :
            print ("Джойстик не найден или отключен")
    def handle_input (self ):
        keys =pygame .key .get_pressed ()
        move_x ,move_y =0 ,0
        if keys [self .settings .config ["keyboard_controls"]["up"]]:
            move_y -=1
        if keys [self .settings .config ["keyboard_controls"]["down"]]:
            move_y +=1
        if keys [self .settings .config ["keyboard_controls"]["left"]]:
            move_x -=1
        if keys [self .settings .config ["keyboard_controls"]["right"]]:
            move_x +=1
        if self .joystick :
            axis_x =self .joystick .get_axis (self .settings .config ["joystick_controls"]["axis_x"])
            axis_y =self .joystick .get_axis (self .settings .config ["joystick_controls"]["axis_y"])
            dead_zone =self .settings .config ["dead_zone"]
            if abs (axis_x )>dead_zone :
                move_x +=axis_x
            if abs (axis_y )>dead_zone :
                move_y +=axis_y
        if move_x !=0 or move_y !=0 :
            import math
            length =math .sqrt (move_x *move_x +move_y *move_y )
            if length >1 :
                move_x /=length
                move_y /=length
            self .cube .move (move_x *2 ,0 )
    def handle_events (self ):
        for event in pygame .event .get ():
            if event .type ==pygame .QUIT :
                self .running =False
            elif event .type ==pygame .KEYDOWN :
                if event .key ==self .settings .config ["keyboard_controls"]["jump"]:
                    self .cube .jump ()
                elif event .key ==pygame .K_F1 :
                    self .show_settings =not self .show_settings
                elif event .key ==pygame .K_ESCAPE :
                    self .running =False
            elif event .type ==pygame .JOYBUTTONDOWN :
                if self .joystick and event .button ==self .settings .config ["joystick_controls"]["jump_button"]:
                    self .cube .jump ()
            elif event .type ==pygame .JOYDEVICEADDED :
                self .init_joystick ()
            elif event .type ==pygame .JOYDEVICEREMOVED :
                self .joystick =None
    def draw_settings (self ):
        if not self .show_settings :
            return
        overlay =pygame .Surface ((SCREEN_WIDTH ,SCREEN_HEIGHT ))
        overlay .set_alpha (128 )
        overlay .fill (BLACK )
        self .screen .blit (overlay ,(0 ,0 ))
        settings_rect =pygame .Rect (100 ,100 ,600 ,400 )
        pygame .draw .rect (self .screen ,WHITE ,settings_rect )
        pygame .draw .rect (self .screen ,BLACK ,settings_rect ,2 )
        title =self .font .render ("НАСТРОЙКИ (F1 - закрыть)",True ,BLACK )
        self .screen .blit (title ,(120 ,120 ))
        y_offset =160
        if self .joystick :
            joystick_info =[
            f"Джойстик: {self .joystick .get_name ()}",
            f"Кнопок: {self .joystick .get_numbuttons ()}",
            f"Осей: {self .joystick .get_numaxes ()}",
            "",
            "Управление:",
            f"Движение: Левый стик",
            f"Прыжок: Кнопка {self .settings .config ['joystick_controls']['jump_button']}",
            ]
        else :
            joystick_info =[
            "Джойстик не подключен",
            "",
            "Управление клавиатурой:",
            f"W/A/S/D - движение в 8 направлениях",
            f"Пробел - прыжок",
            ]
        for line in joystick_info :
            text =self .font .render (line ,True ,BLACK )
            self .screen .blit (text ,(120 ,y_offset ))
            y_offset +=25
    def draw_hud (self ):
        info_lines =[
        f"На земле: {'Да'if self .cube .on_ground else 'Нет'}",
        "",
        "F1 - Настройки",
        "ESC - Выход"
        ]
        y_offset =10
        for line in info_lines :
            text =self .font .render (line ,True ,WHITE )
            self .screen .blit (text ,(10 ,y_offset ))
            y_offset +=25
    def run (self ):
        while self .running :
            self .handle_events ()
            self .handle_input ()
            self .cube .update ()
            self .screen .fill (BLUE )
            pygame .draw .rect (self .screen ,GREEN ,(0 ,SCREEN_HEIGHT -50 ,SCREEN_WIDTH ,50 ))
            self .cube .draw (self .screen )
            self .draw_hud ()
            self .draw_settings ()
            pygame .display .flip ()
            self .clock .tick (60 )
        pygame .quit ()
if __name__ =="__main__":
    game =Game ()
    game .run ()