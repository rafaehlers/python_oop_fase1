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
        self.assertEqual(resultado, "Gratuitos: 15.00%, Pagos: 85.00%")

    def test_ano_com_mais_jogos(self):
        anos_max = self.stats.ano_com_mais_jogos()
        self.assertIn("2021", anos_max)

    def test_jogo_com_maior_nota_por_categoria(self):
        output_esperado = (
            "Single-player                  | DCS World Steam Edition                  | 19580.0\n"
            "Multi-player                   | DCS World Steam Edition                  | 19580.0\n"
            "PvP                            | DCS World Steam Edition                  | 19580.0\n"
            "Online PvP                     | DCS World Steam Edition                  | 19580.0\n"
            "LAN PvP                        | DCS World Steam Edition                  | 19580.0\n"
            "Co-op                          | DCS World Steam Edition                  | 19580.0\n"
            "Online Co-op                   | DCS World Steam Edition                  | 19580.0\n"
            "LAN Co-op                      | DCS World Steam Edition                  | 19580.0\n"
            "Captions available             | DCS World Steam Edition                  | 19580.0\n"
            "VR Support                     | DCS World Steam Edition                  | 19580.0\n"
            "Partial Controller Support     | DCS World Steam Edition                  | 19580.0\n"
            "Includes level editor          | DCS World Steam Edition                  | 19580.0\n"
            "Steam Leaderboards             | Modbox                                   | 191.0\n"
            "Steam Achievements             | Tormented Souls                          | 3229.0\n"
            "Steam Trading Cards            | Shot In The Dark                         | 78.0\n"
            "Shared/Split Screen PvP        | Modbox                                   | 191.0\n"
            "Steam Workshop                 | Modbox                                   | 191.0\n"
            "Stats                          | Virtual Army: Revolution                 | 13.0\n"
            "Remote Play Together           | Modbox                                   | 191.0\n"
            "Steam Cloud                    | That Time I Got Reincarnated as an Orc   | 243.0\n"
            "Full controller support        | Modbox                                   | 191.0\n"
            "Shared/Split Screen Co-op      | Modbox                                   | 191.0\n"
            "Shared/Split Screen            | Modbox                                   | 191.0\n"
            "Cross-Platform Multiplayer     | Modbox                                   | 191.0"
        )
        resultado = self.stats.jogo_com_maior_nota_por_categoria()
        self.assertEqual(resultado, output_esperado)

if __name__ == "__main__":
    unittest.main()