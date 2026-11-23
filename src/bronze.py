import json
import requests
import logging
from pathlib import Path

class BronzeLayer:

    def __init__(self, url):
        self.url = url

    def extract_data(self):
        try:
            resp = requests.get(self.url, timeout=10)
            resp.raise_for_status()

            data = resp.json()
            logging.info(f'Dados extraídos com sucesso: {self.url}')
            return data

        except requests.exceptions.HTTPError as e:
            if resp.status_code == 404:
                logging.warning(f'Dados não encontrados em: {self.url}')
            else:
                logging.error(f'Erro HTTP: {e}')

        except requests.exceptions.JSONDecodeError as e:
            logging.error(f'Erro ao interpretar JSON: {e}')

        except requests.exceptions.RequestException as e:
            logging.error(f'Erro na requisição: {e}')

        return None
        
    
    def save_raw_data(self, data, caminho):
        try:
            caminho = Path(caminho)

            caminho.parent.mkdir(parents=True, exist_ok=True)

            with open(caminho, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            logging.info(f"Dados salvos com sucesso em: {caminho}")

            return True

        except (OSError, TypeError, ValueError) as e:
            logging.error(f"Erro ao salvar os dados: {e}")

            return False
