import source
import target

from source import *
from target import Target

import pandas as pd
from typing import (Dict, List, Tuple)

import warnings
warnings.filterwarnings('ignore')


class Main:

    def __init__(self, batch_size: int):
        import math as mt
        self.batch_size: int = batch_size  # Define o tamanho do batch
        self.source = Source()  # Cria uma "instância" da classe Source para gerir a leitura dos dados
        # Calculo do número de batches necessários com base no tamanho do file e no tamanho do batch
        self.batch_limit = mt.ceil(self.source.file_size/self.batch_size)  # arredonda por excesso para caso se trata de
        # um numero decimal
        # O atributo antes criado delimita o tamanho da fila que irá ser criada na classe Target
        self.target = Target(self.batch_limit)
        # Atributo criado, por preferência, para que as listas sejam ordenadas de forma alterada (ascendente e depois
        # descendente, sucessivamente)
        self.asc = True

    # Chama a funçao da classe Source que atualiza a ultima linha lida
    def update_last_searched_id(self, new_id):
        self.source.update_last_read_id(new_id=new_id)

    # Chama a funçao da classe Source que vai incrementando os batches processados
    def update_batch_nr(self):
        self.source.update_batch_nr()

    # Entrega o tuplo com o "batch_nr", minimo e maximo retornado do funçao process à fila Numpy da classe Target
    def persist_delivery(self, payload: Tuple):
        return self.target.persist_delivery(payload=payload)

    # Função "main" que chama metodos de ordenação desenvolvidos e retorna o minimo e maximo consoante a ordenaçao feita
    @staticmethod
    def sort(batch: list, ascending: bool, which=True) -> Tuple[int, int]:
        # Which define o metodo de ordenaçao a utilizar
        if which:
            lista = Main.merge_sort(a=batch, ascending=ascending)
        else:
            lista = Main.selection_sort(a=batch, ascending=ascending)
        if ascending:
            return lista[0], lista[-1]  # Caso a lista tenha sido ascendentemente, retira o minimo do indice nr 1 e
        # maximo do ultimo indice, e retorna os mesmos num tuplo
        return lista[-1], lista[0]  # Caso a lista tenha sido descendentemente, retira o minimo do ultimo indice  e
        # o maximo do indice nr 1, e retorna os mesmos num tuplo

    @staticmethod
    def selection_sort(a: list, ascending: bool):
        # Este algoritmo funciona encontrando repetidamente o elemento mínimo (considerando a ordenação ascendente)
        # da parte não ordenada e movendo-o para o início. O método percorre toda a lista, posicionando corretamente
        # cada elemento por vez
        n = len(a)
        for e in range(0, n):
            valor = e
            for j in range(e + 1, n):
                if not ascending and a[j] > a[valor]:
                    valor = j
                elif ascending and a[j] < a[valor]:
                    valor = j
            if e != valor:
                a.insert(e, a[valor])
                del a[valor + 1]
        return a

    @staticmethod
    def bubble_sort(a, ascending):
        # Este método percorre a lista, comparando o elemento no índice atual 'e' com todos os elementos após O mesmo
        # Se os elementos não estiverem na ordem correta (definida pelo parametro "ascending"), eles serão trocados.
        # Este processo é repetido até que a lista esteja ordenada.
        n = len(a)
        for e in range(0, n):
            for j in range(e + 1, n):
                if (a[e] > a[j]) and ascending:
                    a[e], a[j] = a[j], a[e]  # Troca se a ordem ascendente não for cumprida
                elif (a[e] < a[j]) and not ascending:
                    a[e], a[j] = a[j], a[e]  # Troca se a ordem descendente não for cumprida
        return a

    @staticmethod
    def merge_sort(a, ascending=True):
        # Este método implementa o algoritmo merge_sort recursivamente.
        # Se o array 'a' tem 1 ou nenhum elemento, está ordenado por definição, então retorna 'a'.
        if len(a) <= 1:
            return a
        # Divide o array em duas metades, 'left' e 'right'
        mid = len(a) // 2
        left = a[:mid]
        right = a[mid:]
        # Aplica o merge sort recursivamente nas metades 'left' e 'right'
        left = Main.merge_sort(left, ascending)
        right = Main.merge_sort(right, ascending)
        # Combina as metades ordenadas
        return Main.merge(left, right, ascending)

    @staticmethod
    def merge(left, right, ascending):
        # Esta função auxiliar combina dois arrays ordenados (left e right) em um único array ordenado
        result = []   # Inicializa o array que conterá o resultado final da combinação
        e = j = 0  # Inicializa os índices para iteragir sobre o "left" e "right"
        # Enquanto houver elementos em ambos os arrays "left" e "right"
        while e < len(left) and j < len(right):
            # Se estiver ordenando de forma ascendente e o elemento atual de "left"
            # for menor que o do "right", ou se estiver ordenando de forma descendente
            # e o elemento de "left" for maior, adiciona o elemento de 'left' ao 'result'.
            if (ascending and left[e] < right[j]) or (not ascending and left[e] > right[j]):
                result.append(left[e])
                e += 1  # Incrementa o índice de 'left'
            else:
                # Caso contrário, adiciona o elemento de 'right' ao 'result'
                result.append(right[j])
                j += 1
        # Uma vez que um dos arrays tenha sido completamente iterado, adiciona o restante do outro array ao 'result'
        result += left[e:]
        result += right[j:]
        return result  # Retorna o array resultante da combinação

    def process(self, batch: List) -> Tuple:
        # Recebe um batch de dados do método "run", ordenando-os e alternando a direção da ordenação a cada batch
        payload: Tuple = Main.sort(batch=batch, ascending=self.asc)
        self.asc = not self.asc
        # Retorna o respetivo batch processado, o minimo e maximo do respetivo batch
        return self.source.batch_nr, payload[0], payload[1]

    def run(self) -> None:
        # Este método é o "motor" principal do script, controlando o fluxo de processamento dos dados
        # Ele executa em um loop contínuo até que todos os dados tenham sido processados
        while True:
            # Carrega o próximo batch de dados usando a classe Source, o referente tamanho do batch é definido
            # na inicialização da classe Main
            batch: Tuple = self.source.load_state(batch_size=self.batch_size)
            if batch is None:
                return  # Se não houver mais dados (mais linhas) para processar, o loop é encerrado e o método termina
            # Processa o batch atual. Inclui ordenar os dados do batch e guarda o batch nr processado, o minimo e maximo
            delivery: Tuple = self.process(batch=batch[1])
            # "Tenta" entregar os dados processados para a classe Target. Se a entrega falhar, uma exceção é "levantada"
            result: bool = self.persist_delivery(payload=delivery)
            if result:
                # Atualiza o número do batch e o ID da última linha lida se a entrega for bem-sucedida
                self.update_batch_nr()
                self.update_last_searched_id(new_id=batch[0])
                del batch  # Opcional - remove a referência ao batch atual para "libertar" de memória
            else:
                raise ValueError(f'Batch unsuccessfully delivered for id: {self.source.last_read_id}')


