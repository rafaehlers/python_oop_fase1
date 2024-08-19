from collections import defaultdict

class GameStatistics:
    def __init__(self, games):
        self.games = games

    def percentual_jogos_gratuitos_pagos(self):
        gratuitos = sum(1 for game in self.games if float(game['Price']) == 0)
        pagos = len(self.games) - gratuitos
        total = len(self.games)
        return {
            "gratuitos": (gratuitos / total) * 100,
            "pagos": (pagos / total) * 100
        }
