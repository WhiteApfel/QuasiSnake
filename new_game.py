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
		self.map_history = deque([], maxlen=32)
		self.size = size
		self.gen_map()

		self.step_counter = 0
		self.available_a = 0
		self.available_b = 0

		self.GamerGay = Gamer(self.size)
		self.GamerStraight = Gamer(self.size)

	def gen_map(self):
		map_array = np.ones(self.size * self.size // 2)
		a, b = 0, 0
		while a == b:
			a, b = [random.randint(0, 31) for _ in [a, b]]
		map_array[a] = -10
		map_array[b] = -11
		self.map_history.append(map_array)

	def make_step(self, who, gender_step):
		pass

	def get_available_step(self, who):
		a = self.map_history[-1][0]
		return a*2 if who == -10 else a*3

	def update_map_info(self):
		self.available_a = self.get_available_step(-10)
		self.available_b = self.get_available_step(-11)


class Gamer:
	def __init__(self, size):
		self.size = size
		self.model = self.create_model()

	def create_model(self):
		model = Sequential()
		model.add(Dense(22, input_dim=(self.size + 2) ** 2 // 2, activation='relu'))
		model.add(Dense(14, activation='relu'))
		model.add(Dense(9, activation='relu'))
		model.add(Dense(4, activation='sigmoid'))
		model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])  # надо менять
		return model

	def bdsm(self):
		pass

	def gingerbread(self):
		# кнут можно без пряника оставаить
		pass

	def step_predict(self, map_array, gamer):
		return self.model.predict(map_array, gamer)