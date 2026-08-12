from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query

from models import Player
from player_stats import players

app = FastAPI(
    title="Mario Sluggers Player Stats API",
    description="Player batting, fielding, pitching, and running statistics",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Mario Sluggers API is running",
        "documentation": "/docs"
    }

@app.get("/players", response_model=List[Player])
def get_players():
    results = list(players.values())
    return results

@app.get("/players/{player_id}", response_model=Player)
def get_player(player_id: int):
    player = players.get(player_id)

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return player

@app.get("/colors/{color}", response_model=List[Player])
def get_player_color(player_color: str):
    results = [
        player
        for player in players.values()
        if player.color == player_color
    ]

    if not results:
        raise HTTPException(status_code=404, detail="No players found for that color")

    return results

@app.get("/rankings/{stat_name}", response_model=List[Player])
def rank_players(stat_name: str, descending: bool = True):
    valid_stats = ["batting", "fielding", "pitching", "running"]

    if stat_name not in valid_stats:
        raise HTTPException(status_code=400, detail={"message": "Invalid statistic","valid_statistics": list(valid_stats)})

    ranked_players = [
        player
        for player in players.values()
        if getattr(player, stat_name) is not None
    ]

    return sorted(
        ranked_players,
        key=lambda player: getattr(player, stat_name),
        reverse=descending
    )

@app.get("/stats/{stat_name}/{stat_value}", response_model=List[Player])
def get_stat_number(stat_name: str, stat_value: int):
    valid_stats = ["batting", "fielding", "pitching", "running"]
    
    if stat_name not in valid_stats:
        raise HTTPException(status_code=400, detail={"message": "Invalid statistic","valid_statistics": list(valid_stats)})

    if stat_value < 1 or stat_value > 10:
            raise HTTPException(status_code=400, detail={"message": "Invalid value"})
    
    results = [
            player
            for player in players.values()
            if getattr(player, stat_name) == stat_value
    ]

    if not results:
            raise HTTPException(status_code=404, detail="No players match this criteria")

    return results

@app.get("/better/{stat_name}/{stat_value}", response_model=List[Player])
def better_than(stat_name: str, stat_value: int):
    valid_stats = ["batting", "fielding", "pitching", "running"]

    if stat_name not in valid_stats:
        raise HTTPException(status_code=400, detail={"message": "Invalid statistic","valid_statistics": list(valid_stats)})
     
    if stat_value < 1 or stat_value > 10:
        raise HTTPException(status_code=400, detail={"message": "Invalid value"})

    results = [
        player
        for player in players.values()
        if getattr(player, stat_name) >= stat_value
    ]

    if not results:
                raise HTTPException(status_code=404, detail="No players match this criteria")
    
    return results

@app.get("/worse/{stat_name}/{stat_value}", response_model=List[Player])
def worse_than(stat_name: str, stat_value: int):
    valid_stats = ["batting", "fielding", "pitching", "running"]

    if stat_name not in valid_stats:
        raise HTTPException(status_code=400, detail={"message": "Invalid statistic","valid_statistics": list(valid_stats)})
     
    if stat_value < 1 or stat_value > 10:
        raise HTTPException(status_code=400, detail={"message": "Invalid value"})

    results = [
        player
        for player in players.values()
        if getattr(player, stat_name) <= stat_value
    ]

    if not results:
                raise HTTPException(status_code=404, detail="No players match this criteria")
    
    return results

@app.post("/players", response_model=Player, status_code=201)
def create_player(player: Player):
    if player.id in players:
        raise HTTPException(status_code=409,detail="A player with that ID already exists")

    for existing_player in players.values():
        if existing_player.name.lower() == player.name.lower():
            raise HTTPException(status_code=409,detail="A player with that name already exists")

    players[player.id] = player
    return player


@app.put("/players/{player_id}", response_model=Player)
def update_player(player_id: int, updated_player: Player):
    if player_id not in players:
        raise HTTPException(status_code=404, detail="player not found")

    if updated_player.id != player_id:
        raise HTTPException(status_code=400,detail="The player ID in the URL must match the request body")

    players[player_id] = updated_player
    return updated_player


@app.delete("/players/{player_id}")
def delete_player(player_id: int):
    player = players.pop(player_id, None)

    if player is None:
        raise HTTPException(status_code=404, detail="player not found")

    return {
        "message": "player deleted",
        "player": player,
    }