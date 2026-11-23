import json
import pandas as pd
import logging
from pathlib import Path
from bs4 import BeautifulSoup


class SilverLayer:

    def __init__(self, path):
        self.path = path

    def load_data(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            df = pd.DataFrame(data)

            logging.info('Dados carregados com sucesso.')
            return df

        except (OSError, json.JSONDecodeError) as e:
            logging.error(f'Erro ao carregar os dados: {e}')
            return None


    def clean_data(self, df):

        df['summary'] = df['summary'].apply(
            lambda x: BeautifulSoup(x, 'html.parser').get_text()
            if pd.notna(x) else x
        )

        logging.info('Sinopses limpas com sucesso.')

        return df


    def transform_rating(self, df):

        df['rating_average'] = df['rating'].apply(
            lambda x: x['average'] if isinstance(x, dict) else None
        )

        df = df.drop(columns=['rating'])

        logging.info('Avaliações transformadas com sucesso.')

        return df


    def transform_dates(self, df):
        df['premiered'] = pd.to_datetime(
            df['premiered'], errors='coerce'
        )

        df['ended'] = pd.to_datetime(
            df['ended'], errors='coerce'
        )

        logging.info('Datas transformadas com sucesso.')

        return df
    
    
    def save_data(self, df, caminho):
        try:
            caminho = Path(caminho)
            caminho.parent.mkdir(parents=True, exist_ok=True)

            df.to_parquet(caminho, index=False)

            logging.info(f'Dados salvos com sucesso em: {caminho}')

            return True

        except (OSError, ValueError) as e:
            logging.error(f'Erro ao salvar os dados: {e}')

            return False
