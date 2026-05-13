import pygame

class EntityManager:
    def __init__(self):
        self.entities = []
        self.enemies_by_level = {}
    
    def add(self, entity):
        self.entities.append(entity)
    
    def remove(self, entity):
        self.entities.remove(entity)
        
    def update(self, tilemap, movement):
        for entity in self.entities:
            entity.update(tilemap, movement)
    
    def render(self, display, camera):
        for entity in self.entities:
            entity.render(display, camera)
    
    def clear(self):
        self.entities.clear()
        
    def get_entity_by_id(self, id):
        for entity in self.entities:
            if getattr(entity, "id", None) == id:
                return entity
        raise ValueError(f"Entity with id '{id}' not found.")
        
    def get_entities_by_type(self, cls):
        return [e for e in self.entities if isinstance(e, cls)]
    
    def is_empty(self):
        if not self.entities:
            return True
        return False
    
    def get_player_from_entities(self, cls):
        for entity in self.entities:
            if isinstance(entity, cls):
                return entity
    
    def entity_exists(self, entity):
        for entity_instance in self.entities:
            if entity == entity_instance:
                return True
        return False
    
    def remove_enemies_by_level_id(self, level_id):
        if level_id in self.enemies_by_level:
            for e in self.enemies_by_level[level_id]:
                if e in self.entities:
                    self.entities.remove(e)
            del self.enemies_by_level[level_id]