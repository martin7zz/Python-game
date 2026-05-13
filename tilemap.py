import pygame, math
from tile import Tile

class Tilemap(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        
        self.render_tiles_by_level = {}
        self.collision_tilemaps = {}
        self.tilemap = {}
        
        self.game = game
        self.tile_size = 0
        
    def render(self, display, camera):
        for level_Data in self.render_tiles_by_level.items():
            for tile in level_Data[1]:
                tile.draw(display, camera)
                # print(display, camera)
    
    def build_neighbor_offsets(self, width, height):
        half_w = math.ceil(width / 2 / self.tile_size)
        half_h = math.ceil(height / 2 / self.tile_size)
        
        offsets = []
        
        for dy in range(-half_h, half_h + 1):
            for dx in range(-half_w, half_w + 1):
                offsets.append((dx, dy))
        
        return offsets
    
    def render_tiles(self, autoTile_layer, autoTile_image, world_offset):
        tiles = pygame.sprite.Group()
        self.tile_size = autoTile_layer['__gridSize']
        
        for tile_data in autoTile_layer.get('autoLayerTiles', []):
            tile_px_x, tile_px_y = tile_data["px"]
            
            tile_world_x = tile_px_x + world_offset[0]
            tile_world_y = tile_px_y + world_offset[1]
            
            src = tile_data['src']
            
            tile = Tile(
                (tile_world_x, tile_world_y),
                (tile_px_x, tile_px_y),
                src,
                autoTile_image,
                self.tile_size
            )
            
            tiles.add(tile)
        return tiles
    
    def collision_grid(self, tile_layer, world_offset):
        collision_map = {}
        
        grid_size = tile_layer['__gridSize']
        width = tile_layer['__cWid']
        
        csv = tile_layer['intGridCsv']
        
        for i, value in enumerate(csv):
            if value == 0:
                continue
            
            x = i % width
            y = i // width
            
            world_x = x + (world_offset[0] // grid_size)
            world_y = y + (world_offset[1] // grid_size)
            
            collision_map[(world_x, world_y)] = value
        
        return collision_map
    
    def load_tilemap(self, current_level):
        self.tilemap = self.collision_tilemaps[current_level]
    
    def load_from_layer(self, level, level_id):
        tile_layer = next(
            layer for layer in level['layerInstances']
            if layer['__identifier'] == 'Collisions'
        )
        
        autoTile_layer = next(
            layer for layer in level['layerInstances']
            if layer['__identifier'] == 'Terrain_AutoLayer'
        )
        
        autoTileset_image = pygame.image.load(
            autoTile_layer['__tilesetRelPath']
        ).convert_alpha()
        
        self.world_offset = (level['worldX'], level['worldY'])
        
        render_tiles = self.render_tiles(
            autoTile_layer,
            autoTileset_image,
            self.world_offset
        )
        
        collision_map = self.collision_grid(
            tile_layer,
            self.world_offset
        )
        
        self.render_tiles_by_level[level_id] = render_tiles
        self.collision_tilemaps[level_id] = collision_map
    
    
    def extract(self, tiles, id_pairs, keep=False):
        matches = []
        for tile in tiles.sprites():
            if (tile.type, tile.variant) in id_pairs:
                matches.append(tile)
                if not keep:
                    tiles.remove(tile)
        return matches
    
    def solid_check(self, pos):
        # Check if a position intersects with a solid tile
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            return self.tilemap[tile_loc]
        return None
    
    def physics_rects_around(self, rect):
        rects = []

        left = int(rect.left // self.tile_size)
        right = int(rect.right // self.tile_size)
        top = int(rect.top // self.tile_size)
        bottom = int(rect.bottom // self.tile_size)

        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                if (x, y) in self.tilemap:
                    rects.append(
                        pygame.Rect(
                            x * self.tile_size,
                            y * self.tile_size,
                            self.tile_size,
                            self.tile_size
                        )
                    )

        return rects