from enum import Enum
from typing import List, Optional

class TileType(Enum):
    WAN = "Wan"
    TONG = "Tong"
    SUO = "Suo"
    WIND = "Wind"
    DRAGON = "Dragon"

class Tile:
    def __init__(self, tile_type: TileType, value: int):
        self.type = tile_type
        self.value = value
        self._validate()

    def _validate(self):
        if self.type in [TileType.WAN, TileType.TONG, TileType.SUO]:
            if not 1 <= self.value <= 9:
                raise ValueError(f"Invalid value {self.value} for {self.type}")
        elif self.type == TileType.WIND:
            if not 1 <= self.value <= 4:  # 东南西北
                raise ValueError(f"Invalid wind value {self.value}")
        elif self.type == TileType.DRAGON:
            if not 1 <= self.value <= 3:  # 中发白
                raise ValueError(f"Invalid dragon value {self.value}")

    def __str__(self):
        return f"{self.type.value}{self.value}"

    def __repr__(self):
        return f"Tile({self.type.value}, {self.value})"

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.type == other.type and self.value == other.value

    def __hash__(self):
        return hash((self.type, self.value))

class TileSet:
    """麻将牌组管理类"""
    @staticmethod
    def create_full_set() -> List[Tile]:
        """创建一副完整的麻将牌"""
        tiles = []
        # 数牌 (万筒条)
        for tile_type in [TileType.WAN, TileType.TONG, TileType.SUO]:
            for value in range(1, 10):
                for _ in range(4):  # 每种牌4张
                    tiles.append(Tile(tile_type, value))
        
        # 风牌
        for value in range(1, 5):
            for _ in range(4):
                tiles.append(Tile(TileType.WIND, value))
        
        # 三元牌
        for value in range(1, 4):
            for _ in range(4):
                tiles.append(Tile(TileType.DRAGON, value))
        
        return tiles
