
import pandas as pd

# Carregamento das tabelas Gold
shows = pd.read_parquet('layers/gold/shows.parquet')
genres = pd.read_parquet('layers/gold/genres.parquet')
show_genres = pd.read_parquet('layers/gold/show_genres.parquet')

# Carregamento da tabela Silver
silver_df = pd.read_parquet('layers/silver/shows.parquet')


# 1. Verificação da quantidade de registros
print('\n--- Quantidade de Registros ---')

print('Total de séries:', len(shows))
print('Total de gêneros:', len(genres))
print('Total de relacionamentos:', len(show_genres))


# 2. Verificação da integridade referencial
print('\n--- Integridade Referencial ---')

shows_ids = set(shows['id'])
genres_ids = set(genres['genre_id'])

show_ids_relacionados = set(show_genres['show_id'])
genre_ids_relacionados = set(show_genres['genre_id'])

shows_sem_correspondencia = show_ids_relacionados - shows_ids
genres_sem_correspondencia = genre_ids_relacionados - genres_ids

if not shows_sem_correspondencia:
    print(f'Todos os IDs de séries possuem correspondência.')
else:
    print('IDs de séries sem correspondência:', shows_sem_correspondencia)

if not genres_sem_correspondencia:
    print('Todos os IDs de gêneros possuem correspondência.')
else:
    print('IDs de gêneros sem correspondência:', genres_sem_correspondencia)


# 3. Verificação de relacionamentos duplicados
print('\n--- Relacionamentos Duplicados ---')

duplicados = show_genres.duplicated(
    subset=['show_id', 'genre_id']
).sum()

if duplicados == 0:
    print('Nenhum relacionamento duplicado encontrado.')
else:
    print(f'Foram encontrados {duplicados} relacionamentos duplicados.')


# 4. Verificação de valores nulos
print('\n--- Valores Nulos ---')

print('\nTabela shows:')
print(shows.isnull().sum())

print('\nTabela genres:')
print(genres.isnull().sum())

print('\nTabela show_genres:')
print(show_genres.isnull().sum())


# 5. Comparação dos identificadores entre Silver e Gold
print('\n--- Comparação da Silver x Gold ---')

ids_diferentes = set(silver_df['id']) ^ set(shows['id'])

if len(ids_diferentes) == 0:
    print('Todos os IDs foram preservados entre Silver e Gold.')
else:
    print(
        f'Foram encontrados {len(ids_diferentes)} '
        'IDs diferentes entre Silver e Gold:',
        ids_diferentes
    )

print('\n--- Verificações Concluídas ---')