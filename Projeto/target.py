from typing import (
    Dict,
    List,
    Tuple,
)

import warnings
warnings.filterwarnings('ignore')


class Target:

    def __init__(self, limit: int):
        # Cria uma 'instância' da classe NumQueue, "Fila Numpy", com o limite definido pelo parâmetro 'limit'
        self.target = NumQueue(limit, tuple)

    # Método para adicionar um 'payload' à fila
    def persist_delivery(self, payload: Tuple):
        try:
            self.target.put(payload)  # Tenta adicionar à fila o 'payload'
            return True  # Retorna Verdadeiro se isso acontecer
        except:
            return False  # Se acontecer algum erro retorna Falso


class NumQueue:

    def __init__(self, limit: int, tipo):
        import numpy as np
        # Cria um array vazio com o limite fornecido e o tipo especificado
        self.__elementos = np.empty(limit, tipo)
        # Pontos de partida dos ponteiros da fila
        self.__point1 = self.__point0 = -1  # (ponteiro inicial -> 'self.__point1', ponteiro final -> 'self.__point0')
        # Guarda no respetivo atributo o limite da fila a ser criada
        self.__dime = limit

    def put(self, add):
        # Como ponto principal verifica se a fila não está cheia
        if self.length() != self.__dime:
            # Caso se tratasse de uma fila circular e se ainda existisse espaço para adicionar um 'tuplo' no inicio,
            # o ponteiro inicial voltaria ao inicio
            self.__point1 = (self.__point1 + 1) % self.__dime
            # É adicinado o tuplo recebido no respetivo indice incrementado do 'self.__point1'
            self.__elementos[self.__point1] = add
        # Da erro caso se deseje adicionar e já nao exista espaço na fila
        else:
            raise ValueError('put: Full Queue')

    def begin(self):
        # Verifica, inicialmente, se a fila contem algum elemento
        if not self.is_empty:
            # Para mostrar o respetivo elemento é incrementado o indice do ponteiro 'self.__point0'
            return self.__elementos[(self.__point0 + 1) % self.__dime]
        raise ValueError("begin: Empty Queue")

    def take(self):
        # Apenas "retira" (manipula o ponteiro, incrementando) se a fila não estiver vazia
        if self.is_empty:
            raise ValueError("take: Empty Queue")
        elif self.length() == 1:
            # Caso se deseja retirar o "unico" elemento da fila, incrementa-se os 2 ponteiros de modo que
            # voltem a posição inicial
            self.__point0 = self.__point1 = - 1
        # Caso as condiçoes acima nao se verifiquem é imcrementado (+ 1) o ponteiro final
        else:
            self.__point0 = (self.__point0 + 1) % self.__dime

    @property
    def is_empty(self):
        # Se o tamanho da lista for 0 então está vazia
        return self.length == 0

    def length(self):
        # Como no projeto o ponteiro inicial (self.__point1) é sempre maior que o ponteiro final (self.__point) a
        # seguinte condiçao irá ser sempre válida
        if self.__point1 > self.__point0 or (self.__point0 == -1 and self.__point1 == -1):
            return self.__point1 - self.__point0
        # Só daria o seguinte return caso estivessemos perante uma fila circular
        return self.__dime - self.__point0 + self.__point1
