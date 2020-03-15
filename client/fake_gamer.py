import requests


class Gamer:
	def __init__(self, size):
		self.size = size
		self.ip = "0.0.0.0"
		self.port = "54321"

	def get_step(self, map_array):
		to_send = {"map": map_array}
		r: str = requests.post(f"http://{self.ip}:{self.port}/get_step", json=to_send).text
		return {1: [-1, -1], 2: [-1, 1], 3: [1, 1], 4: [1, -1]}[int(r)]

	def bdsm(self, map_array):
		to_send = {"map": map_array}
		requests.post(f"http://{self.ip}:{self.port}/bdsm", json=to_send)
