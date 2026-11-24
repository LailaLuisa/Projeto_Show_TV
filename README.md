
# Projeto Show TV — Pipeline de Dados trabalhando com Arquitetura Medallion
## Sobre o projeto

Este projeto tem como objetivo desenvolver um pipeline de dados utilizando Python e a arquitetura Medallion (Bronze, Silver e Gold).

Os dados são extraídos da API pública TVmaze, que disponibiliza informações sobre séries de televisão.

Ao longo do processo, os dados passam por etapas de extração, limpeza, transformação, organização e validação, sendo armazenados em arquivos JSON e Parquet.

O projeto foi desenvolvido com foco no aprendizado de conceitos de Engenharia de Dados, organização de pipelines e modelagem de dados.


## Arquitetura Medallion

O projeto utiliza a arquitetura Medallion, dividida em três camadas:

### Bronze — Dados brutos

Responsável pela extração dos dados da API TVmaze e pelo armazenamento das informações originais em formato JSON.

### Silver — Dados tratados

Responsável pela limpeza e transformação dos dados, incluindo remoção de tags HTML das sinopses, tratamento das avaliações e conversão de datas. Os dados tratados são armazenados em formato Parquet.

### Gold — Dados organizados

Responsável pela organização e modelagem dos dados para análise, utilizando três tabelas:

- **shows:** informações das séries.
- **genres:** catálogo de gêneros únicos.
- **show_genres:** tabela associativa que relaciona séries e gêneros.

## Fluxo de dados

O pipeline segue esta sequência:

**1. API TVmaze**
- Fonte dos dados sobre as séries.


**2. Bronze — Dados brutos**
- Extração e armazenamento em JSON.


**3. Silver — Dados tratados**
- Limpeza e transformação dos dados.
- Armazenamento em Parquet.


**4. Gold — Dados organizados**
- `shows.parquet`: informações das séries.
- `genres.parquet`: catálogo de gêneros.
- `show_genres.parquet`: relacionamento entre séries e gêneros.

## Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento do pipeline.
- **Requests:** realização das requisições à API TVmaze.
- **Pandas:** manipulação, limpeza e transformação dos dados.
- **BeautifulSoup4:** remoção de tags HTML das sinopses.
- **PyArrow:** suporte à leitura e gravação de arquivos Parquet.
- **JSON:** armazenamento dos dados brutos na camada Bronze.
- **Logging:** registro de informações e erros durante a execução.
- **Pathlib:** manipulação dos caminhos e diretórios do projeto.

## Fonte dos dados e escopo da extração
- Fonte: API pública TVmaze.
- Intervalo consultado: IDs de 1 a 79.
- Registros obtidos: 77 séries.
- IDs 17 e 36: não encontrados na API (HTTP 404).

## Resultados do projeto ✅  

Após a execução do pipeline, foram obtidos os seguintes resultados:

- **77 séries:** dados extraídos e processados com sucesso.
- **20 gêneros:** gêneros únicos identificados na base.
- **214 relacionamentos:** associações entre séries e gêneros.

### Validação dos dados

Foram realizadas verificações para garantir a qualidade e a consistência dos dados:

- Integridade referencial entre as tabelas.
- Ausência de relacionamentos duplicados entre séries e gêneros.
- Comparação dos identificadores entre as camadas Silver e Gold.
- Verificação de valores ausentes.

Os valores ausentes em campos como data de encerramento e duração foram preservados, evitando o preenchimento de informações sem fundamento.
