# Curso: Curso Superior de Tecnologia em Banco de Dados: Ênfase em Data Analytics<br>
# Disciplina: Programação para Dados<br>
# Projeto: Fase 2<br>
# Aluno: Rafael de Menezes Ehlers<br>
# Data: Setembro de 2024

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataLoader:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_data(self):
        return self.data
    
class PreProcessing:
    def __init__(self, data):
        self.data = data

    def clean_data(self):
        # Tratar valores nulos, converter tipos, etc.
        self.data['Release date'] = pd.to_datetime(self.data['Release date'], errors='coerce')
        self.data = self.data.dropna(subset=['Metacritic score'])
        return self.data
    
class Analysis:
    def __init__(self, data):
        self.data = data

    # Pergunta 1: Jogos mais bem avaliados
    def top_metacritic_games_grouped_by_name(self, top_n=10):
        # Agrupa os jogos por nome e mantém o maior Metacritic score por nome de jogo
        grouped_games = self.data.loc[self.data.groupby('Name')['Metacritic score'].idxmax()]
        
        # Ordena os jogos por Metacritic score (decrescente) e, em caso de empate, pela data de lançamento (crescente)
        sorted_games = grouped_games.sort_values(
            by=['Metacritic score', 'Release date'],
            ascending=[False, True]
        )
        
        # Retorna os top N jogos
        return sorted_games[['Name', 'Release date', 'Metacritic score']].head(top_n)

    # Pergunta 2: Estatísticas para jogos de Role-playing
    def role_playing_stats(self):
        # Filtra os jogos do gênero "Role-playing" usando .loc
        role_playing_games = self.data.loc[self.data['Genres'].str.contains('RPG', na=False)].copy()

        # Verifica se existem jogos de role-playing
        if role_playing_games.empty:
            return {
                'DLC mean': 0,
                'DLC max': 0,
                'Positive mean': 0,
                'Positive max': 0,
                'Negative mean': 0,
                'Negative max': 0,
                'Demo materials mean': 0,
                'Demo materials max': 0
            }

        # Converte as colunas relevantes para numéricas ou conta os elementos, tratando valores ausentes
        role_playing_games['DLC count'] = pd.to_numeric(role_playing_games['DLC count'], errors='coerce').fillna(0)
        role_playing_games['Positive'] = pd.to_numeric(role_playing_games['Positive'], errors='coerce').fillna(0)
        role_playing_games['Negative'] = pd.to_numeric(role_playing_games['Negative'], errors='coerce').fillna(0)

        # Conta o número de screenshots e filmes usando str.split() e len(), e preenche NaN com 0
        role_playing_games['Screenshots'] = role_playing_games['Screenshots'].fillna('').apply(lambda x: len(x.split(',')) if x else 0)
        role_playing_games['Movies'] = role_playing_games['Movies'].fillna('').apply(lambda x: len(x.split(',')) if x else 0)

        # Calcula o número total de materiais de demonstração (Screenshots + Movies)
        role_playing_games = role_playing_games.assign(
            Demo_materials=role_playing_games['Screenshots'] + role_playing_games['Movies']
        )

        # Calcula estatísticas: média e máximo de DLCs, avaliações positivas, avaliações negativas e materiais de demonstração
        stats = {
            'DLCs médio': round(role_playing_games['DLC count'].mean(), 2),
            'DLCs máximo': round(role_playing_games['DLC count'].max(), 2),
            'Avaliações Positivas média': round(role_playing_games['Positive'].mean(), 2),
            'Avaliações Positivas  máximo': round(role_playing_games['Positive'].max(), 2),
            'Avaliações Negativas média': round(role_playing_games['Negative'].mean(), 2),
            'Avaliações Negativas máximo': round(role_playing_games['Negative'].max(), 2),
            'Materias de demonstração média': round(role_playing_games['Demo_materials'].mean(), 2),
            'Materias de demonstração máximo': round(role_playing_games['Demo_materials'].max(), 2)
        }

        return stats

    # Pergunta 3: Empresas que mais publicam jogos pagos
    # Função para encontrar os cinco publishers que mais publicam jogos pagos e calcular as estatísticas de avaliações positivas
    def top_publishers(self):
        # Filtra apenas jogos pagos
        paid_games = self.data[self.data['Price'] > 0]

        # Contabiliza o número de jogos pagos por publisher
        publisher_counts = paid_games['Publishers'].value_counts().head(5)

        # Lista para armazenar as estatísticas de cada publisher
        publisher_stats = []

        # Itera sobre os publishers mais frequentes
        for publisher in publisher_counts.index:
            # Filtra os jogos pagos do publisher
            publisher_games = paid_games[paid_games['Publishers'] == publisher]

            # Calcula a média e a mediana de avaliações positivas
            positive_mean = publisher_games['Positive'].mean()
            positive_median = publisher_games['Positive'].median()

            # Adiciona os resultados à lista
            publisher_stats.append({
                'Produtora': publisher,
                'Jogos Pagos': publisher_counts[publisher],
                'Média Rev. Pos.': round(positive_mean, 2),
                'Mediana Rev. Pos.': round(positive_median, 2)
            })

        # Cria um DataFrame a partir dos resultados
        df = pd.DataFrame(publisher_stats)

        return df

    # Pergunta 4: Crescimento de suporte para Linux
    def linux_support_growth(self):
        # Filtra os jogos que suportam Linux
        linux_support = self.data[self.data['Linux'] == True].copy()

        # Extrai o ano da data de lançamento usando .loc para evitar SettingWithCopyWarning
        linux_support.loc[:, 'Ano lançamento'] = linux_support['Release date'].dt.year

        # Filtra os jogos lançados entre 2018 e 2022
        linux_support_filtered = linux_support[(linux_support['Ano lançamento'] >= 2018) & (linux_support['Ano lançamento'] <= 2022)]

        # Conta o número de jogos por ano
        linux_games_by_year = linux_support_filtered.groupby('Ano lançamento').size()

        # Calcula o crescimento no número de jogos
        growth = linux_games_by_year.diff().fillna(0)

        # Verifica se houve crescimento geral entre 2018 e 2022
        if linux_games_by_year.iloc[-1] > linux_games_by_year.iloc[0]:
            growth_status = "Sim"
        else:
            growth_status = "Não"

        # Retorna o número de jogos por ano, o crescimento, e se houve crescimento geral
        return linux_games_by_year, growth, growth_status
    
    # Pergunta do aluno: Qual o jogo com maior nota, por categoria
    def jogo_maior_nota_por_categoria(self):
        # Filtrar jogos com Metacritic score maior que zero
        filtered_data = self.data[self.data['Metacritic score'] > 0].copy()

        # Dividir as categorias e expandir as categorias que estão separadas por vírgula
        filtered_data.loc[:, 'Categories'] = filtered_data['Categories'].str.split(',')

        # Explodir a coluna de categorias para criar uma linha para cada categoria
        exploded_data = filtered_data.explode('Categories')

        # Remover espaços em branco ao redor das categorias
        exploded_data.loc[:, 'Categories'] = exploded_data['Categories'].str.strip()

        # Para cada categoria, encontrar a maior nota
        max_scores = exploded_data.groupby('Categories')['Metacritic score'].max().reset_index()

        # Fazer o merge com os dados originais para pegar os jogos que possuem essa maior nota
        best_games = pd.merge(exploded_data, max_scores, on=['Categories', 'Metacritic score'])

        # Remover duplicatas exatas (caso um jogo tenha sido listado mais de uma vez exatamente)
        best_games_unique = best_games.drop_duplicates(subset=['Categories', 'Name'])

        # Ordenar as categorias por ordem alfabética
        result_sorted = best_games_unique[['Categories', 'Name', 'Metacritic score']].sort_values(by='Categories', ascending=True)

        # Retornar o DataFrame para possíveis usos
        return result_sorted

