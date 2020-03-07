import random
import numpy as np
from collections import deque

from keras import Sequential
from keras.layers import Dense


class OneGame:

	def __init__(self, size=8):
		self.size = size

		model = Sequential()
		model.add(Dense(12, input_dim=(self.size + 1) ** 2 + 1, activation='relu'))
		model.add(Dense(122, activation='relu'))
		model.add(Dense(4, activation='sigmoid'))
		model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])  # надо менять

		self.models = deque([model], maxlen=6)
		self.history = deque([self.create_map()], maxlen=6)

		self.start_game()

	def create_map(self):
		a, b = random.choices(range(64), k=2)  # надо придумать нормальную генерацию на одних диагоналях
		local_map = np.ones(self.size ** 2)
		local_map[a] = -2
		local_map[b] = -3
		return np.pad(np.reshape(local_map, (self.size, self.size)), pad_width=1, mode="constant", constant_values=-1)

	def check_status(self, loc: list):
		x = loc[0]
		y = loc[1]
		local_map = self.history[-1]
		if local_map[x - 1][y - 1] == 1 or local_map[x - 1][y + 1] or local_map[x + 1][y - 1] or local_map[x + 1][y + 1]:
			return True
		else:
			return False

	def start_game(self):
		pass

	def make_step(self, element):
		way = self.models[-1].predict(np.append(np.ravel(self.history[-1], element)))
		best_rule = way.index(max(way))
		if best_rule == 0:
			pass
		elif best_rule == 1:
			pass
		elif best_rule == 2:
			pass
		else:
			pass
		pass


Game = OneGame()
print(Game.history[0])
