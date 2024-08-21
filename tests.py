# Curso: Curso Superior de Tecnologia em Banco de Dados: Ênfase em Data Analytics
# Disciplina: Programação para Dados
# Projeto: Fase 1
# Aluno: Rafael de Menezes Ehlers
# Data: Agosto de 2024

import unittest
from steam_data.data_loader import DataLoader
from steam_data.game_statistics import GameStatistics

class TestSteamData(unittest.TestCase):

    def setUp(self):
        loader = DataLoader("dados_teste.csv")
        self.games = loader.load_data()
        self.stats = GameStatistics(self.games)

    def test_percentual_jogos_gratuitos_pagos(self):
        resultado = self.stats.percentual_jogos_gratuitos_pagos()
        self.assertEqual(resultado['Gratuitos'], 50)  # Exemplo de teste

    def test_ano_com_mais_jogos(self):
        anos_max = self.stats.ano_com_mais_jogos()
        self.assertIn("2022", anos_max)  # Exemplo de teste

    def test_jogo_com_maior_nota_por_categoria(self):
        categorias = self.stats.jogo_com_maior_nota_por_categoria()
        self.assertEqual(categorias['Action']['jogo'], "Game X")  # Exemplo de teste

if __name__ == "__main__":
    unittest.main()