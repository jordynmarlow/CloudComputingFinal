import pygame
import random

# Settings
WIDTH = 800
HEIGHT = 500
FPS = 60
TITLE = 'Labyrinth'
ACC = 0.5
FRICTION = -0.15
GRAVITY = 0.2
FONT = 'Arial'

PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (250, HEIGHT * 3 / 4 - 20, WIDTH / 2, 40)]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(pygame.Color('Yellow'))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.pos.x = x
        self.pos.y = y
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.rect.midbottom = self.pos
        self.on_floor = False
    
    def jump(self):
        if self.on_floor:
            self.on_floor = False
            self.vel.y = -7

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
        if self.pos.x < WIDTH and self.pos.x > 0:
            self.rect.midbottom = self.pos
        else:
            self.pos.x = self.rect.midbottom.x
            self.pos.y = self.rect.midbottom.y

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color(0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(pygame.Color('Red'))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT)
        self.score = 0

    def new(self):
        self.sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()
        # create Player
        self.player = Player(WIDTH / 2, HEIGHT / 2, self)
        self.sprites.add(self.player)
        # create Flag
        self.flag = Flag(100, HEIGHT - 40, self)
        self.sprites.add(self.flag)
        self.flags.add(self.flag)
        # create Platforms
        for platform in PLATFORM_LIST:
            p = Platform(*platform)
            self.sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
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
        if pygame.sprite.spritecollide(self.player, self.flags, False):
            self.score += 1
            self.playing = False
        if self.score == 5:
            self.running = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # pause event?
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self):
        self.screen.fill(pygame.Color('Black'))
        self.sprites.draw(self.screen)
        self.draw_text(str(self.score), 20, pygame.Color(255, 255, 255), WIDTH / 2, 5)
        pygame.display.flip()

    def splash(self):
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

    def over(self):
        if not self.running:
            return
        self.draw_text("Game Over. You Won.", 48, pygame.Color(255, 255, 255), WIDTH / 2, HEIGHT / 2)
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
game.splash() # show splash screen
while game.running:
    game.new()
game.over()
pygame.quit()