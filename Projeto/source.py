import pandas as pd

from typing import (
    Dict,
    List,
    Tuple,
)

import warnings
warnings.filterwarnings('ignore')


class Source:

    def __init__(self):
        # Carrega o ficheiro fornecido e guarda diretamente no atributo 'self.file'
        self.file = pd.read_csv("file_with_numbers.csv")
        # Numero inicial do batch; representa o numero de batches processados
        self.batch_nr: int = 0
        # Representa o indice da ultima linha do ficheiro
        self.last_read_id: int = 0
        # Atributo onde fica guardado o tamanho total da coluna 'number' do ficheiro CSV
        self.file_size: int = len(self.file["number"])

    # Incrementa o numero de batches de 1 em 1
    def update_batch_nr(self):
        self.batch_nr += 1

    # Atualiza a ultima linha 'lida' para o novo indice passado como parametro
    def update_last_read_id(self, new_id):
        self.last_read_id = new_id

    # Atualiza o estado da 'fonte' de dados, retornando o novo limite superior e um batch de dados
    def load_state(self, batch_size: int) -> Tuple[int, List] or None:
        # Apenas retorna o que foi referido se ainda existir 'linhas' por ler
        if self.last_read_id < self.file_size:
            # Atualiza o limite do batch que passará a ser 'new_id' do método 'uptade_last_read_id'
            upper_limit: int = self.last_read_id + batch_size
            # Busca um novo batch desde da ultima linha lida até ao novo limite superior
            batch: List = list(
                self.file['number'][self.last_read_id:upper_limit]
            )
            return upper_limit, batch
        # Retorna 'None' apenas se não houver mais linhas por ler
        return None
