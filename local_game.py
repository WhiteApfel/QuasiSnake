import random
import numpy as np
from collections import deque

from keras import Sequential
from keras.layers import Dense


class OneGame:

	def __init__(self, size=8):
		self.size = size

		model = Sequential()
		model.add(Dense(12, input_dim=(self.size + 1) ** 2, activation='relu'))
		model.add(Dense(122, activation='relu'))
		model.add(Dense(1, activation='sigmoid'))
		model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])  # надо менять

		self.models = deque([model], maxlen=6)
		self.history = deque([self.create_map()], maxlen=6)

	def create_map(self):
		a, b = random.choices(range(64), k=2)
		local_map = np.ones(self.size ** 2)
		local_map[a] = 0
		local_map[b] = 0
		return np.pad(np.reshape(local_map, (self.size, self.size)), pad_width=1, mode="constant", constant_values=-1)

	def start_game(self):
		pass


Game = OneGame()
print(Game.history[0])
