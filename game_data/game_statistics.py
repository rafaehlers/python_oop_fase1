# Curso: Curso Superior de Tecnologia em Banco de Dados: Ênfase em Data Analytics
# Disciplina: Programação para Dados
# Projeto: Fase 1
# Aluno: Rafael de Menezes Ehlers
# Data: Agosto de 2024
# GitHub: https://github.com/rafaehlers/python_oop_fase1

from collections import defaultdict

class GameStatistics:
    def __init__(self, games):
        self.games = games

    def percentual_jogos_gratuitos_pagos(self):
        gratuitos = sum(1 for game in self.games if float(game['Price']) == 0)
        pagos = len(self.games) - gratuitos
        total = len(self.games)
        return f"Gratuitos: {((gratuitos / total) * 100):.2f}%, Pagos: {((pagos / total) * 100):.2f}%"

    def ano_com_mais_jogos(self):
        anos = defaultdict(int)
        for game in self.games:
            ano = game['Release date'].split(', ')[-1]
            anos[ano] += 1
        
        max_jogos = max(anos.values())
        anos_max = [ano for ano, count in anos.items() if count == max_jogos]
        
        # Se houver apenas um ano, retorna diretamente como string
        if len(anos_max) == 1:
            return anos_max[0]
    
        # Se houver mais de um ano (empate), retorna como string concatenada
        return ', '.join(anos_max)

    def jogo_com_maior_nota_por_categoria(self):
        categorias = defaultdict(lambda: {'jogo': '', 'nota': 0})
        
        for game in self.games:
            game_score = float(game.get('User score', 0))
            for categoria in game['Categories'].split(','):
                categoria = categoria.strip()
                if categoria and game['Name'] and game_score > categorias[categoria]['nota']:
                    categorias[categoria] = {'jogo': game['Name'], 'nota': game_score}

        # Formata a saída para uma string legível, ignorando categorias ou jogos vazios
        output = []
        for categoria, info in categorias.items():
            if info['jogo']:  # Verifica se o nome do jogo não está vazio
                output.append(f"{categoria: <30} | {info['jogo']: <40} | {info['nota']}")

        return '\n'.join(output)