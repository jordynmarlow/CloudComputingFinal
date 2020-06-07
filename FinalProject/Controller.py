from pygame.locals import *
import pygame
import Viewer

# chat window colors
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')

class Player:
    x = 44
    y = 44
    speed = 1
 
    def moveRight(self):
        self.x = self.x + self.speed
 
    def moveLeft(self):
        self.x = self.x - self.speed
 
    def moveUp(self):
        self.y = self.y - self.speed
 
    def moveDown(self):
        self.y = self.y + self.speed
 
class Maze:
    def __init__(self):
       self.M = 10
       self.N = 8
       self.maze = [ 1,1,1,1,1,1,1,1,1,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,0,1,1,1,1,1,1,0,1,
                     1,0,1,0,0,0,0,0,0,1,
                     1,0,1,0,1,1,1,1,0,1,
                     1,0,0,0,0,0,0,0,2,1,
                     1,1,1,1,1,1,1,1,1,1,]

    def draw(self,display_surf,block_surf,flag_surf):
        bx = 0
        by = 0
        for i in range(0,self.M*self.N):
            if self.maze[ bx + (by*self.M) ] == 1:
                display_surf.blit(block_surf,( bx * 44 , by * 44))
            elif self.maze[ bx + (by*self.M) ] == 2:
                display_surf.blit(flag_surf,( bx * 44 , by * 44))
            bx = bx + 1
            if bx > self.M-1:
                bx = 0 
                by = by + 1


class App:
 
    windowWidth = 800
    windowHeight = 600
    player = 0
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.player = Player()
        self.maze = Maze()
 
    def on_init(self):
        pygame.init()
        self.input_box = pygame.Rect(250, 450, 500, 32)
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        

        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("player.png").convert()
        self._block_surf = pygame.image.load("block.png").convert()
        self._flag_surf = pygame.image.load("flag.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        pass
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self._display_surf.blit(self._image_surf,(self.player.x,self.player.y))
        self.maze.draw(self._display_surf, self._block_surf, self._flag_surf)
        self.color = color_active
        pygame.draw.rect(self._display_surf, self.color, self.input_box, 2)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()

    def chat(self):
        done = False
        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        text = ''
        print('debug')
        # make text box active
        while not done:
            pygame.event.pump()
            for event in pygame.event.get():
                #pygame.event.pump()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # send info through socket instead of sending to Viewer function
                        Viewer.printChat(text)
                        text = ''
                        self.color = color_inactive
                        done = True
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                else:
                    done = False
            self.on_render()
            # Render the current text.
            txt_surface = font.render(text, True, self.color)
            # Resize the box if the text is too long.
            #width = max(200, txt_surface.get_width()+10)
            #self.input_box.w = width
            # Blit the text.
            self._display_surf.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
            # Blit the input_box rect.
            pygame.display.flip()
            clock.tick(30)
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if (keys[K_BACKSPACE]):
                self.chat()

            if (keys[K_RIGHT]):
                self.player.moveRight()
            if (keys[K_LEFT]):
                self.player.moveLeft()
            if (keys[K_UP]):
                self.player.moveUp()
            if (keys[K_DOWN]):
                self.player.moveDown()
            if (keys[K_ESCAPE]):
                self._running = False
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()