class Graphs:
    def __init__(self, data):
        self.data = data
    
    def apply_custom_style(self):
        # Definir estilo global
        plt.style.use('ggplot')  # Usar o estilo ggplot como base

        # Customizar detalhes específicos
        plt.rcParams['figure.figsize'] = (10, 6)  # Tamanho padrão dos gráficos
        plt.rcParams['axes.facecolor'] = '#f0f0f0'  # Cor de fundo dos eixos
        plt.rcParams['axes.edgecolor'] = '#333333'  # Cor da borda dos eixos
        plt.rcParams['axes.grid'] = True  # Mostrar grade
        plt.rcParams['grid.color'] = '#cccccc'  # Cor da grade
        plt.rcParams['grid.linestyle'] = '--'  # Estilo da grade
        plt.rcParams['axes.titleweight'] = 'bold'  # Título em negrito
        plt.rcParams['axes.labelweight'] = 'bold'  # Rótulos dos eixos em negrito
        plt.rcParams['font.size'] = 12  # Tamanho da fonte padrão
        plt.rcParams['legend.fontsize'] = 10  # Tamanho da fonte da legenda
        plt.rcParams['lines.linewidth'] = 2  # Largura das linhas
        plt.rcParams['lines.markersize'] = 8  # Tamanho dos marcadores
        plt.rcParams['font.family'] = 'Arial' # Fonte Arial

    # Gráfico 1: Percentual de jogos com suporte para cada sistema operacional
    def os_support_pie_chart(self):
        self.apply_custom_style()  # Aplica o estilo customizado

        # Conta os jogos que suportam cada sistema operacional
        total_games = len(self.data)
        windows_support = self.data['Windows'].sum()
        mac_support = self.data['Mac'].sum()
        linux_support = self.data['Linux'].sum()

        # Calcula a porcentagem de suporte para cada sistema
        os_support = {
            'Windows': (windows_support / total_games) * 100,
            'Mac': (mac_support / total_games) * 100,
            'Linux': (linux_support / total_games) * 100
        }

        # Gera o gráfico de pizza
        labels = list(os_support.keys())
        sizes = list(os_support.values())
        colors = ['#66c2a5', '#fc8d62', '#8da0cb']  # Definir cores personalizadas
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, counterclock=False, colors=colors)
        plt.title('Percentual de Jogos com Suporte para Sistemas Operacionais')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

    # Gráfico 2: Jogos single-player Indie e Estratégia por ano
    def indie_strategy_trend(self):
        self.apply_custom_style()  # Aplica o estilo customizado

        # Filtra os jogos de gêneros Indie e Strategy que também são single-player
        indie_games = self.data[
            (self.data['Genres'].str.contains('Indie', na=False)) & 
            (self.data['Categories'].str.contains('Single-player', na=False))
        ]
        strategy_games = self.data[
            (self.data['Genres'].str.contains('Strategy', na=False)) & 
            (self.data['Categories'].str.contains('Single-player', na=False))
        ]
        
        # Agrupa por ano de lançamento, considerando o intervalo entre 2010 e 2020
        indie_by_year = indie_games[(indie_games['Release date'].dt.year >= 2010) & (indie_games['Release date'].dt.year <= 2020)].groupby(indie_games['Release date'].dt.year).size()
        strategy_by_year = strategy_games[(strategy_games['Release date'].dt.year >= 2010) & (strategy_games['Release date'].dt.year <= 2020)].groupby(strategy_games['Release date'].dt.year).size()

        # Gera o gráfico de linhas mostrando a tendência de jogos Indie e Strategy
        plt.plot(indie_by_year.index, indie_by_year.values, label='Indie', marker='o', color='blue')
        plt.plot(strategy_by_year.index, strategy_by_year.values, label='Strategy', marker='x', color='green')
        plt.title('Número de Jogos Indie e Estratégia Single-Player Lançados por Ano (2010-2020)')
        plt.xlabel('Ano')
        plt.ylabel('Número de Jogos')
        plt.legend()
        plt.grid(True)
        plt.show()

    # Gráfico do aluno: Percentual de jogos lançados por ano.
    def jogos_lancados_por_ano_pizza(self):
        # Aplica o estilo customizado
        self.apply_custom_style()

        # Certifique-se de usar cópias do DataFrame se necessário
        self.data = self.data.copy()

        # Converte 'Release date' para datas, ignorando erros
        self.data['Release date'] = pd.to_datetime(self.data['Release date'], errors='coerce')

        # Extraindo o ano de lançamento e removendo valores nulos
        self.data['Release Year'] = self.data['Release date'].dt.year
        self.data = self.data.dropna(subset=['Release Year'])

        # Convertendo para inteiro para evitar possíveis erros de tipo
        self.data['Release Year'] = self.data['Release Year'].astype(int)

        # Cria uma nova coluna agrupando anos antes de 2015
        self.data['Release Year Grouped'] = self.data['Release Year'].apply(lambda x: '2015 e anteriores' if x <= 2015 else str(x))

        # Contando a quantidade de jogos por grupo de ano
        jogos_por_ano = self.data['Release Year Grouped'].value_counts().sort_index()

        # Gerar gráfico de pizza
        plt.pie(jogos_por_ano, labels=jogos_por_ano.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)

        # Configurações do gráfico
        plt.title('Percentual de Jogos Lançados por Ano')
        plt.axis('equal')  # Assegura que o gráfico de pizza seja um círculo perfeito

        # Exibe o gráfico
        plt.show()

