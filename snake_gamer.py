from copy import deepcopy
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
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
		self.step_decode = {0: [-1, -1], 1: [-1, 1], 2: [1, 1], 3: [1, -1]}

	@property
	def create_model(self):
		model = Sequential()
		model.add(Dense(22, input_dim=(self.size + 2) ** 2 // 2, activation='relu'))
		model.add(Dense(12, activation='relu'))
		model.add(Dense(8, activation='relu'))
		model.add(Dense(4, activation='sigmoid'))
		model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])  # надо менять
		return model

	def predict_step(self, map_array) -> int:
		pred = self.model.predict(np.array([map_array])).tolist()[0]
		return pred.index(max(pred))

	def get_step(self, map_array) -> list:
		return self.step_decode[self.bdsm(map_array)]

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
		to_check = [-5, -4, 6, 5] if (loc // 5) % 2 == 1 else [-6, -5, 5, 4]
		for i in to_check:
			to_return.append(int(map_array[loc + i] != -1))
		return to_return

	def bdsm(self, map_array):
		# TODO: Надо доделать наказание
		need = self.get_available(map_array)
		ps = self.predict_step(map_array)
		while ps not in [i for i, x in enumerate(need) if x == 1] and need != [0, 0, 0, 0]:
			self.model.fit(np.array([map_array]), np.array([need]), verbose=0)
			ps = self.predict_step(map_array)
		ps = self.model.predict(np.array([map_array])).tolist()[0]
		self.model.save("model.h5")
		step = ps.index(max(ps))
		return step
