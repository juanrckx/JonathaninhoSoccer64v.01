import json
import os
from datetime import datetime


class StatsManager:
    def __init__(self, stats_file="game_stats.json"):
        self.stats_file = stats_file
        self.stats = self.load_stats()

    def load_stats(self):
        """Carga las estadísticas desde el archivo JSON"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error cargando estadísticas: {e}")

        # Estructura inicial si no existe el archivo
        return {
            "total_games": 0,
            "total_goals": 0,
            "games": [],
            "players": {},
            "teams": {},
            "records": {
                "most_goals_game": 0,
                "best_accuracy": 0,
                "longest_win_streak": 0
            }
        }

    def save_stats(self):
        """Guarda las estadísticas en el archivo JSON"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando estadísticas: {e}")

    def add_game(self, game_config, player_stats, score):
        """Agrega estadísticas de un juego completado"""
        game_data = {
            "timestamp": datetime.now().isoformat(),
            "score": score.copy(),
            "config": game_config.copy(),
            "player_stats": player_stats.copy(),
            "winner": self.determine_winner(score)
        }

        # Actualizar estadísticas generales
        self.stats["total_games"] += 1
        self.stats["total_goals"] += score["local"] + score["visit"]
        self.stats["games"].append(game_data)

        # Mantener solo los últimos 100 juegos
        if len(self.stats["games"]) > 100:
            self.stats["games"] = self.stats["games"][-100:]

        # Actualizar estadísticas de jugadores y equipos
        self.update_player_stats(game_config, player_stats, score)
        self.update_team_stats(game_config, score)
        self.update_records(game_config, player_stats, score)

        self.save_stats()

    def determine_winner(self, score):
        """Determina el ganador del juego"""
        if score["local"] > score["visit"]:
            return "local"
        elif score["local"] < score["visit"]:
            return "visit"
        else:
            return "draw"

    def update_player_stats(self, game_config, player_stats, score):
        """Actualiza estadísticas de jugadores individuales"""
        for team in ["local", "visit"]:
            team_data = game_config[f"team_{team}"]
            shooter_idx = game_config[f"shooter_{team}"]
            goalie_idx = game_config[f"goalie_{team}"]

            shooter = team_data["shooters"][shooter_idx]
            goalie = team_data["goalies"][goalie_idx]

            # Estadísticas del artillero
            self.update_shooter_stats(shooter, player_stats[team], team_data["name"])

            # Estadísticas del portero
            opponent = "visit" if team == "local" else "local"
            self.update_goalie_stats(goalie, player_stats[opponent], team_data["name"])

    def update_shooter_stats(self, shooter, stats, team_name):
        """Actualiza estadísticas de un artillero"""
        shooter_name = shooter["name"]
        if shooter_name not in self.stats["players"]:
            self.stats["players"][shooter_name] = {
                "role": "shooter",
                "team": team_name,
                "games": 0,
                "goals": 0,
                "shots": 0,
                "timeouts": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0
            }

        player = self.stats["players"][shooter_name]
        player["games"] += 1
        player["goals"] += stats["goals"]
        player["shots"] += stats["shots"]
        player["timeouts"] += stats.get("timeouts", 0)

    def update_goalie_stats(self, goalie, opponent_stats, team_name):
        """Actualiza estadísticas de un portero"""
        goalie_name = goalie["name"]
        if goalie_name not in self.stats["players"]:
            self.stats["players"][goalie_name] = {
                "role": "goalie",
                "team": team_name,
                "games": 0,
                "goals_received": 0,
                "saves": 0,
                "clean_sheets": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0
            }

        goalie_stats = self.stats["players"][goalie_name]
        goalie_stats["games"] += 1
        goalie_stats["goals_received"] += opponent_stats["goals"]
        goalie_stats["saves"] += (opponent_stats["shots"] - opponent_stats["goals"])

        # Clean sheet (cero goles recibidos)
        if opponent_stats["goals"] == 0:
            goalie_stats["clean_sheets"] += 1

    def update_team_stats(self, game_config, score):
        """Actualiza estadísticas de equipos"""
        for team in ["local", "visit"]:
            team_data = game_config[f"team_{team}"]
            team_name = team_data["name"]

            if team_name not in self.stats["teams"]:
                self.stats["teams"][team_name] = {
                    "games": 0,
                    "wins": 0,
                    "losses": 0,
                    "draws": 0,
                    "goals_for": 0,
                    "goals_against": 0
                }

            team_stats = self.stats["teams"][team_name]
            team_stats["games"] += 1
            team_stats["goals_for"] += score[team]
            team_stats["goals_against"] += score["visit" if team == "local" else "local"]

            # Actualizar wins/losses/draws
            if score["local"] > score["visit"]:
                if team == "local":
                    team_stats["wins"] += 1
                else:
                    team_stats["losses"] += 1
            elif score["local"] < score["visit"]:
                if team == "visit":
                    team_stats["wins"] += 1
                else:
                    team_stats["losses"] += 1
            else:
                team_stats["draws"] += 1

    def update_records(self, game_config, player_stats, score):
        """Actualiza récords del juego"""
        total_goals = score["local"] + score["visit"]

        # Récord de más goles en un juego
        if total_goals > self.stats["records"]["most_goals_game"]:
            self.stats["records"]["most_goals_game"] = total_goals

        # Mejor precisión
        for team in ["local", "visit"]:
            accuracy = (player_stats[team]["goals"] / max(player_stats[team]["shots"], 1)) * 100
            if accuracy > self.stats["records"]["best_accuracy"]:
                self.stats["records"]["best_accuracy"] = accuracy

    def get_player_stats(self, player_name):
        """Obtiene estadísticas de un jugador específico"""
        return self.stats["players"].get(player_name)

    def get_team_stats(self, team_name):
        """Obtiene estadísticas de un equipo específico"""
        return self.stats["teams"].get(team_name)

    def get_recent_games(self, count=10):
        """Obtiene los juegos más recientes"""
        return self.stats["games"][-count:] if self.stats["games"] else []

    def get_top_scorers(self, limit=5):
        """Obtiene los máximos goleadores"""
        shooters = {name: data for name, data in self.stats["players"].items() if data["role"] == "shooter"}
        return sorted(shooters.items(), key=lambda x: x[1]["goals"], reverse=True)[:limit]

    def get_top_goalies(self, limit=3):
        """Obtiene los mejores porteros por efectividad"""
        goalies = {name: data for name, data in self.stats["players"].items() if data["role"] == "goalie"}
        return sorted(goalies.items(),
                      key=lambda x: (x[1]["saves"] / max(x[1]["saves"] + x[1]["goals_received"], 1)) * 100,
                      reverse=True)[:limit]