loader = DataLoader('steam_games.csv')
data = loader.get_data()

pre_processor = PreProcessing(data)
clean_data = pre_processor.clean_data()

analysis = Analysis(clean_data)

top_games = analysis.top_metacritic_games_grouped_by_name(10)
print(top_games)

rpg_stats = analysis.role_playing_stats()
rpg_stats = "\n".join([f"{label}: {valor}" for label, valor in rpg_stats.items()])
print(rpg_stats)

top_publishers = analysis.top_publishers()
print(top_publishers)

linux_games_by_year, growth, growth_status = analysis.linux_support_growth()

linux_games_by_year.index.rename(None, inplace=True)
growth.index.rename(None, inplace=True)

print("Número de jogos que suportam Linux por ano:")
print(linux_games_by_year.to_string(index=True))

print("\nCrescimento no número de jogos por ano:")
print(growth.to_string(index=True))

print(f"\nO número de jogos que suportam Linux cresceu entre 2018 e 2022? {growth_status}")

tabela_maior_nota = analysis.jogo_maior_nota_por_categoria()
print(tabela_maior_nota.to_string(index=False))

graphs = Graphs(clean_data)

graphs.os_support_pie_chart()
graphs.indie_strategy_trend()
graphs.jogos_lancados_por_ano_pizza()