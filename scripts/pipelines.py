
import logging

from src.bronze import BronzeLayer
from src.silver import SilverLayer
from src.gold import GoldLayer


# Configuração dos logs

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)


# Caminhos e configurações

BASE_URL = 'https://api.tvmaze.com/shows/'

BRONZE_PATH = 'layers/bronze/raw_data.json'
SILVER_PATH = 'layers/silver/shows.parquet'

GOLD_SHOWS_PATH = 'layers/gold/shows.parquet'
GOLD_GENRES_PATH = 'layers/gold/genres.parquet'
GOLD_SHOW_GENRES_PATH = 'layers/gold/show_genres.parquet'


# Camada Bronze

logging.info('Iniciando camada Bronze.')

raw_data = []

for show_id in range(1, 80):
    url = f'{BASE_URL}{show_id}'

    bronze = BronzeLayer(url)
    result = bronze.extract_data()

    if result is not None:
        raw_data.append(result)

bronze = BronzeLayer(BASE_URL)

saved = bronze.save_raw_data(raw_data, BRONZE_PATH)

if not saved:
    raise RuntimeError('Falha ao salvar os dados na camada Bronze.')

logging.info(f'Total de registros extraídos: {len(raw_data)}')


# Camada Silver

logging.info('Iniciando camada Silver.')

silver = SilverLayer(BRONZE_PATH)

df = silver.load_data()

if df is None:
    raise RuntimeError('Não foi possível carregar os dados da Bronze.')


# Seleção das colunas

columns = [
    'id',
    'name',
    'type',
    'language',
    'genres',
    'status',
    'premiered',
    'ended',
    'runtime',
    'averageRuntime',
    'rating',
    'summary'
]

df = df[columns].copy()


# Limpeza e transformações

df = silver.clean_data(df)
df = silver.transform_rating(df)
df = silver.transform_dates(df)


# Salvando camada Silver

saved = silver.save_data(df, SILVER_PATH)

if not saved:
    raise RuntimeError('Falha ao salvar os dados na camada Silver.')


# Camada Gold

logging.info('Iniciando camada Gold.')

gold = GoldLayer(SILVER_PATH)

df = gold.load_data()

if df is None:
    raise RuntimeError('Não foi possível carregar os dados da Silver.')


# Tabela de gêneros

genres_df = gold.create_genres(df)

saved = gold.save_data(
    genres_df,
    GOLD_GENRES_PATH
)

if not saved:
    raise RuntimeError('Falha ao salvar a tabela de gêneros na Gold.')


# Tabela de relacionamento entre séries e gêneros

show_genres_df = gold.create_show_genres(df, genres_df)

saved = gold.save_data(
    show_genres_df,
    GOLD_SHOW_GENRES_PATH
)

if not saved:
    raise RuntimeError('Falha ao salvar a tabela de relacionamentos na Gold.')


# Tabela de séries

shows_gold_df = gold.create_shows(df)

saved = gold.save_data(
    shows_gold_df,
    GOLD_SHOWS_PATH
)

if not saved:
    raise RuntimeError('Falha ao salvar a tabela de séries na Gold.')

# Conclusão do pipeline

logging.info('Pipeline executado com sucesso!')

logging.info(f'Total de séries: {len(shows_gold_df)}')
logging.info(f'Total de gêneros: {len(genres_df)}')
logging.info(f'Total de relacionamentos: {len(show_genres_df)}')
