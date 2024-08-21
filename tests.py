# Curso: Curso Superior de Tecnologia em Banco de Dados: Ênfase em Data Analytics
# Disciplina: Programação para Dados
# Projeto: Fase 1
# Aluno: Rafael de Menezes Ehlers
# Data: Agosto de 2024
# GitHub: https://github.com/rafaehlers/python_oop_fase1

import unittest
from game_data.data_loader import DataLoader
from game_data.game_statistics import GameStatistics

class TestSteamData(unittest.TestCase):

    def setUp(self):
        loader = DataLoader("dados_teste.csv")
        self.games = loader.load_data()
        self.stats = GameStatistics(self.games)

    def test_percentual_jogos_gratuitos_pagos(self):
        resultado = self.stats.percentual_jogos_gratuitos_pagos()
        self.assertEqual(resultado, "Gratuitos: 17.39%, Pagos: 82.61%")

    def test_ano_com_mais_jogos(self):
        anos_max = self.stats.ano_com_mais_jogos()
        self.assertIn("2022", anos_max)

if __name__ == "__main__":
    unittest.main()