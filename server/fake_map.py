from flask import Flask, request
import json
from snake_gamer import Gamer
import numpy as np

gamer_gay = Gamer(8)

app = Flask("QuasiSnake")


@app.route("/get_step", methods=["POST"])
def get_step():
	to_json = str(request.data)[2:-1]
	map_array = json.loads(to_json)["map"]
	return str(gamer_gay.predict_step(map_array))


@app.route("/bdsm", methods=["POST"])
def bdsm():
	to_json = str(request.data)[2:-1]
	map_array = json.loads(to_json)["map"]
	gamer_gay.bdsm(map_array)
	return "ok"


app.run(host="0.0.0.0", port=54321, threaded=False)
