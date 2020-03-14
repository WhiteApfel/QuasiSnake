from copy import deepcopy
import numpy as np
from keras import Sequential
from keras.layers import Dense
from keras.models import load_model


class Gamer:
	def __init__(self, size: int):
		self.size = size
		try:
			self.model = load_model("model.h5")
		except Exception as e:
			print(f"Ошибочка вышла... {e}")
			self.model = self.create_model
		self.counter = 0
		self.step_decode = {1: [-1, -1], 2: [-1, 1], 3: [1, 1], 4: [1, -1]}

	@property
	def create_model(self):
		model = Sequential()
		model.add(Dense(22, input_dim=(self.size + 2) ** 2 // 2, activation='relu'))
		model.add(Dense(14, activation='relu'))
		model.add(Dense(9, activation='relu'))
		model.add(Dense(4, activation='sigmoid'))
		model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])  # надо менять
		return model

	def predict_step(self, local_map):
		pred = self.model.predict(np.array([local_map])).tolist()[0]
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

	@staticmethod
	def get_available(map_array):
		to_return = []
		loc = map_array.index(-2)
		to_check = [-5, -4, 6, 5] if (loc // 10) % 2 == 1 else [-6, -5, 5, 4]
		for i in to_check:
			to_return.append(int(map_array[loc + i] not in [-1, -3]))
		return to_return

	def bdsm(self, map_array):
		# TODO: Надо доделать наказание
		self.model.fit(np.array([map_array]), np.array([self.get_available(map_array)]))
		self.model.save("model.h5")
