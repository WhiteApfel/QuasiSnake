import random
import numpy as np
from collections import deque

from keras import Sequential
from keras.layers import Dense


class OneGame:

	def __init__(self, size=8):
		self.size = size

		model = Sequential()
		model.add(Dense(12, input_dim=(self.size + 2) ** 2, activation='relu'))
		model.add(Dense(122, activation='relu'))
		model.add(Dense(4, activation='sigmoid'))
		model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])  # надо менять

		self.models = deque([model], maxlen=6)
		self.history = deque([self.create_map()], maxlen=6)
		self.start_game()

	def create_map(self):
		locations = []
		[[locations.append([i, j]) for i in range(j % 2, 8, 2)] for j in range(8)]
		a, b = random.choices(locations, k=2)

		local_map = np.ones((self.size, self.size)) # Генерация двумерного массива из единиц
		local_map[a[0]][a[1]] = 4 # Меняем одного игрока на 4
		local_map[b[0]][b[1]] = 5 # Другого игрока
		return np.ravel(np.pad(local_map, pad_width=1, mode="constant", constant_values=-1))
		# Добавляет рамку и переводит двумерку в строчку

	def check_status(self, loc: int):
		local_map = self.history[-1] # для удобства сделал переменную-ссылку
		# -11 это на ряд выше и на один влево. 9 - вправо. Аналогично с +, только вниз
		# -1 это стена, -3 это соперник.
		if local_map[loc-11] in [-1, -3] or local_map[loc-9] in [-1, -3] or \
			local_map[loc+11] in [-1, -3] or local_map[loc+9] in [-1, -3]:
			return True
		else:
			return False

	def start_game(self):
		# Тут надо сделать последовательный запуск self.make_step для двух элементов и так далее.
		pass

	def make_step(self, element):
		local_map = self.history[-1].copy() # Делаем локальную копию
		local_map[local_map == 4] = -2 if element == 4 else -3 # Заменяем игрока "4" на -2, либо на -3, если это враг.
		local_map[local_map == 5] = -2 if element == 5 else -3 # Наоборот.
		now_location = np.argwhere(local_map == -2)[0] # Получаем координату "нас"
		way = self.models[-1].predict(local_map)  # Делаем предсказание
		# np.append(np.ravel(self.history[-1]), element)
		best_rule = way.index(max(way)) # Получаем индекс максимально-вероятного направления
		# 0 - лево верх 1 - право верх
		# 3 - лево низ  2 - право низ

		if self.check_status(now_location): # если есть куда идти
			local_map[now_location + {0:-11, 1:-9, 2:+11, 3:+9}[best_rule] ] = element # Перемещаем игрока
			# Но надо добавить проверку на свободу конкретно по направлению, а не в целом
			local_map[now_location] = -1 # заменяем старую на стену
		else:
			pass  # Тут мы ругаем нейроночку и говорим об окончании игры



Game = OneGame()
print(Game.history[0])
