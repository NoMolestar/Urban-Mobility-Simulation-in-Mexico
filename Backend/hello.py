from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit
import _thread
import time

# Model design
import agentpy as ap
import math
import random

app = Flask(__name__, static_url_path="")

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv("PORT", 5000))


class IntersectionModel(ap.Model):
    def setup(self):

        # trafficLights positions
        trafficLightsPositions = [(12, 10), (10, 12), (8, 25), (10, 27)]

        # Create agents
        self.trafficLights = ap.AgentList(self, 4)
        self.cars = ap.AgentList(self, self.p.cars)

        # Create grid (room)
        self.intersection = ap.Grid(self, (20, 40), torus=True, track_empty=True)
        self.intersection.add_agents(
            self.trafficLights, trafficLightsPositions, empty=False
        )
        self.intersection.add_agents(self.cars, random=True, empty=True)

        # Initiate a dynamic variable for cars
        # Moving 0: false, 1: true
        self.cars.moving = 1
        # direction 0: up, 1: down, 2: left, 3: right
        for car in self.cars:
            carDirection = random.randint(0, 2)
            if carDirection == 0:
                car.direction = carDirection
                self.intersection.move_to(
                    car, (random.randint(14, 20), 11)
                )  # (random.randint(13,20),carPositions[3])
            elif carDirection == 1:
                car.direction = carDirection
                self.intersection.move_to(
                    car, (9, random.randint(14, 20))
                )  # (carPositions[1],random.randint(13,20)))
            elif carDirection == 2:
                car.direction = carDirection
                self.intersection.move_to(car, (random.randint(0, 6), 24))

        self.cars.color = 3
        self.cars.id = 1000

        # Initiate a dynamic variable for trafficLights
        # Color 0: red(stop), 1: yellow(slow), 2: green(go) 3: cars
        self.trafficLights.color = 1
        self.trafficLights.direction = 10000
        self.trafficLights.cooldown = 0

        i = 0
        # Give Ids to the traffic lights
        for trafficLight in self.trafficLights:
            trafficLight.id = i
            i += 1

    def step(self):

        time.sleep(1)
        minTrafficLightID = 0
        min = 100000
        # Find the traffic light with the closer car
        for trafficLight in self.trafficLights:
            if trafficLight.id == 0 or trafficLight.id == 1:
                for neighbor in self.intersection.neighbors(trafficLight, 2):
                    pos1 = self.intersection.positions[neighbor]
                    pos2 = self.intersection.positions[trafficLight]
                    distance = math.sqrt(
                        (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2
                    )
                    if min > distance and neighbor.direction == trafficLight.id:
                        min = distance
                        minTrafficLightID = trafficLight.id

        # If no cars are found nearby, turn all intersection traffic lights yellow
        if min == 100000:
            trafficLight = self.trafficLights.select(self.trafficLights.id == 0)
            trafficLight[0].color = 1
            trafficLight = self.trafficLights.select(self.trafficLights.id == 1)
            trafficLight[0].color = 1
        else:
            # Turn Green the Traffic Light with the Closest Car
            trafficLight = self.trafficLights.select(
                self.trafficLights.id == minTrafficLightID
            )
            if trafficLight[0].id == 0:
                trafficLight.color = 2
                trafficLight = self.trafficLights.select(self.trafficLights.id == 1)
                trafficLight[0].color = 0
            else:
                trafficLight[0].color = 2
                trafficLight = self.trafficLights.select(self.trafficLights.id == 0)
                trafficLight[0].color = 0

        # controlador interseccion2
        minTrafficLightID = 0
        min = 100000
        # Find the traffic light with the closer car
        for trafficLight in self.trafficLights:
            if trafficLight.id == 2 or trafficLight.id == 3:
                for neighbor in self.intersection.neighbors(trafficLight, 2):
                    pos1 = self.intersection.positions[neighbor]
                    pos2 = self.intersection.positions[trafficLight]
                    distance = math.sqrt(
                        (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2
                    )
                    if min > distance and (
                        neighbor.direction == trafficLight.id
                        or (neighbor.direction == 1 and trafficLight.id == 3)
                    ):
                        min = distance
                        minTrafficLightID = trafficLight.id

        # If no cars are found nearby, turn all intersection traffic lights yellow
        if min == 100000:
            trafficLight = self.trafficLights.select(self.trafficLights.id == 2)
            trafficLight[0].color = 1
            trafficLight = self.trafficLights.select(self.trafficLights.id == 3)
            trafficLight[0].color = 1
        else:
            # Turn Green the Traffic Light with the Closest Car
            trafficLight = self.trafficLights.select(
                self.trafficLights.id == minTrafficLightID
            )
            if trafficLight[0].id == 2:
                trafficLight[0].color = 2
                trafficLight = self.trafficLights.select(self.trafficLights.id == 3)
                trafficLight[0].color = 0
            else:
                trafficLight[0].color = 2
                trafficLight = self.trafficLights.select(self.trafficLights.id == 2)
                trafficLight[0].color = 0

        # Car movement, car won't move if corresponding traffic light is red
        for car in self.cars.select(self.cars.moving == 1):

            if car.direction == 0:  ##Up

                for neighbor in self.intersection.neighbors(car, 2):
                    if (
                        neighbor.color == 0
                        and neighbor.id == car.direction
                        and self.intersection.positions[neighbor][0]
                        - self.intersection.positions[car][0]
                        == -2
                    ):
                        car.moving = 1  # cambiar esto
                        break
                else:
                    for neighbor in self.intersection.neighbors(car):
                        if (
                            neighbor.color == 3
                            and (
                                self.intersection.positions[neighbor][0]
                                - self.intersection.positions[car][0]
                            )
                            == -1
                            and (
                                self.intersection.positions[neighbor][1]
                                - self.intersection.positions[car][1]
                            )
                            == 0
                        ):
                            break
                    else:
                        self.intersection.move_by(car, (-1, 0))

            elif car.direction == 1:  ##left

                for neighbor in self.intersection.neighbors(car, 2):
                    if (
                        neighbor.color == 0
                        and (neighbor.id == car.direction or neighbor.id == 3)
                        and self.intersection.positions[neighbor][1]
                        - self.intersection.positions[car][1]
                        == -2
                    ):
                        car.moving = 1  # cambiar esto
                        break
                else:
                    for neighbor in self.intersection.neighbors(car):
                        if (
                            neighbor.color == 3
                            and (
                                self.intersection.positions[neighbor][1]
                                - self.intersection.positions[car][1]
                            )
                            == -1
                            and (
                                self.intersection.positions[neighbor][0]
                                - self.intersection.positions[car][0]
                            )
                            == 0
                        ):
                            break
                    else:
                        self.intersection.move_by(car, (0, -1))

            elif car.direction == 2:  ##down

                for neighbor in self.intersection.neighbors(car, 2):
                    if (
                        neighbor.color == 0
                        and neighbor.id == car.direction
                        and self.intersection.positions[neighbor][0]
                        - self.intersection.positions[car][0]
                        == 2
                    ):
                        car.moving = 1  # cambiar esto
                        break
                else:
                    for neighbor in self.intersection.neighbors(car):
                        if (
                            neighbor.color == 3
                            and (
                                self.intersection.positions[neighbor][0]
                                - self.intersection.positions[car][0]
                            )
                            == 1
                            and (
                                self.intersection.positions[neighbor][1]
                                - self.intersection.positions[car][1]
                            )
                            == 0
                        ):
                            break
                    else:
                        self.intersection.move_by(car, (1, 0))

        carsOnStep = []
        count = 0
        for car in self.cars:
            carsOnStep.append(
                {
                    "valor": self.intersection.positions[car],
                    "direccion": car.direction,
                }
            )
            count = count + 1

        semaforos = []
        count = 0
        for trafficLight in self.trafficLights:
            semaforos.append(
                {
                    "color": trafficLight.color,
                }
            )

        Data = {
            "data": [
                {
                    "semaforo": semaforos,
                    "posiciones": carsOnStep,
                }
            ]
        }

        with open("data.txt", "w") as outfile:
            json.dump(Data, outfile)


def print_time(carros):
    parameters = {
        "cars": carros,  # Number of cars
    }
    model = IntersectionModel(parameters)
    model.run()


try:
    _thread.start_new_thread(
        print_time,
        (10,),
    )
except:
    print("Error: unable to start thread")


@app.route("/")
def root():
    try:
        with open("data.txt") as json_file:
            data = json.load(json_file)
            return jsonify(data)
    except:
        return "No terminó"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
