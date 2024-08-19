from steam_data.data_loader import DataLoader
from steam_data.game_statistics import GameStatistics

def main():
    loader = DataLoader('steam_games.csv')
    games = loader.load_data()

    stats = GameStatistics(games)
    
    # Responder perguntas
    print("Percentual de jogos gratuitos e pagos:")
    print(stats.percentual_jogos_gratuitos_pagos())

    print("Ano com mais lançamentos:")
    print(stats.ano_com_mais_jogos())

if __name__ == "__main__":
    main()