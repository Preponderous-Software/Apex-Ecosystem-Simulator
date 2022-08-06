import random
import pygame


#  @author Daniel McCoy Stephenson
#  @since August 5th, 2022
class SoundService:
    def __init__(self):
        self.reproduceSoundEffect = pygame.mixer.Sound("src/pop.wav")
        self.deathSoundEffect = pygame.mixer.Sound("src/pain.wav")

        self.volumeFactor = 0.01
        self.minVolume = 1
        self.maxVolume = 10

    def playReproduceSoundEffect(self):
        self.reproduceSoundEffect.set_volume(self.volumeFactor * random.randrange(self.minVolume, self.maxVolume))
        pygame.mixer.Sound.play(self.reproduceSoundEffect)
    
    def playDeathSoundEffect(self):
        self.deathSoundEffect.set_volume(self.volumeFactor * random.randrange (self.minVolume, self.maxVolume))
        pygame.mixer.Sound.play(self.deathSoundEffect)