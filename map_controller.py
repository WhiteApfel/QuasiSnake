import random
from collections import deque
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from main import Gamer


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
		self.coordinates = {10: (0,0), 11:(0,0)}
		self.players = {10: Gamer(self.size), 11:Gamer(self.size)}

	def start_loop(self):
		"""Запускает непорочный круг шагов. Надеюсь, это когда-нибудь кончится."""
		i = 0
		while self.est_li_zhizn_na_zemle:
			self.make_step(10 + i % 2)
			i += 1
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
		self.map_history.append(local_map)

	def make_step(self, number_player):
		"""
		Шагает одним, шагает другим. Если оба игрока пошагали, то обновляет карту в истории.
		"""
		new_map = deepcopy(self.map_history[-1])


		new_map[self.coordinates[number_player][0]][self.coordinates[number_player][1]] = -1
		coordinates_moving = self.players[number_player].get_step(self.map_compress(number_player))

		self.coordinates[number_player] = (
			self.coordinates[number_player][0] + coordinates_moving[0],
			self.coordinates[number_player][1] + coordinates_moving[1])

		if  self.map_history[-1][self.coordinates[number_player][0]][self.coordinates[number_player][1]] == -1:
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
