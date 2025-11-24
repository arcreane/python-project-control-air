import random as rnd
from math import*
from PySide6.QtWidgets import QFrame



class Avion():
    def __init__(self, position_x, position_y, altitude, vitesse, cap, carburant):
        self.x = position_x
        self.y = position_y
        self.altitude = altitude
        self.vitesse = vitesse
        self.cap = cap
        self.carburant = carburant
    def new_coords(self):
        self.x = rnd.randint(self.cap[0], self.cap[1])
        self.y = rnd.randint(self.cap[0], self.cap[1])
        print(f"x : {self.x}")


avion = Avion(30,30,2000,200,[0,360],1000)
avion.new_coords()








