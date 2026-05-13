import pygame
from tilemap import Tilemap
from entityLoader import EntityLoader
from entityManager import EntityManager

from player import Player
from npc import NPC
from enemy import Enemy

class World:
    def __init__(self, game, screen, display, level_data):
        self.game = game
        self.level_data = level_data
        self.levels = self.level_data['levels']
        
        self.entityManager = EntityManager()
        self.entityLoader = EntityLoader(self)
        
        self.loaded_levels = []
        self.current_level = None
        self.level = None
        
        self.get_initial_level()
        
        self.display = display
        self.screen = screen
        
        self.SKYCOLOR = (135, 206, 235)
        
        
        self.current_level_index = 0
        
        self.x_shift = 0
        self.y_shift = 0
        
        self.scroll = [0, 0]
        
    
    def run(self):
        self.display.fill(self.SKYCOLOR)
        
        map_left, map_right, map_top, map_bottom = self.calculate_map_boundaries()
        
        camera = self.update_camera(map_left, map_right, map_top, map_bottom, self.player)
        
        self.player.update(self.tilemap, (self.player.movement[1] - self.player.movement[0], 0))
        
        
        
        
        self.load_nearby_levels(self.player)
        
        # print(f'Enemies by level count: {len(self.entityManager.enemies_by_level[self.current_level['identifier']])}')
        
        
        self.tilemap.render(self.display, camera)
        
        for npc in self.npc:
            npc.render(self.display, camera)
        
        for enemy in self.enemies.copy():
            IsDead = enemy.update(self.tilemap, (0, 0))
            enemy.render(self.display, camera)
            # print(f'Enemy position: {enemy.pos}')
            if IsDead:
                self.enemies.remove(enemy)
                self.entityManager.entities.remove(enemy)
        
        self.player.render(self.display, camera)
        
        # self.entities.render(self.display, camera)
        
        self.draw(self.screen)
        
    def calculate_map_boundaries(self):
        map_left = float('inf')
        map_right = float('-inf')
        map_top = float('inf')
        map_bottom = float('-inf')
        
        for level in self.levels:
            level_x, level_y = level['worldX'], level['worldY']
            level_width, level_height = level['pxWid'], level['pxHei']
            
            map_left = min(map_left, level_x)
            map_top = min(map_top, level_y)
            map_right = max(map_right, level_x + level_width)
            map_bottom = max(map_bottom, level_y + level_height)
            
        return map_left, map_right, map_top, map_bottom
    
    def update_camera(self, map_left, map_right, map_top, map_bottom, player):
        
        target_scroll_x = -(player.pos[0] + player.size[0] / 2) + self.display.get_width() / 2
        target_scroll_y = -(player.pos[1] + player.size[1] / 2) + self.display.get_height() / 2
        
        if player.rect().centerx < map_left + self.display.get_width() / 2:
            target_scroll_x = -map_left
        elif player.rect().centerx > map_right - self.display.get_width() / 2:
            target_scroll_x = -(map_right - self.display.get_width())

        if player.rect().centery < map_top + self.display.get_height() / 2:
            target_scroll_y = -map_top
        elif player.rect().centery > map_bottom - self.display.get_height() / 2:
            target_scroll_y = -(map_bottom - self.display.get_height())
        
        render_scroll = (round(target_scroll_x), round(target_scroll_y))
        
        return (render_scroll)
    
    # NEEDS TO BE FIXED
    def load_nearby_levels(self, player, range_x = 10000, range_y = 10000):
        # unlaod levels based on player position
        player_x = player.rect().x
        player_y = player.rect().y
        
        self.loaded_levels = [level for level in self.loaded_levels if self.is_within_range(self.get_level_boundaries(level), player_x, player_y, range_x, range_y)]
        
        for level in self.levels:
            level_id = level['identifier']
            current_level_id = self.current_level['identifier']
            
            level_boundaries = self.get_level_boundaries(level)
            
            # Load nearby levels that are not already loaded
            if self.is_within_range(level_boundaries, player_x, player_y, range_x, range_y) and level not in self.loaded_levels:
                self.load_level(level)
                
            if level_id != current_level_id:
                if level_boundaries['minX'] <= player_x <= level_boundaries['maxX'] and level_boundaries['minY'] <= player_y <= level_boundaries['maxY']:
                    self.current_level = level # Update the current level based on the player's position
                    current_level_id = self.current_level['identifier']
                    # print(current_level_id)
                    # print(self.current_level['identifier'])
                    self.enemies = self.entityManager.enemies_by_level.get(current_level_id)
                    
                    # could be and error together with the other tilemap loader
                    self.tilemap.load_tilemap(current_level_id)
                
        # Now, unload levels that are no longer within range
        for level_id, level_tiles in list(self.tilemap.render_tiles_by_level.items()):
            level = self.get_level_by_id(level_id)
            level_boundaries = self.get_level_boundaries(level)
            
            if not self.is_within_range(level_boundaries, player_x, player_y, range_x, range_y) and level_id != current_level_id:
                level_tiles.empty()  # Unload tiles by emptying the sprite group
                # self.loaded_levels.remove(level)
                del self.tilemap.render_tiles_by_level[level_id]
                
                self.entityManager.remove_enemies_by_level_id(level_id)
                
    def get_level_boundaries(self, level):
            return {
                'minX': level['worldX'],
                'maxX': level['worldX'] + level['pxWid'],
                'minY': level['worldY'],
                'maxY': level['worldY'] + level['pxHei']
            }
            
    def get_level_by_id(self, level_id):
        return next((level for level in self.levels if level['identifier'] == level_id), None)
    
    # NEEDS TO BE FIXED
    def is_within_range(self, level_boundaries, player_x, player_y, range_x, range_y):
        within_horizontal_range = (level_boundaries['minX'] - range_x <= player_x <= level_boundaries['maxX'] + range_x)
        within_vertical_range = (level_boundaries['minY'] - range_y <= player_y <= level_boundaries['maxY'] + range_y)
        return within_horizontal_range and within_vertical_range
    
    def get_initial_level(self):
        current_level = next((level for level in self.levels if level['identifier'] == "Level_2"), None)
        
        self.current_level = current_level
        
        # change location
        self.tilemap = Tilemap(self.game)
        
        self.load_level(self.current_level)
    
    def load_level(self, level):
        # for now
        self.game.audio_manager.music_manager.play('background.mp3', -1, 0.1)
        
        # print(f"Current level fddfd after change: {self.current_level['identifier']}")
        
        # probably uneeded, fix later. remove from every place and add normal level to the functions
        self.level = level
        
        if level not in self.loaded_levels:
            self.setup_level()
            self.loaded_levels.append(level)
        
        # for level in self.loaded_levels:
            # print(level['identifier'])    
    
    def setup_level(self):
        level_id = self.level['identifier']
        self.entityLoader.clear_npc_data()
        self.entityLoader.clear_enemy_data()
        
        #FOR NOW ONLY
        self.entityLoader.parse_level_entities()
        
        if not self.entityManager.get_player_from_entities(Player):
            self.entityLoader.player_spawn()
            self.player = self.entityManager.get_player_from_entities(Player)
        
        # if self.level['identifier'] == self.current_level['identifier']:
        #     self.entityLoader.enemy_spawn()
        
        self.entityLoader.enemy_spawn(level_id)
        
        # self.entityLoader.npc_spawn()
        
        
        
        self.enemies = self.entityManager.enemies_by_level.get(self.current_level['identifier'], [])
        self.npc = self.entityManager.get_entities_by_type(NPC)
        
        if level_id not in self.tilemap.render_tiles_by_level:
            self.tilemap.load_from_layer(self.level, level_id)
        
        # maybe not needed. could be loading the tilemap twice
        if level_id == self.current_level['identifier']:
            self.tilemap.load_tilemap(self.current_level['identifier'])
            
    def get_level_from_menu(self, levelID):
        chosen_level = self.get_level_by_id(levelID)
        
        self.current_level = chosen_level
        
        self.entityManager.entities.clear()
        
        self.entityLoader.clear_player_data()
        self.entityLoader.clear_npc_data()
        self.entityLoader.clear_enemy_data()
        
        if chosen_level in self.loaded_levels:
            self.loaded_levels.remove(chosen_level)
        
        # print(f"Current level after change: {self.current_level['identifier']}")
        # print(f"Current level after change: {chosen_level['identifier']}")
        
        self.load_level(chosen_level)
        
        
    def draw(self, screen):
        screen.blit(self.display, (0, 0))

    def update_resolution(self, width, height, screen):
        self.screen = screen
        self.display = pygame.Surface((width, height), pygame.SRCALPHA)
        
    