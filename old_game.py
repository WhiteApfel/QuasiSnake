import random
import numpy as np
from collections import deque
from copy import deepcopy
import matplotlib.pyplot as plt
import time

from keras import Sequential
from keras.layers import Dense


class OneGame:

	def __init__(self, size=8):
		self.size = size
		self.next = True
		self.max_steps = 0
		self.base_map = [self.create_map()]
		model = Sequential()
		model.add(Dense(12, input_dim=(self.size + 2) ** 2, activation='relu'))
		model.add(Dense(122, activation='relu'))
		model.add(Dense(14, activation='relu'))
		model.add(Dense(4, activation='sigmoid'))
		model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])  # надо менять

		self.model = deepcopy(model)
		self.models = deque([model], maxlen=6)
		self.history_map = deque(self.base_map, maxlen=32)
		for _ in range(2000):
			self.start_game()


	def create_map(self):
		locations = []
		[[locations.append([i, j]) for i in range(j % 2, 8, 2)] for j in range(8)]  # Генерирует "черные" клетки
		a, b = 1, 1
		while a == b:
			a, b = random.choices(locations, k=2)  # Выбор двух случайных разных

		local_map = np.ones((self.size, self.size))  # Генерация двумерного массива из единиц
		local_map[a[0]][a[1]] = 4  # Меняем одного игрока на 4
		local_map[b[0]][b[1]] = 5  # Другого игрока
		return np.ravel(np.pad(local_map, pad_width=1, mode="constant", constant_values=-1))

	# Добавляет рамку и переводит двумерку в одномерный лист

	def check_status(self, loc: int):
		local_map = self.history_map[-1]  # для удобства сделал переменную-ссылку
		# -11 это на ряд выше и на один влево. 9 - вправо. Аналогично с только 9 уже влево, только вниз
		# -1 это стена, -3 это соперник.
		to_return = []
		for i in [-11, -9, 11, 9]:
			to_return.append(int(local_map[loc + i] not in [-1, -3]))
		return to_return

	def start_game(self):
		i = 0
		while self.next:  # Пока никто не оказался в тупике поочередно играем
			if i % 2 == 0:
				self.make_step(4)
			else:
				self.make_step(5)
			i -= -1

	def bdsm(self, loc):
		self.history_map = deque(self.base_map, maxlen=32)
		self.model.fit(np.array([self.history_map[-1]]), np.array([self.check_status(loc)]))
		# self.models = deque([self.models[0]], maxlen=6)
		# self.models.append(deepcopy(self.models[-1]))
		# self.models[-1].fit(np.array([self.history_map[-1]]), np.array([self.check_status(loc)]))
		# надо переделать систему наказаний, это для общего представления сделано
		pass

	def gingerbread(self):
		# должна хвалить модель
		pass

	def make_step(self, element):
		local_map = deepcopy(self.history_map[-1])  # Делаем локальную копию
		local_map[local_map == 4] = -2 if element == 4 else -3  # Заменяем игрока "4" на -2, либо на -3, если это враг.
		local_map[local_map == 5] = -2 if element == 5 else -3  # Наоборот.
		now_location = np.argwhere(local_map == -2)
		if not len(now_location):
			print(self.history_map)
		now_location = now_location[0]  # Получаем координату "нас"
		self.model.fit(np.array([local_map]), np.array([self.check_status(now_location)]))
		way = self.model.predict(np.array([local_map]))[0]  # Делаем предсказание
		# np.append(np.ravel(self.history[-1]), element)
		best_rule = way.tolist().index(max(way.tolist()))  # Получаем индекс максимально-вероятного направления
		# 0 - лево верх 1 - право верх
		# 3 - лево низ  2 - право низ

		# Надо переделать логику этого блока. Разделить на тупик и просто на шаг не туда
		if (self.check_status(now_location) != [0, 0, 0, 0]) and \
				(local_map[now_location + {0: -11, 1: -9, 2: +11, 3: +9}[best_rule]] not in [-1, -3]):

			local_map[now_location + {0: -11, 1: -9, 2: +11, 3: +9}[best_rule]] = element  # Перемещаем игрока
			# Но надо добавить проверку на свободу конкретно по направлению, а не в целом
			local_map[now_location] = -1  # заменяем старую на стену

			local_map[local_map == -2] = 4 if element == 4 else 5
			local_map[local_map == -3] = 4 if element == 5 else 5
			plt.imshow(np.reshape(local_map, (10, 10)), cmap='hot', interpolation='nearest')
			plt.show()
			plt.pause(0.0001)
			plt.clf()
			self.history_map.append(local_map)
			self.max_steps += 1
		else:
			self.bdsm(now_location)
			self.next = False
			pass  # Тут мы ругаем нейроночку и говорим об окончании игры


def visual(maps):
	for onemap in maps:
		np.reshape(onemap, (10, 10))
		print(np.reshape(onemap, (10, 10)))


plt.ion()
Game = OneGame()
maps = Game.history_map
while len(maps) < 5:
	Game = OneGame()
	maps = Game.history_map
visual(Game.history_map)
