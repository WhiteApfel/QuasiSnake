from keras import Sequential
from keras.layers import Dense
from copy import deepcopy
import numpy as np
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

class Gamer:
    def __init__(self, size):
        self.size = size
        self.model = self.create_model()
        self.counter = 0
        self.step_decode = {1: [-1, -1], 2: [-1, 1], 3: [1, 1], 4: [1, -1]}

    def create_model(self):
        model = Sequential()
        model.add(Dense(22, input_dim=(self.size + 2) ** 2 // 2, activation='relu'))
        model.add(Dense(14, activation='relu'))
        model.add(Dense(9, activation='relu'))
        model.add(Dense(4, activation='sigmoid'))
        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])  # надо менять
        return model

    def predict_step(self, local_map):
        pred = self.model.predict(np.array([local_map])).tolist()
        return pred.index(max(pred)) + 1

    def get_step(self, local_map) -> list:
        step = self.predict_step(local_map)
        return self.step_decode[step]

    def counter_steps(self, map_array, my_index, new=True):
        if new:
            self.counter = 0
        x = my_index[0]
        y = my_index[1]
        for i in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
            if map_array[x + i[0]][y + i[1]] == 1:
                map_array[x + i[0]][y + i[1]] = -1
                self.counter += 1
                self.counter_steps(map_array, [x + i[0], y + i[1]], new=False)
        if new:
            counter_copy = deepcopy(self.counter)
            self.counter = 0
            return counter_copy

    def get_available(self, map_array):
        to_return = []
        loc = map_array.index(-2)
        for i in [-4, -3, 5, 4]:
            to_return.append(int(map_array[loc + i] not in [-1, -3]))
        return to_return

    def bdsm(self, map_array):
        # TODO: Надо доделать наказание
        self.model.fit(np.array([map_array]), np.array([self.get_available(map_array)]))


import random
from collections import deque
from copy import deepcopy
import matplotlib.pyplot as plt


class MapController:

    def __init__(self, size):
        plt.ion()  # важная штука для динамических графиков
        self.map_history = deque([], maxlen=32)  # переполняемый лист
        self.size = size
        self.gen_map()
        self.step_counter = 0
        self.available_a = 0
        self.available_b = 0
        self.est_li_zhizn_na_zemle = None
        self.est_li_zhizn_na_zemle = True
        # Инициализируем игроков
        self.players = {10: Gamer(self.size), 11: Gamer(self.size)}

    def start_loop(self):
        """Запускает непорочный круг шагов. Надеюсь, это когда-нибудь кончится."""
        i = 0
        while True:
            while self.est_li_zhizn_na_zemle:
                self.make_step(10 + i % 2)
                i += 1
            self.gen_map()
            self.est_li_zhizn_na_zemle = True
        pass

    def viewer(self, local_map):
        """Показывает наглядно, что происходит. Спасибо тепловым картам"""
        plt.imshow(local_map, cmap='hot', interpolation='nearest')
        plt.show()
        plt.pause(0.0001)
        plt.clf()

    def map_compress(self, element):
        """
        Убирает ненужные диагонали, оставляя
        чистый и понятный нейронке лист значений
        """
        compressed = list()
        for y in range(0, self.size + 2):
            for x in range(y % 2, self.size + 2, 2):
                compressed.append(self.map_history[-1][x][y])
        compressed[compressed.index(10)] = -2 if element == 10 else -3
        compressed[compressed.index(11)] = -2 if element == 11 else -3
        return compressed

    def gen_map(self):
        """
        Генерирует полноценную карту в формате двумерного массива
        со стоящими на одной диагональной системе игроками
        """
        locations = []
        [[locations.append([i, j]) for i in range(j % 2, self.size, 2)] for j in
         range(self.size)]  # Выбирает клетки одной диагональной системы
        a, b = [0, 0], [0, 0]  # Вспомогательный шаг
        while a == b:
            a, b = random.choices(locations, k=2)  # Выбор двух случайных разных

        local_map = np.ones((self.size, self.size))  # Генерация двумерного массива из единиц
        local_map[a[0]][a[1]] = 10  # Меняем одного игрока на 10
        local_map[b[0]][b[1]] = 11  # Другого игрока на 11
        local_map = np.pad(local_map, pad_width=1, mode="constant", constant_values=-1)
        self.coordinates = {10: (a[0] + 1, a[1] + 1), 11: (b[0] + 1, b[1] + 1)}
        self.map_history.append(local_map)

    def make_step(self, number_player):
        """
        Шагает одним, шагает другим. Если оба игрока пошагали, то обновляет карту в истории.
        """
        new_map = deepcopy(self.map_history[-1])
        self.viewer(new_map)

        new_map[self.coordinates[number_player][0]][self.coordinates[number_player][1]] = -1
        print(self.coordinates)
        coordinates_moving = self.players[number_player].get_step(self.map_compress(number_player))
        print(coordinates_moving)
        self.coordinates[number_player] = (
            self.coordinates[number_player][0] + coordinates_moving[0],
            self.coordinates[number_player][1] + coordinates_moving[1])

        if self.map_history[-1][self.coordinates[number_player][0]][self.coordinates[number_player][1]] in  [-1,10,11] :
            self.players[number_player].bdsm(self.map_compress(number_player))
            self.est_li_zhizn_na_zemle = False
            return False

        new_map[self.coordinates[number_player][0], self.coordinates[number_player][1]] = number_player
        self.viewer(new_map)
        self.map_history.append(new_map)

    def get_available_step(self, who):
        # TODO Надо доделать зачем-то
        a = self.map_history[-1][0]
        return a * 2 if who == -10 else a * 3

    def update_map_info(self):
        # TODO Соответственно, тоже
        self.available_a = self.get_available_step(-10)
        self.available_b = self.get_available_step(-11)


MC = MapController(8)

MC.start_loop()
