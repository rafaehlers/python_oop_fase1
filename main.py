# Curso: Curso Superior de Tecnologia em Banco de Dados: Ênfase em Data Analytics
# Disciplina: Programação para Dados
# Projeto: Fase 1
# Aluno: Rafael de Menezes Ehlers
# Data: Agosto de 2024
# GitHub: https://github.com/rafaehlers/python_oop_fase1

from game_data.data_loader import DataLoader
from game_data.game_statistics import GameStatistics

def main():
    loader = DataLoader('steam_games.csv')
    games = loader.load_data()

    stats = GameStatistics(games)
    
    # Responde as perguntas
    print("#"*50)
    print("Percentual de jogos gratuitos e pagos:")
    print(stats.percentual_jogos_gratuitos_pagos())
    print("#"*50)
    print(f"Ano com mais lançamentos: {stats.ano_com_mais_jogos()}")
    print("#"*50)
    print("Jogo com maior nota, por categoria:")
    print("CATEGORIA                      | NOME DO JOGO                             | NOTA")
    print(stats.jogo_com_maior_nota_por_categoria())

if __name__ == "__main__":
    main()