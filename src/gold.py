import pandas as pd
import logging
from pathlib import Path

class GoldLayer:

    def __init__(self, caminho):
        self.caminho = caminho

    def load_data(self):
        try:
            df = pd.read_parquet(self.caminho)

            logging.info('Dados Silver carregados com sucesso.')
            return df

        except (OSError, ValueError) as e:
            logging.error(f'Erro ao carregar os dados: {e}')
            return None


    def create_genres(self, df):
        all_genres = []

        for genres in df['genres']:
            all_genres.extend(genres)

        unique_genres = sorted(set(all_genres))

        genres_df = pd.DataFrame({
            'genre_id': range(1, len(unique_genres) + 1),
            'genre_name': unique_genres
        })

        logging.info('Tabela de gêneros criada com sucesso.')

        return genres_df


    def create_show_genres(self, shows_df, genres_df):
        genre_ids = {}

        for _, genre in genres_df.iterrows():
            genre_ids[genre['genre_name']] = genre['genre_id']

        relationships = []

        for _, show in shows_df.iterrows():
            for genre in show['genres']:
                relationships.append({
                    'show_id': show['id'],
                    'genre_id': genre_ids[genre]
                })

        show_genres_df = pd.DataFrame(relationships)

        return show_genres_df


    def create_shows(self, df):
        shows_df = df.drop(columns=['genres'])

        return shows_df

    
    def save_data(self, df, nome_arquivo):
        try:
            caminho = Path(nome_arquivo)
            caminho.parent.mkdir(parents=True, exist_ok=True)

            df.to_parquet(caminho, index=False)

            logging.info(f'Dados salvos com sucesso em: {caminho}')

            return True

        except (OSError, ValueError) as e:
            logging.error(f'Erro ao salvar os dados: {e}')

            return False
