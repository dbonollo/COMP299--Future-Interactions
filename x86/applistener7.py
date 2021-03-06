import Leap
import sys
import winsound
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import os
import pygame
import re
import math
import time
from pygame.locals import *
from pygame import midi
'''
Notes:  find time sig and bpm and correspond audio to that.
'''

timer = pygame.time.Clock()
playsound = USEREVENT + 1
pygame.time.set_timer(playsound, 500)
pygame.midi.init()
b = False
pygame.init()

 #sets hardware surface
resolutions = pygame.display.list_modes()
horiz = int(resolutions[0][0] //1.5) 
vert = int(resolutions[0][1]  // 1.5)

#if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'
bits = 16
pygame.mixer.pre_init(44100, -bits, 2,64)


gamecontinue = True
pattern = pygame.image.load("4-4pattern.png")

xs = pygame.mixer.music
xs.load("C:maryNorm.mid")


class beatbox:
    def __init__(self,display_surf):
	self.display_surf = display_surf
        self.go = 0
        self.i = 0
        self.score = 0
        self.beatArray = [] # stores array of pygame Rect objects
        self.beatCount = 0  # for looping through beat array
        self.b = False      # True or False triggered every second
        for i in range(4): #appends Rect object to the beat array 
            self.beatArray.append(pygame.Rect(0,0,400,400))
        
        #moves the boxes for collision testing
        self.beatArray[0].center = (int(horiz *.5),int(vert * .75))
        self.beatArray[1].center =(int(horiz*.25),int(vert *.5))
        self.beatArray[2].center =(int(horiz*.75),int(vert *.5))
        self.beatArray[3].center =(int(horiz *.5),int(vert *.25))
        
    def interaction(self,x,y):#checks for collisions and plays current note in song.
        for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		#controller.remove_listener(listener)
		pygame.quit()
		sys.exit()
	if self.go == 0 :
	    xs.play()
	    self.go = 1
	if self.go == 1:
	    
	    self.display_surf.fill((0,0,0)) #fills the display surface with black
	    self.display_surf.blit(pattern, ((horiz * .5) + 200, 10))
	    pygame.draw.circle(self.display_surf,(168,54,245),(int(horiz * .5) ,int(vert * .25)), 100)
	    pygame.draw.circle(self.display_surf,(255,0,0),(int(horiz * .5) ,int(vert * .75)), 100)
	    pygame.draw.circle(self.display_surf,(73,195,240),(int(horiz * .25) ,int(vert * .50)), 100)
	    pygame.draw.circle(self.display_surf,(24,161,33),(int(horiz * .75) ,int(vert * .50)), 100)
	    pygame.draw.circle(self.display_surf,(0,255,0),(x ,y ), 10)#prints a circle on the screen
	    
	    pygame.display.flip() 
		
	       
	    
		   
	    if pygame.event.get(playsound): #triggers event every second and updates beat spot and song note
		a = pygame.time.get_ticks()
		
		self.i += 1
		self.b = True
		if self.beatCount < 3 :
		    self.beatCount += 1
		    
		else:
		    self.beatCount = 0
		xs.set_volume(0.0)
	    if (self.beatArray[self.beatCount -1 ].collidepoint(x,y) and self.b == True):
		
		xs.set_volume(.99)
		self.score += 1
		self.b = False   
	    if pygame.mixer.music.set_endevent():
		gamecontinue = False
		self.check_hit()
    def check_hit(self):#point system for accuracy
        
    
        pass
    
    def blip(self):
	b = 100
	if(self.beatCount == 0 ):
	    pygame.draw.circle(self.display_surf,(255,0,0),(int(horiz * .5) ,int(vert * .75)), 20 + b)
	    
	elif(self.beatCount == 1 ):
	    pygame.draw.circle(self.display_surf,(73,195,240),(int(horiz * .25) ,int(vert * .50)), 20 + b)
	    
	elif(self.beatCount == 2 ):
	    pygame.draw.circle(self.display_surf,(24,161,33),(int(horiz * .75) ,int(vert * .50)), 20 + b)
	    
	elif(self.beatCount == 3 ):
	    pygame.draw.circle(self.display_surf,(168,54,245),(int(horiz * .5) ,int(vert * .25)), 20 + b)     
	
                

        

class applistener(Leap.Listener):
    
    def on_init(self,controller):
        self.check = 0
        
	self.directional = {}
	self.directional['x'] = 0
	self.directional['y'] = 0
	self.directional['z'] = 0
        x = y = 0
        
        
        self._running = True 
        
       
        print "Connected"
        timerz = 0
    def on_connect(self,controller):
        print "Connected"
        
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        
    def on_disconnect(self,controller):
        print "Disconnected"
        
    def on_exit(self,controller):
        print "Exited"
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        return self._running
    def on_loop(self, end):
        print "hello"
        
        if self.running == False:
            return False
        else:
            return True
    def exits(self):
        return False
    
    
    def on_cleanup(self):
        if self.on_loop == True:
            return False
    
    
    def on_frame(self,controller):#Leap motion loop listens for any interaction with Leap Motion device

        frame = controller.frame()  
         #polls for any user input events
        iBox = frame.interaction_box
            
            
        
        
        if not frame.hands.is_empty:#Checks for hands or pointables over Leap
            
            hand = frame.hands[0] # fingers on first hand
            hand2 = frame.hands[1]# fingers on second hand
            
            fingers1 = hand.fingers # list of fingers from first hand
            fingers2 = hand2.fingers # list of fingers from second hand
            if not frame.fingers.is_empty:#checks fingers
                if not fingers1.is_empty: #checks if fingers from first hand are present
                    
                    #print iBox.width , iBox.height
		    screenPosition = iBox.normalize_point(fingers1[0].tip_position)
		    self.directional['x'] = int(screenPosition[0] * horiz)
		    self.directional['y'] = -(vert - int(screenPosition[1] * vert))
		    #print self.directional['x'],self.directional['y']
		    
                    
        for gesture in frame.gestures(): #reads in a swipe gesture
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                #print self.state_string(gesture.state)
                #print swipe.start_position
                #print swipe.direction
                #print swipe.position
                self.on_cleanup()
       
        
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
def timeSig(time):
    pass
def midis():
    pass
    #coun = pygame.midi.get_count()
    #print coun
class cursor:
    def __init__(self,display_surf):
	self.x = 0
	self.y = 0
	self.display = display_surf
	
    def cursorPrint(self,x,y):
	pygame.draw.circle(self.display,(0,255,0),(x ,y ), 10)
	self.x = x
	self.y = y
    def cursorPos(self):
	print self.x,self.y
	return (self.x, self.y) 
class songs:
    def __init__(self):
	self.songName
	self.timeSig
	self.midiName
    def name(self):
	return self.songName
    def time_sig(self):
	return self.timeSig
    def midi_name(self):
	return self.midiName
class menus:
    
    def __init__(self,display_surf):
	pygame.font.init()
	self.display_surf = display_surf
	self.menu_index = 0
	self.menu_dict = {}
	self.ButPress = 0
	self.ButTimer = pygame.time
	self.button = USEREVENT + 1
	self.ButTimer.set_timer(self.button, 2000)
	self.grow = 0
	self.curs = cursor(display_surf)
	
    def buttonDict(self):
	self.menu_dict["play"] = [pygame.Rect(0,0,200,72),1]
	
    def main_menu(self,listener,controller):
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		controller.remove_listener(listener)
		pygame.quit()
		sys.exit()	
	fonts = pygame.font.Font(None,72)
	text = fonts.render("Project Broomstick!",1,(0,255,255))
	play = fonts.render("Play",1,(0,255,255))
	instruct = fonts.render("Instructions",1,(0,255,255))
	self.display_surf.fill((0,0,0))
	self.display_surf.blit(text,(horiz * .35,vert * .25))
	self.display_surf.blit(play,(horiz * .35,vert * .65))
	self.display_surf.blit(instruct,(horiz * .35,vert * .75))
	
	self.menu_dict["play"] = [pygame.Rect(0,0,200,72),1]
	self.menu_dict["play"][0].center = (int(horiz *.35),int(vert * .75))
	pygame.draw.circle(self.display_surf,(0,255,0),(listener.directional['x'] ,-(listener.directional['y']) ), 10)
	for i in self.menu_dict:
	    if self.menu_dict[i][0].collidepoint(listener.directional['x'] ,-(listener.directional['y'])):
		self.grow += .05
		if self.grow == 3:
		    self.grow = 0
		pygame.draw.circle(self.display_surf,(0,255,0),(listener.directional['x'] ,-(listener.directional['y']) ), 10 + int(self.grow), 2)
	        
		
		self.ButPress = 1
		if pygame.event.get(self.button):
		    self.menu_index = 1    	    
	    else:
		self.ButPress = 0
		self.grow = 0
		self.ButTimer.set_timer(self.button, 2000)
	    pygame.display.flip()
	
    def song_sel(self,listener,controller):
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		controller.remove_listener(listener)
		pygame.quit()
		sys.exit()	
	self.display_surf.fill((0,0,0))
	fonts = pygame.font.Font(None,72)
	text = fonts.render("Mary Had A Little Lamb",1,(0,255,255))
	#print fonts.size("Mary Had A Little Lamb")
	self.display_surf.blit(text,(10,10))
	pygame.draw.circle(self.display_surf,(0,255,0),(listener.directional['x'] ,-(listener.directional['y']) ), 10)
	Button = pygame.Rect(10,10,571,52)
	pygame.draw.rect(self.display_surf, (255,0,0), Button, 2)
	for i in self.menu_dict:
	    if Button.collidepoint(listener.directional['x'] ,-(listener.directional['y'])):
		self.grow += .05
		if self.grow == 3:
		    self.grow = 0
		pygame.draw.circle(self.display_surf,(0,255,0),(listener.directional['x'] ,-(listener.directional['y']) ), 10 + int(self.grow), 2)
		
		
		self.ButPress = 1
		if pygame.event.get(self.button):
		    self.menu_index = 2    	    
	    else:
		self.ButPress = 0
		self.grow = 0
		self.ButTimer.set_timer(self.button, 2000)	
	pygame.display.flip()
    
    def buttonPress(self):
	
	return self.menu_index


def pygameLoop(controller, listener):
    check = 0
    
    display_surf = pygame.display.set_mode((horiz,vert), pygame.HWSURFACE) #sets hardware surface
    menuNum = 0
    
    menu = menus(display_surf)
    beatboxes = beatbox(display_surf)
    _running = True 
    
    #self._image_surf = pygame.image.load("myimage.jpg").convert()
    print "Connected"
    timerz = 0
    
    while True:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		controller.remove_listener(listener)
		pygame.quit()
		sys.exit()
	while(menu.menu_index == 0):
	    menu.main_menu(listener,controller)
	while(menu.menu_index == 1):
	    menu.song_sel(listener,controller)
	while(menu.menu_index == 2):
	    if gamecontinue == True:
		beatboxes.blip()
		beatboxes.interaction(listener.directional['x'], -(listener.directional['y']))	    
	

def main():
    
    controller = Leap.Controller()
    applistener1 = applistener()
    controller.add_listener(applistener1)
    
    
    print "Press Enter to quit..."
   
    #sys.stdin.readline()
    
    pygameLoop(controller,applistener1)
    controller.remove_listener(applistener1)
    
    
if __name__ == "__main__":
    main()