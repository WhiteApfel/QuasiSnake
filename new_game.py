import random
import numpy as np
from collections import deque
from copy import deepcopy
import matplotlib.pyplot as plt
import time

from keras import Sequential
from keras.layers import Dense


class MapController:

	def __init__(self, size):
		plt.ion()
		self.map_history = deque([], maxlen=32)
		self.size = size
		self.gen_map()
		self.step_counter = 0
		self.available_a = 0
		self.available_b = 0

		self.GamerGay = Gamer(self.size)
		self.GamerStraight = Gamer(self.size)
		self.coordinatesGay = (0, 0)
		self.coordinatesStraight = (0, 0)

	def viewer(self, local_map):
		plt.imshow(local_map, cmap='hot', interpolation='nearest')
		plt.show()
		plt.pause(0.0001)
		plt.clf()

	def map_compression(self):
		CMap = list()
		for y in range(0, len(self.map_history[-1]), 2):
			for x in range(0, len(self.map_history[-1]), 2):
				list.append(self.map_history[-1][x][y])
		return CMap

	def gen_map(self):
		locations = []
		[[locations.append([i, j]) for i in range(j % 2, self.size, 2)] for j in
		 range(self.size)]  # Генерирует "черные" клетки
		a, b = 0, 0
		while a == b:
			a, b = random.choices(locations, k=2)  # Выбор двух случайных разных

		local_map = np.ones((self.size, self.size))  # Генерация двумерного массива из единиц
		local_map[a[0]][a[1]] = 10  # Меняем одного игрока на 10
		local_map[b[0]][b[1]] = 11  # Другого игрока на 11
		self.map_history.append(local_map)

	def compress_map(self):
		local_map = deepcopy(self.map_history[-1])
		compressed = []
		for i, in range(self.size):
			compressed.append([local_map[j] for j in range(i % 2, self.size+2, 2)])
		return compressed

	def make_step(self):
		newMap = deepcopy(self.map_history[-1])

		self.viewer(newMap)

		# step gay
		newMap[self.coordinatesGay[0]][self.coordinatesGay[1]] = -1
		coordinatesMoving = self.GamerGay.get_step(self.compression_map())
		self.coordinatesGay = (
			self.coordinatesGay[0] + coordinatesMoving[0], self.coordinatesGay[1] + coordinatesMoving[1])
		newMap[self.coordinatesGay[0], self.coordinatesGay[1]] = 10

		self.viewer(newMap)

		# step straight
		newMap[self.coordinatesStraight[0]][self.coordinatesStraight[1]] = -1
		coordinatesMoving = self.GamerStraight.get_step(self.compression_map())
		self.coordinatesStraight = (
			self.coordinatesStraight[0] + coordinatesMoving[0], self.coordinatesStraight[1] + coordinatesMoving[1])
		newMap[self.coordinatesStraight[0], self.coordinatesStraight[1]] = 11

		self.viewer(newMap)

		self.map_history.append(newMap)

	def get_available_step(self, who):
		a = self.map_history[-1][0]
		return a * 2 if who == -10 else a * 3

	def update_map_info(self):
		self.available_a = self.get_available_step(-10)
		self.available_b = self.get_available_step(-11)


class Gamer:
	def __init__(self, size):
		self.size = size
		self.model = self.create_model()
		self.step_decode = {1: -5, 2: -4, 3: 4, 4: 3}

	def predict_step(self, map):
		pred = self.model.predict(map)
		return pred.index(max(pred))+1

	def get_step(self, local_map):
		step = self.predict_step(local_map)
		return self.step_decode[step]

	def create_model(self):
		model = Sequential()
		model.add(Dense(22, input_dim=(self.size + 2) ** 2 // 2, activation='relu'))
		model.add(Dense(14, activation='relu'))
		model.add(Dense(9, activation='relu'))
		model.add(Dense(4, activation='sigmoid'))
		model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])  # надо менять
		return model

	def counter_steps(self, map_array, myIndex):
		x = myIndex[0]
		y = myIndex[1]
		for i in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
			if (map_array[x + i[0]][y + i[1]] == 1):
				map_array[x + i[0]][y + i[1]] = -1
				# каунтер надо вернуть
				self.counter_steps(map_array, [x + i[0], y + i[1]])

	def bdsm(self, map_array, available):
		self.model.fit(map_array, available)

	def gingerbread(self):
		# кнут можно без пряника оставаить
		pass
