import pygame
import os
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic
from pytmx.util_pygame import load_pygame


class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()

		#telecharge l'image de la maison
		self.tmx_data = load_pygame('../data/map.tmx')

		#layer constants
		self.LAYERS_HOUSE_BOTTOM = ['HouseFloor', 'HouseFurnitureBottom']
		self.LAYERS_MAIN = ['HouseWalls', 'HouseFurnitureTop']

		self.setup()
		self.overlay = Overlay(self.player)


#process_layer cette fonction me permet de construire la maison
	def process_layer(self, layer_names, layer_group, tile_size, all_sprites):
		for layer in layer_names:
			for x, y, surf in self.tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * tile_size, y * tile_size), surf, all_sprites, layer_group)
	def setup(self):
		self.process_layer(self.LAYERS_HOUSE_BOTTOM, LAYERS['house bottom'], TILE_SIZE, self.all_sprites)
		self.process_layer(self.LAYERS_MAIN, LAYERS['main'], TILE_SIZE, self.all_sprites)

		#Fence
		self.player = Player((640,360), self.all_sprites)
		path_floor = os.path.join('..', 'graphics', 'world', 'ground.png')
		Generic(
			pos=(0,0),
			surf = pygame.image.load(path_floor).convert_alpha(),
			groups= self.all_sprites,
			z=LAYERS['ground'])
	def run(self,dt):
		self.display_surface.fill('black')
		self.all_sprites.customize_draw(self.player)
		self.all_sprites.update(dt)

		self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
