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

    def ano_com_mais_jogos(self):
        anos = defaultdict(int)
        for game in self.games:
            ano = game['Release date'].split(', ')[-1]
            anos[ano] += 1
        
        max_jogos = max(anos.values())
        anos_max = [ano for ano, count in anos.items() if count == max_jogos]
        return anos_max