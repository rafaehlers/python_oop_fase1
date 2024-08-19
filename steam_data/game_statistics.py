from collections import defaultdict

class GameStatistics:
    def __init__(self, games):
        self.games = games

    def percentual_jogos_gratuitos_pagos(self):
        """
        Calcula o percentual de jogos gratuitos e pagos.

        Exemplos:
        >>> games = [{'Price': '0'}, {'Price': '9.99'}, {'Price': '0'}, {'Price': '19.99'}]
        >>> stats = GameStatistics(games)
        >>> stats.percentual_jogos_gratuitos_pagos()
        {'gratuitos': 50.0, 'pagos': 50.0}

        >>> games = [{'Price': '0'}, {'Price': '0'}, {'Price': '0'}, {'Price': '19.99'}]
        >>> stats = GameStatistics(games)
        >>> stats.percentual_jogos_gratuitos_pagos()
        {'gratuitos': 75.0, 'pagos': 25.0}
        """
        gratuitos = sum(1 for game in self.games if float(game['Price']) == 0)
        pagos = len(self.games) - gratuitos
        total = len(self.games)
        return {
            "gratuitos": (gratuitos / total) * 100,
            "pagos": (pagos / total) * 100
        }

    def ano_com_mais_jogos(self):
        """
        Retorna o ano com o maior número de novos jogos. 
        Se houver empate, retorna uma lista com os anos empatados.

        Exemplos:
        >>> games = [{'Release date': 'Jan 1, 2020'}, {'Release date': 'Feb 1, 2021'}, {'Release date': 'Mar 1, 2021'}, {'Release date': 'Apr 1, 2020'}]
        >>> stats = GameStatistics(games)
        >>> stats.ano_com_mais_jogos()
        ['2020', '2021']

        >>> games = [{'Release date': 'Jan 1, 2019'}, {'Release date': 'Feb 1, 2019'}, {'Release date': 'Mar 1, 2018'}, {'Release date': 'Apr 1, 2019'}]
        >>> stats = GameStatistics(games)
        >>> stats.ano_com_mais_jogos()
        ['2019']

        >>> games = [{'Release date': 'Jan 1, 2022'}]
        >>> stats = GameStatistics(games)
        >>> stats.ano_com_mais_jogos()
        ['2022']
        """
        anos = defaultdict(int)
        for game in self.games:
            ano = game['Release date'].split(', ')[-1]
            anos[ano] += 1
        
        max_jogos = max(anos.values())
        anos_max = [ano for ano, count in anos.items() if count == max_jogos]
        return anos_max

    def jogo_com_maior_nota_por_categoria(self):
        """
        Retorna o jogo com a maior nota em cada categoria.

        Exemplos:
        >>> games = [
        ...     {'Name': 'Game A', 'Categories': 'Action,Adventure', 'User score': '8.5'},
        ...     {'Name': 'Game B', 'Categories': 'Action,Indie', 'User score': '9.0'},
        ...     {'Name': 'Game C', 'Categories': 'Adventure,Indie', 'User score': '7.0'},
        ...     {'Name': 'Game D', 'Categories': 'Action', 'User score': '6.5'}
        ... ]
        >>> stats = GameStatistics(games)
        >>> stats.jogo_com_maior_nota_por_categoria() == {
        ...     'Action': {'jogo': 'Game B', 'nota': 9.0},
        ...     'Adventure': {'jogo': 'Game A', 'nota': 8.5},
        ...     'Indie': {'jogo': 'Game B', 'nota': 9.0}
        ... }
        True

        >>> games = [
        ...     {'Name': 'Game X', 'Categories': 'Puzzle', 'User score': '7.5'},
        ...     {'Name': 'Game Y', 'Categories': 'Puzzle', 'User score': '8.0'}
        ... ]
        >>> stats = GameStatistics(games)
        >>> stats.jogo_com_maior_nota_por_categoria() == {
        ...     'Puzzle': {'jogo': 'Game Y', 'nota': 8.0}
        ... }
        True

        >>> games = [
        ...     {'Name': 'Game Z', 'Categories': 'RPG', 'User score': ''},  # Empty user score should be treated as 0
        ...     {'Name': 'Game W', 'Categories': 'RPG', 'User score': '9.5'}
        ... ]
        >>> stats = GameStatistics(games)
        >>> stats.jogo_com_maior_nota_por_categoria() == {
        ...     'RPG': {'jogo': 'Game W', 'nota': 9.5}
        ... }
        True
        """
        categorias = defaultdict(lambda: {'jogo': '', 'nota': 0})
        
        for game in self.games:
            categorias_jogo = game['Categories'].split(',')
            user_score = float(game['User score']) if game['User score'] else 0
            
            for categoria in categorias_jogo:
                if user_score > categorias[categoria]['nota']:
                    categorias[categoria] = {'jogo': game['Name'], 'nota': user_score}
        
        return categorias