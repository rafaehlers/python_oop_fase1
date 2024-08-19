from steam_data.data_loader import DataLoader

def main():
    loader = DataLoader('steam_games.csv')
    games = loader.load_data()