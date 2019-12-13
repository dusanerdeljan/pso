"""
    Python implementation of PSO (Particle Swarm Optimization) algorithm.
    Copyright (C) 2019  Dušan Erdeljan, Dimitrije Karanfilović

    This file is part of pso.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from math import inf
from random import uniform


class Particle(object):
    global_best = inf
    global_best_position = None

    def __init__(self, position, v):
        """
        Class models a particle in the swarm
        Arguments:
            position(list): Initial position of the particle
            v(list): Initial velocity of the particle
        """
        self.position = [x for x in position]
        self.v = [x for x in v]
        self.personal_best: float = inf
        self.personal_best_position = None
        self.value: float = inf

    def evaluate(self, objfunc):
        """
        Evaluates the objective function in the particle's position, and updates PB and GB if necessary
        Arguments:
            objfunc(Function): Objective function
        """
        self.value = objfunc(self.position)
        if self.value < self.personal_best:
            self.personal_best = self.value
            self.personal_best_position = [x for x in self.position]
        if self.personal_best < Particle.global_best:
            Particle.global_best = self.personal_best
            Particle.global_best_position = [x for x in self.personal_best_position]

    def update(self, w, cp, cg, objfunc, vmax):
        """
        Updates the particle's position
        Arguments:
            w(float): Inertia coefficient
            cp(float): Cognitive coefficient
            cg(float): Social coefficient
            objfunc(Function): Objective function
            vmax(float): Maximal velocity that a particle can have
        """
        for i in range(len(self.position)):
            rp = uniform(0, 1)
            rg = uniform(0, 1)
            self.v[i] = w * self.v[i] + rp * cp * (self.personal_best_position[i] - self.position[i]) + rg * cg * (
                    Particle.global_best_position[i] - self.position[i])
            sign = 1 if self.v[i] > 0 else -1
            self.v[i] = min(vmax, abs(self.v[i])) * sign
            self.position[i] = self.position[i] + self.v[i]
        self.evaluate(objfunc)

    def __str__(self):
        """
        Redefined string operator
        Returns:
            String representation of the particle
        """
        return "Position: {}, value: {}, personal best: {}".format(self.position, self.value, self.personal_best)