if __name__ == '__main__':
    batch_tamanhos = [100, 1000, 10000, 25000, 50000, 100000]  # Lista com diferentes tamanhos de batches
    tempos_execucao = {}  # Criação de um dicionário onde irá ser guardado os diferentes tempos de execução
    import time  # Bibliotca para cronometrar o tempo de execução
    import matplotlib.pyplot as plt  # Biblioteca para gerar graficamente os tempos em função do tamanho do batch
    for batch_size in batch_tamanhos:  # Itera sobre cada tamanho do batch especificado
        # Cria uma instância da classe Main para o tamanho de batch atual
        process = Main(batch_size=batch_size)
        start_time = time.perf_counter()  # Registra o tempo de início do processamento
        process.run()  # Inicia o processamento dos dados
        lista_final = []  # É criada uma lista final que irá receber o minimo e maximo de cada batch processado
        for i in range(0, process.target.target.length()):
            # Retira o minimo e maximo de cada tuplo da fila numpy criada na classe Target, correspondente ao indice nr
            # 1 e 2, respetivamente, e adiciona a "lista_final"
            lista_final.append(process.target.target.begin()[1])
            lista_final.append(process.target.target.begin()[2])
            process.target.target.take()
        # Ordena a lista final para obter os valores extremos globais
        lista_ordenada = process.sort(batch=lista_final, ascending=True)
        # "Imprime" o valor mínimo e máximo global
        print(f"Minimo: {lista_ordenada[0]}")
        print(f"Maximo: {lista_ordenada[1]}")
        # Marca o fim do tempo de processamento e calcula a duração de execução
        end_time = time.perf_counter()
        delta_time = (end_time - start_time)
        # Armazena o tempo de execução no dicionário com a chave sendo o tamanho do batch
        tempos_execucao[process.batch_size] = delta_time
        print(f"Tempo de execução para batch_size {process.batch_size}: {delta_time}  segundos")

    # Uso do Matplotlib para plotar os resultados
    plt.figure(figsize=(10, 6))
    plt.plot(tempos_execucao.keys(), tempos_execucao.values(), marker='o', linestyle='-', color='b')
    plt.title('Tempo de Execução do Algoritmo em Função do Tamanho do Batch')
    plt.xlabel('Tamanho do Batch')
    plt.ylabel('Tempo de Execução (s)')
    plt.grid(True)
    plt.show()
