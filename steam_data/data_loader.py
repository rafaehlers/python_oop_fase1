# Curso: Curso Superior de Tecnologia em Banco de Dados: Ênfase em Data Analytics
# Disciplina: Programação para Dados
# Projeto: Fase 1
# Aluno: Rafael de Menezes Ehlers
# Data: Agosto de 2024
# GitHub: https://github.com/rafaehlers/python_oop_fase1

import csv
from steam_data.exceptions import DataLoadException

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.games = []

    def load_data(self):
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.games.append(row)
        except FileNotFoundError:
            raise DataLoadException(f"Arquivo {self.file_path} não encontrado.")
        except Exception as e:
            raise DataLoadException(f"Erro ao carregar os dados: {e}")

        return self.games
