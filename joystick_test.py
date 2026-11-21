import pygame
import math
import sys
pygame .init ()
pygame .joystick .init ()
SCREEN_WIDTH =1200
SCREEN_HEIGHT =800
FPS =60
BLACK =(0 ,0 ,0 )
WHITE =(255 ,255 ,255 )
RED =(255 ,0 ,0 )
GREEN =(0 ,255 ,0 )
BLUE =(0 ,0 ,255 )
YELLOW =(255 ,255 ,0 )
CYAN =(0 ,255 ,255 )
MAGENTA =(255 ,0 ,255 )
GRAY =(128 ,128 ,128 )
LIGHT_GRAY =(200 ,200 ,200 )
DARK_GRAY =(64 ,64 ,64 )
ORANGE =(255 ,165 ,0 )
PURPLE =(128 ,0 ,128 )
class JoystickTester :
    def __init__ (self ):
        self .screen =pygame .display .set_mode ((SCREEN_WIDTH ,SCREEN_HEIGHT ))
        pygame .display .set_caption ("Тестер джойстика")
        self .clock =pygame .time .Clock ()
        self .running =True
        self .font_large =pygame .font .Font (None ,36 )
        self .font_medium =pygame .font .Font (None ,24 )
        self .font_small =pygame .font .Font (None ,18 )
        self .joystick =None
        self .controller_type ="Unknown"
        self .axis_mapping ={}
        self .init_joystick ()
        self .button_states ={}
        self .axis_values ={}
        self .hat_values ={}
        self .button_history ={}
        self .button_colors ={}
    def detect_controller_type (self ,joystick_name ):
        name_lower =joystick_name .lower ()
        if any (x in name_lower for x in ['xbox','microsoft','x-input','xinput']):
            return "Xbox"
        elif any (x in name_lower for x in ['playstation','dualshock','dualsense','ps3','ps4','ps5']):
            return "PlayStation"
        elif any (x in name_lower for x in ['nintendo','switch','профессиональный контроллер']):
            return "Nintendo"
        else :
            return "Generic"
    def setup_axis_mapping (self ,controller_type ,num_axes ):
        if controller_type =="Xbox":
            self .axis_mapping ={
            'left_stick':(0 ,1 ),
            'right_stick':(2 ,3 ),
            'triggers':[(4 ,'LT'),(5 ,'RT')]if num_axes >=6 else []
            }
        elif controller_type =="PlayStation":
            self .axis_mapping ={
            'left_stick':(0 ,1 ),
            'right_stick':(2 ,3 ),
            'triggers':[(4 ,'L2'),(5 ,'R2')]if num_axes >=6 else []
            }
        elif controller_type =="Nintendo":
            self .axis_mapping ={
            'left_stick':(0 ,1 ),
            'right_stick':(2 ,3 ),
            'triggers':[(4 ,'ZL'),(5 ,'ZR')]if num_axes >=6 else []
            }
        else :
            self .axis_mapping ={
            'left_stick':(0 ,1 ),
            'right_stick':(2 ,3 )if num_axes >=4 else (0 ,1 ),
            'triggers':[]
            }
    def init_joystick (self ):
        if pygame .joystick .get_count ()>0 :
            self .joystick =pygame .joystick .Joystick (0 )
            self .joystick .init ()
            self .controller_type =self .detect_controller_type (self .joystick .get_name ())
            self .setup_axis_mapping (self .controller_type ,self .joystick .get_numaxes ())
            print (f"Подключен {self .controller_type } контроллер: {self .joystick .get_name ()}")
            print (f"Маппинг осей: {self .axis_mapping }")
        else :
            print ("Джойстик не найден!")
    def update_joystick_data (self ):
        if not self .joystick :
            return
        for i in range (self .joystick .get_numbuttons ()):
            pressed =self .joystick .get_button (i )
            self .button_states [i ]=pressed
            if i not in self .button_history :
                self .button_history [i ]=0
                self .button_colors [i ]=WHITE
            if pressed :
                self .button_history [i ]=30
                colors =[RED ,GREEN ,BLUE ,YELLOW ,CYAN ,MAGENTA ,ORANGE ,PURPLE ]
                self .button_colors [i ]=colors [i %len (colors )]
            elif self .button_history [i ]>0 :
                self .button_history [i ]-=1
        for i in range (self .joystick .get_numaxes ()):
            self .axis_values [i ]=self .joystick .get_axis (i )
        for i in range (self .joystick .get_numhats ()):
            self .hat_values [i ]=self .joystick .get_hat (i )
    def draw_joystick_info (self ):
        if not self .joystick :
            no_joystick =self .font_large .render ("ДЖОЙСТИК НЕ ПОДКЛЮЧЕН",True ,RED )
            rect =no_joystick .get_rect (center =(SCREEN_WIDTH //2 ,SCREEN_HEIGHT //2 ))
            self .screen .blit (no_joystick ,rect )
            return
        title =self .font_large .render (f"{self .joystick .get_name ()}",True ,WHITE )
        self .screen .blit (title ,(20 ,20 ))
        type_text =self .font_medium .render (f"Тип: {self .controller_type }",True ,LIGHT_GRAY )
        self .screen .blit (type_text ,(20 ,55 ))
    def draw_buttons (self ):
        if not self .joystick :
            return
        title =self .font_medium .render ("КНОПКИ:",True ,WHITE )
        self .screen .blit (title ,(20 ,100 ))
        button_size =40
        buttons_per_row =12
        start_x =20
        start_y =130
        for i in range (self .joystick .get_numbuttons ()):
            row =i //buttons_per_row
            col =i %buttons_per_row
            x =start_x +col *(button_size +5 )
            y =start_y +row *(button_size +5 )
            if self .button_states .get (i ,False ):
                color =self .button_colors .get (i ,WHITE )
                border_color =WHITE
            elif self .button_history .get (i ,0 )>0 :
                fade =self .button_history [i ]/30.0
                base_color =self .button_colors .get (i ,WHITE )
                color =tuple (int (c *fade )for c in base_color )
                border_color =GRAY
            else :
                color =DARK_GRAY
                border_color =GRAY
            pygame .draw .rect (self .screen ,color ,(x ,y ,button_size ,button_size ))
            pygame .draw .rect (self .screen ,border_color ,(x ,y ,button_size ,button_size ),2 )
            text =self .font_small .render (str (i ),True ,BLACK if sum (color )>400 else WHITE )
            text_rect =text .get_rect (center =(x +button_size //2 ,y +button_size //2 ))
            self .screen .blit (text ,text_rect )
    def draw_sticks (self ):
        if not self .joystick :
            return
        title =self .font_medium .render ("АНАЛОГОВЫЕ СТИКИ:",True ,WHITE )
        self .screen .blit (title ,(20 ,300 ))
        stick_radius =60
        stick_center_radius =50
        left_axes =self .axis_mapping .get ('left_stick',(0 ,1 ))
        if len (self .axis_values )>max (left_axes ):
            left_stick_x =120
            left_stick_y =400
            pygame .draw .circle (self .screen ,DARK_GRAY ,(left_stick_x ,left_stick_y ),stick_radius )
            pygame .draw .circle (self .screen ,GRAY ,(left_stick_x ,left_stick_y ),stick_radius ,2 )
            axis_x =self .axis_values .get (left_axes [0 ],0 )
            axis_y =self .axis_values .get (left_axes [1 ],0 )
            stick_pos_x =left_stick_x +int (axis_x *stick_center_radius )
            stick_pos_y =left_stick_y +int (axis_y *stick_center_radius )
            pygame .draw .circle (self .screen ,GREEN ,(stick_pos_x ,stick_pos_y ),8 )
            pygame .draw .circle (self .screen ,WHITE ,(stick_pos_x ,stick_pos_y ),8 ,2 )
            label =self .font_small .render ("Левый стик",True ,WHITE )
            self .screen .blit (label ,(left_stick_x -30 ,left_stick_y +70 ))
            values =self .font_small .render (f"X: {axis_x :.2f}, Y: {axis_y :.2f}",True ,LIGHT_GRAY )
            self .screen .blit (values ,(left_stick_x -40 ,left_stick_y +85 ))
        right_axes =self .axis_mapping .get ('right_stick',(2 ,3 ))
        if len (self .axis_values )>max (right_axes ):
            right_stick_x =320
            right_stick_y =400
            pygame .draw .circle (self .screen ,DARK_GRAY ,(right_stick_x ,right_stick_y ),stick_radius )
            pygame .draw .circle (self .screen ,GRAY ,(right_stick_x ,right_stick_y ),stick_radius ,2 )
            axis_x =self .axis_values .get (right_axes [0 ],0 )
            axis_y =self .axis_values .get (right_axes [1 ],0 )
            stick_pos_x =right_stick_x +int (axis_x *stick_center_radius )
            stick_pos_y =right_stick_y +int (axis_y *stick_center_radius )
            pygame .draw .circle (self .screen ,BLUE ,(stick_pos_x ,stick_pos_y ),8 )
            pygame .draw .circle (self .screen ,WHITE ,(stick_pos_x ,stick_pos_y ),8 ,2 )
            label =self .font_small .render ("Правый стик",True ,WHITE )
            self .screen .blit (label ,(right_stick_x -35 ,right_stick_y +70 ))
            values =self .font_small .render (f"X: {axis_x :.2f}, Y: {axis_y :.2f}",True ,LIGHT_GRAY )
            self .screen .blit (values ,(right_stick_x -40 ,right_stick_y +85 ))
    def draw_triggers (self ):
        if not self .joystick :
            return
        triggers =self .axis_mapping .get ('triggers',[])
        if not triggers :
            return
        title =self .font_medium .render ("ТРИГГЕРЫ:",True ,WHITE )
        self .screen .blit (title ,(520 ,300 ))
        trigger_y =350
        for i ,(axis_id ,name )in enumerate (triggers ):
            if axis_id >=len (self .axis_values ):
                continue
            value =self .axis_values [axis_id ]
            x =580 +i *80
            bar_height =100
            bar_width =25
            if self .controller_type =="Xbox":
                fill_height =int ((value +1 )/2 *bar_height )
            else :
                fill_height =int (abs (value )*bar_height )
            pygame .draw .rect (self .screen ,DARK_GRAY ,(x ,trigger_y ,bar_width ,bar_height ))
            pygame .draw .rect (self .screen ,GRAY ,(x ,trigger_y ,bar_width ,bar_height ),2 )
            if fill_height >0 :
                color =RED if i ==0 else ORANGE
                pygame .draw .rect (self .screen ,color ,(x ,trigger_y +bar_height -fill_height ,bar_width ,fill_height ))
            label =self .font_small .render (name ,True ,WHITE )
            label_rect =label .get_rect (center =(x +bar_width //2 ,trigger_y +bar_height +15 ))
            self .screen .blit (label ,label_rect )
            value_text =self .font_small .render (f"{value :.2f}",True ,LIGHT_GRAY )
            value_rect =value_text .get_rect (center =(x +bar_width //2 ,trigger_y +bar_height +30 ))
            self .screen .blit (value_text ,value_rect )
    def draw_dpad (self ):
        if not self .joystick or self .joystick .get_numhats ()==0 :
            return
        title =self .font_medium .render ("D-PAD:",True ,WHITE )
        self .screen .blit (title ,(750 ,300 ))
        dpad_x =800
        dpad_y =380
        button_size =30
        hat_value =self .hat_values .get (0 ,(0 ,0 ))
        pygame .draw .rect (self .screen ,DARK_GRAY ,
        (dpad_x -45 ,dpad_y -45 ,90 ,90 ))
        pygame .draw .rect (self .screen ,GRAY ,
        (dpad_x -45 ,dpad_y -45 ,90 ,90 ),2 )
        color =GREEN if hat_value [1 ]==1 else DARK_GRAY
        pygame .draw .rect (self .screen ,color ,
        (dpad_x -15 ,dpad_y -45 ,button_size ,button_size ))
        color =GREEN if hat_value [1 ]==-1 else DARK_GRAY
        pygame .draw .rect (self .screen ,color ,
        (dpad_x -15 ,dpad_y +15 ,button_size ,button_size ))
        color =GREEN if hat_value [0 ]==-1 else DARK_GRAY
        pygame .draw .rect (self .screen ,color ,
        (dpad_x -45 ,dpad_y -15 ,button_size ,button_size ))
        color =GREEN if hat_value [0 ]==1 else DARK_GRAY
        pygame .draw .rect (self .screen ,color ,
        (dpad_x +15 ,dpad_y -15 ,button_size ,button_size ))
        value_text =self .font_small .render (f"({hat_value [0 ]}, {hat_value [1 ]})",True ,LIGHT_GRAY )
        value_rect =value_text .get_rect (center =(dpad_x ,dpad_y +55 ))
        self .screen .blit (value_text ,value_rect )
    def handle_events (self ):
        for event in pygame .event .get ():
            if event .type ==pygame .QUIT :
                self .running =False
            elif event .type ==pygame .KEYDOWN :
                if event .key ==pygame .K_ESCAPE :
                    self .running =False
            elif event .type ==pygame .JOYDEVICEADDED :
                self .init_joystick ()
            elif event .type ==pygame .JOYDEVICEREMOVED :
                self .joystick =None
    def run (self ):
        while self .running :
            self .handle_events ()
            self .update_joystick_data ()
            self .screen .fill (BLACK )
            self .draw_joystick_info ()
            self .draw_buttons ()
            self .draw_sticks ()
            self .draw_triggers ()
            self .draw_dpad ()
            pygame .display .flip ()
            self .clock .tick (FPS )
        pygame .quit ()
        sys .exit ()
if __name__ =="__main__":
    app =JoystickTester ()
    app .run ()