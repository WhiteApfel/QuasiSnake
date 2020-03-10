import random
import numpy as np
from collections import deque
from copy import deepcopy
import matplotlib.pyplot as plt
import time

from keras import Sequential
from keras.layers import Dense

class Map_controller:

	def __init__(self, size):
		self.size = size
		self.map = self.gen_map()
		self.step_counter = 0
		self.GameOne = Game(self.map, self.size)
		self.GameTwo = Game(self.map, self.size)

	def gen_map(self):
		return False

	def make_step(self, who, gender_step):

		pass


class Game:

	def __init__(self, size, m):
		self.size = size
		self.map = m
		self.model = self.create_model()
		pass

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

		pass