import random
from collections import deque
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np


class MapController:

	def __init__(self, size):
		plt.ion()  # важная штука для динамических графиков
		self.map_history = deque([], maxlen=32)  # переполняемый лист
		self.size = size
		self.gen_map()
		self.step_counter = 0
		self.available_a = 0
		self.available_b = 0
		self.coordinates_gay = (0, 0)
		self.coordinates_straight = (0, 0)
		self.est_li_zhizn_na_zemle = None

		# Инициализируем игроков
		self.GamerGay = Gamer(self.size)
		self.GamerStraight = Gamer(self.size)

	def start_loop(self):
		"""Запускает непорочный круг шагов. Надеюсь, это когда-нибудь кончится."""
		while self.est_li_zhizn_na_zemle:
			continue
		# TODO Надо запускать карту
		pass

	def viewer(self, local_map):
		"""Показывает наглядно, что происходит. Спасибо тепловым картам"""
		plt.imshow(local_map, cmap='hot', interpolation='nearest')
		plt.show()
		plt.pause(0.0001)
		plt.clf()

	def map_compress(self):
		"""
		Убирает ненужные диагонали, оставляя
		чистый и понятный нейронке лист значений
		"""
		compressed = list()
		for y in range(0, self.size + 2):
			for x in range(y % 2, self.size + 2, 2):
				compressed.append(self.map_history[-1][x][y])
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

		self.map_history.append(local_map)

	def make_step(self):
		"""
		Шагает одним, шагает другим. Если оба игрока пошагали, то обновляет карту в истории.
		"""
		# TODO Надо сделать окончание игры, если кто-то из игроков лохонулся.

		new_map = deepcopy(self.map_history[-1])

		self.viewer(new_map)

		# step gay
		new_map[self.coordinates_gay[0]][self.coordinates_gay[1]] = -1
		coordinates_moving = self.GamerGay.get_step(self.map_compress())
		self.coordinates_gay = (
			self.coordinates_gay[0] + coordinates_moving[0], self.coordinates_gay[1] + coordinates_moving[1])
		new_map[self.coordinates_gay[0], self.coordinates_gay[1]] = 10

		self.viewer(new_map)

		# step straight
		new_map[self.coordinates_straight[0]][self.coordinates_straight[1]] = -1
		coordinates_moving = self.GamerStraight.get_step(self.map_compress())
		self.coordinates_straight = (
			self.coordinates_straight[0] + coordinates_moving[0], self.coordinates_straight[1] + coordinates_moving[1])
		new_map[self.coordinates_straight[0], self.coordinates_straight[1]] = 11

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