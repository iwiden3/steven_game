"""
Sprite strip animator demo
 
Requires spritesheet.spritesheet and the Explode1.bmp through Explode5.bmp
found in the sprite pack at
http://lostgarden.com/2005/03/download-complete-set-of-sweet-8-bit.html
 
I had to make the following addition to method spritesheet.image_at in
order to provide the means to handle sprite strip cells with borders:
 
            elif type(colorkey) not in (pygame.Color,tuple,list):
                colorkey = image.get_at((colorkey,colorkey))
"""
import sys
import os, pygame
from pygame.locals import *
import spritesheet
from sprite_strip_anim import SpriteStripAnim

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def main():
    pygame.init()
    surface = pygame.display.set_mode((1000,1000))
    BackGround = Background('beach.png', [0,0])
    FPS = 120
    frames = FPS / 6
    strips = [
	    SpriteStripAnim('gems.png', (0,0,32,32), 3, 1, True, frames),
        SpriteStripAnim('gems.png', (96,0,32,32), 3, 1, True, frames),
	]
    black = Color('black')
    bg_music = load_sound('EndingThemeSong.mp3')
    clock = pygame.time.Clock()
    n = 0
    strips[n].iter()
    image = strips[n].next()
    pygame.mixer.music.load("EndingThemeSong.mp3")
    pygame.mixer.music.play(0)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
		            return
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                   sys.exit()
                elif event.key == K_RETURN:
		            n += 1
		            if n >= len(strips):
		                n = 0
		            strips[n].iter()
        surface.fill(black)
        surface.blit(BackGround.image, BackGround.rect)
        surface.blit(image, (0,0))
        pygame.display.flip()
        image = strips[n].next()
        clock.tick(FPS)

if __name__ == '__main__': main()
