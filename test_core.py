import pytest
from chaoshan_mahjong_ai import ChaoshanMJPlugin
from chaoshan_mahjong_ai.tiles import Tile, TileType, TileSet

def test_tile_selection():
    plugin = ChaoshanMJPlugin()
    available_tiles = TileSet.create_full_set()
    selected = plugin.tile_selection(available_tiles)
    
    assert len(selected) == 13
    assert all(isinstance(tile, Tile) for tile in selected)

def test_intelligent_discard():
    plugin = ChaoshanMJPlugin()
    hand_tiles = [
        Tile(TileType.WAN, 1),
        Tile(TileType.WAN, 2),
        Tile(TileType.WAN, 3),
        Tile(TileType.TONG, 5),
        Tile(TileType.SUO, 7),
    ]
    
    discarded = plugin.intelligent_discard(hand_tiles)
    assert isinstance(discarded, Tile)
    assert discarded in hand_tiles

def test_tile_validation():
    with pytest.raises(ValueError):
        Tile(TileType.WAN, 10)  # Invalid value
    
    with pytest.raises(ValueError):
        Tile(TileType.WIND, 5)  # Invalid wind value

def test_probability_engine():
    plugin = ChaoshanMJPlugin()
    tiles = [
        Tile(TileType.WAN, 1),
        Tile(TileType.WAN, 2),
        Tile(TileType.WAN, 3),
    ]
    
    scores = plugin.prob_engine.calculate_tile_scores(tiles)
    assert len(scores) == len(tiles)
    assert all(isinstance(score, float) for score in scores.values())
