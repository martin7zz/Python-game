import pygame
from player import Player
from npc import NPC
from enemy import Enemy

class EntityLoader:
    def __init__(self, world):
        self.world = world
        
        self.player_data = None
        self.npc_data = None
        self.enemy_data = []
    
    def parse_level_entities(self):
        for entity in self.world.level["layerInstances"][2]["entityInstances"]:
            if entity["__identifier"] == "Player":
                for field in entity["fieldInstances"]:
                    if field["__identifier"] == "Is_Spawned":
                        if field["__value"] == False:
                            self.player_data = entity
                            self.isSpawned = False
            elif entity["__identifier"] == "Npc":
                self.npc_data = entity
            elif entity["__identifier"] == "Player_animation":
                self.player_animation_entity = entity
            elif entity["__identifier"] == "Enemy1":
                self.enemy_data.append(entity)
    
    def clear_player_data(self):
        self.player_data = None
    
    def clear_npc_data(self):
        self.npc_data = None
    
    def clear_enemy_data(self):
        self.enemy_data.clear()
        
    def player_spawn(self):
        self.isSpawned = True
        id = self.player_data["iid"]
        player_x, player_y = self.player_data["px"]
        player_world_x = self.world.level['worldX'] + player_x
        player_world_y = self.world.level['worldY'] + player_y
        player_width = self.player_data.get("width", 0)
        player_height = self.player_data.get("height", 0)
        player_size = (player_width, player_height)
        player = Player(self.world.game, (player_x, player_y), (player_world_x, player_world_y), player_size, self.isSpawned, id)
        
        self.world.entityManager.entities.append(player)
    
    def npc_spawn(self):
        id = self.npc_data["iid"]
        npc_x, npc_y = self.npc_data["px"]
        npc_world_x = self.world.level['worldX'] + npc_x
        npc_world_y = self.world.level['worldY'] + npc_y
        self.npc_width = self.npc_data.get("width", 0)
        self.npc_height = self.npc_data.get("height", 0)
        npc_size = (self.npc_width, self.npc_height)
        
        npc = NPC(self.world.game, (npc_x, npc_y), (npc_world_x,  npc_world_y), npc_size, id)
        
        self.world.entityManager.entities.append(npc)
        
    def enemy_spawn(self, level_id):
        enemies = []
        for enemy_instance in self.enemy_data:
            id = enemy_instance["iid"]
            enemy_x, enemy_y = enemy_instance["px"]
            enemy_world_x = self.world.level['worldX'] + enemy_x
            enemy_world_y = self.world.level['worldY'] + enemy_y
            enemy_width = enemy_instance.get("width", 0)
            enemy_height = enemy_instance.get("height", 0)
            enemy_size = (enemy_width, enemy_height)
            
            enemy = Enemy(self.world.game, (enemy_x, enemy_y), (enemy_world_x, enemy_world_y), enemy_size, id)
            enemies.append(enemy)
            self.world.entityManager.entities.append(enemy)
        
        self.world.entityManager.enemies_by_level[level_id] = enemies
            
        
        
        
        
        
        
        
        
        