from keras import Sequential
from keras.layers import Dense


class Gamer:
	def __init__(self, size):
		self.size = size
		self.model = self.create_model()
		self.step_decode = {1: [-1, -1], 2: [-1, 1], 3: [1, 1], 4: [1, -1]}

	def predict_step(self, local_map):
		pred = self.model.predict(local_map)
		return pred.index(max(pred)) + 1

	def get_step(self, local_map) -> list:
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

	def counter_steps(self, map_array, my_index):
		# TODO Надо доделать код
		x = my_index[0]
		y = my_index[1]
		for i in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
			if map_array[x + i[0]][y + i[1]] == 1:
				map_array[x + i[0]][y + i[1]] = -1
				# каунтер надо вернуть
				self.counter_steps(map_array, [x + i[0], y + i[1]])

	def bdsm(self, map_array, available):
		# __ Надо доделать наказание
		self.model.fit(map_array, available)

	def gingerbread(self):
		# кнут можно без пряника оставаить
		pass
