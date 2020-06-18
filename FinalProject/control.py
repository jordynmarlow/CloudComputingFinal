# Controller Client
# This client will have full game functionality except the Coin will be invisible
import pygame
import random
from os import path
import socket

# Settings
WIDTH = 960
HEIGHT = 540
FPS = 60
TITLE = 'Labyrinth Controller'
ACC = 0.5
FRICTION = -0.15
GRAVITY = 0.2
FONT = 'Arial'
BACKGROUND_IMAGE = 'background.png'
SMALL_PLATFORM = 'small_platform.png'
MEDIUM_PLATFORM = 'medium_platform.png'
LARGE_PLATFORM = 'large_platform.png'
COIN_ANIM = 'coin.png'
PLAYER_IDLE_ANIM = 'idle.png'
PLAYER_RUN_ANIM = 'run.png'
PLAYER_JUMP_ANIM = 'jump.png'

BOTTOM_PLATFORM = (LARGE_PLATFORM, WIDTH / 2, HEIGHT, 3072, 128)
PLATFORM_LIST = [(MEDIUM_PLATFORM, 350, HEIGHT - 300, 1536, 128),
                (SMALL_PLATFORM, 750, HEIGHT - 150, 768, 128),
                BOTTOM_PLATFORM]

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "54.164.222.47"
port = 9999
clientSocket.connect((host, port))
print("Connection done")
clientSocket.setblocking(0)

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
    
    def get_image(self, x, y, w, h):
        image = pygame.Surface((w, h))
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        return image

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_r
        self.image.set_colorkey(pygame.Color('White'))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.rect.midbottom = self.pos
        self.on_floor = False
    
    def load_images(self):
        self.idle_r = self.game.load_image(PLAYER_IDLE_ANIM).get_image(0, 0, 100, 104)
        self.idle_r = pygame.transform.scale(self.idle_r, (75, 76))
        self.idle_l = pygame.transform.flip(self.idle_r, True, False)
        self.jump_r = self.game.load_image(PLAYER_JUMP_ANIM).get_image(37, 25, 76, 78)
        self.jump_l = pygame.transform.flip(self.jump_r, True, False)
        self.fall_r = self.game.load_image(PLAYER_JUMP_ANIM).get_image(152, 25, 67, 78)
        self.fall_l = pygame.transform.flip(self.fall_r, True, False)
        self.run_r = [self.game.load_image(PLAYER_RUN_ANIM).get_image(61, 40, 66, 72),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(147, 41, 65, 73),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(231, 40, 66, 74),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(316, 40, 66, 74),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(401, 38, 66, 76),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(486, 38, 66, 76),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(571, 38, 67, 76),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(658, 39, 80, 75),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(758, 40, 88, 72),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(866, 40, 97, 72),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(125, 140, 99, 74),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(244, 139, 95, 75),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(358, 138, 89, 76),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(466, 137, 79, 77),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(564, 136, 67, 78),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(650, 138, 66, 76),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(735, 138, 66, 75),
                    self.game.load_image(PLAYER_RUN_ANIM).get_image(820, 139, 66, 71)]
        self.run_l = []
        for i in range(0, len(self.run_r)):
            self.run_l.append(pygame.transform.flip(self.run_r[i], True, False))
    
    def jump(self):
        if self.on_floor:
            self.on_floor = False
            self.vel.y = -9
    
    def animate(self, sprite_list):
        now = pygame.time.get_ticks()
        if now - self.last_update > 45:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(sprite_list)
            self.image = sprite_list[self.current_frame]

    def update(self):
        self.acc = pygame.math.Vector2(0, GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = ACC
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + (self.acc / 2)
        if self.pos.x < WIDTH - 37 and self.pos.x > 37: # 37 is half of the player width
            self.rect.midbottom = self.pos
        else:
            self.pos.x = self.rect.midbottom[0]
            self.pos.y = self.rect.midbottom[1]
        # format: 'pos.x pos.y vel.x vel.y acc.x acc.y'
        game.sockconn("PLAYER" +
                    str(self.pos.x) + ' ' + 
                    str(self.pos.y) + ' ' + 
                    str(self.vel.x) + ' ' + 
                    str(self.vel.y) + ' ' + 
                    str(self.acc.x) + ' ' + 
                    str(self.acc.y) + ' ' +
                    str(self.on_floor))
        if self.on_floor:
            if self.vel.x > 1.5:
                # moving right
                self.animate(self.run_r)
            elif self.vel.x < -1.5:
                # moving left
                self.animate(self.run_l)
            else:
                # idle
                if self.vel.x > 0:
                    self.image = self.idle_r
                elif self.vel.x < 0:
                    self.image = self.idle_l
        else:
            if self.vel.y > 1:
                if self.vel.x > 0:
                    self.image = self.fall_r
                elif self.vel.x < 0:
                    self.image = self.fall_l
            elif self.vel.y < -1:
                if self.vel.x > 0:
                    self.image = self.jump_r
                elif self.vel.x < 0:
                    self.image = self.jump_l
        self.image.set_colorkey(pygame.Color('White'))

class Platform(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, w, h, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.load_images(filename, w, h)
        self.image = self.platform
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
    
    def load_images(self, filename, w, h):
        self.platform = self.game.load_image(filename).get_image(0, 0, w, h)
        self.platform = pygame.transform.scale(self.platform, (w // 3, h // 3))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.image = self.game.load_image(COIN_ANIM).get_image(32, 32, 64, 64)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(pygame.Color('Black'))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.attempt = 3
        self.dir = path.dirname(__file__)
        self.image_dir = path.join(self.dir, 'assets')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load(path.join(self.image_dir, BACKGROUND_IMAGE)).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT)
        self.score = 0
    
    def load_image(self, spritesheet):
        return Spritesheet(path.join(self.image_dir, spritesheet))
    
    def sockconn(self, text):
        stringencoded = text.encode('utf-8')
        clientSocket.send(stringencoded)

    def new(self):
        self.sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        # create Player
        self.player = Player(WIDTH / 2, HEIGHT / 4, self)
        self.sprites.add(self.player)
        # create Coin
        self.coin = Coin(100, HEIGHT - 50, self)
        #self.sprites.add(self.coin) # this will blit the coin
        self.coins.add(self.coin)
        # create Platforms
        for platform in PLATFORM_LIST:
            p = Platform(*platform, self)
            self.sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            if self.playing:
                self.draw()

    def update(self):
        self.sprites.update()
        if self.player.vel.y > 0: # player hits platform when falling
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if self.player.pos.y < hits[0].rect.bottom:
                    self.player.on_floor = True
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
        elif self.player.vel.y < 0: # player hits platform while jumping
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.vel.y = 0
        if pygame.sprite.spritecollide(self.player, self.coins, True):
            self.score += 1
            self.playing = False
        if self.score == 5:
            self.playing = False
            self.running = False
            self.over('Won')
        if self.attempt == 0:
            self.playing = False
            self.running = False
            self.over('Lost')

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("attempt")
                    self.attempt -= 1

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.sprites.draw(self.screen)
        self.draw_text(str(self.score), 20, pygame.Color(255, 255, 255), WIDTH / 2, 5)
        pygame.display.flip()

    def splash(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text("Labyrinth", 48, pygame.Color(255, 255, 255), WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play", 20, pygame.Color(255, 255, 255), WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS / 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def over(self, status):
        self.screen.blit(self.background, (0, 0))
        self.draw_text("You " + status, 48, pygame.Color(255, 255, 255), WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS / 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

game = Game()
game.splash()
while game.running:
    game.new()
pygame.quit()