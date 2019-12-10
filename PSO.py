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
import random
from Particle import Particle


class PSO(object):

    class Options(object):

        def __init__(self):
            """
            PSO algorithm options
            """
            self.npart = 30
            self.niter = 100
            self.cpi = 2.5
            self.cpf = 0.5
            self.cgi = 0.5
            self.cgf = 2.5
            self.wi = 0.9
            self.wf = 0.4
            self.vmax = inf
            self.initoffset = 0
            self.initspan = 1
            self.vspan = 1
            self.plot = False
            self.log = False

    def __init__(self, objfunc, dimension, opts=None):
        """
        Implementation of Particle Swarm Optimization algorithm
        Arguments:
            objfunc(Function): Objective function
            dimension(int): Dimension of the problem, the number of the variables
            opts(PSO.Options): Algorithm options, if None default options will be used
        """
        Particle.global_best_position = None
        Particle.global_best = inf
        self.options = opts if opts else PSO.Options()
        self.linrate_cp = self.linear_interpolation(self.options.cpi, self.options.cpf)
        self.linrate_cg = self.linear_interpolation(self.options.cgi, self.options.cgf)
        self.linrate_w = self.linear_interpolation(self.options.wi, self.options.wf)
        self.particles = None
        self.dimension = dimension
        self.objfunc = objfunc
        self.init_population()

    def optimize(self):
        """
        Optimizes the objective function
        Returns:
            Array which is consisted of: 1. Global best evaluation
                                         2. Global best position
                                         3. History of the global best evaluations throughout the iterations
        """
        history = [0.0]*self.options.niter
        for iteration in range(1, self.options.niter+1):
            w = self.linrate_w(iteration)
            cp = self.linrate_cp(iteration)
            cg = self.linrate_cg(iteration)
            for particle in self.particles:
                particle.update(w, cp, cg, self.objfunc, self.options.vmax)
            if self.options.log and iteration % 10 == 0:
                print(f"Iter #{iteration}, GBEST: {Particle.global_best}")
            history[iteration-1] = Particle.global_best
        return [Particle.global_best, Particle.global_best_position, history]

    def init_population(self):
        """
        Initializes particle population
        """
        self.particles = []
        for i in range(self.options.npart):
            velocity = [0]*self.dimension
            position = [0]*self.dimension
            for j in range(self.dimension):
                velocity[j] = random.uniform(-self.options.vspan, self.options.vspan)
                position[j] = random.uniform(-self.options.initspan, self.options.initspan) + self.options.initoffset
            self.particles.append(Particle(position, velocity))
        for particle in self.particles:
            particle.evaluate(self.objfunc)

    def linear_interpolation(self, y0, y1):
        """
        Returns linear interpolation polynomial
        Arguments:
            y0(float): Initial value of some parameter
            y1(float): Final value of some parameter
        Returns:
            y(Function): Approximation polynomial function
        """
        x0 = 1
        x1 = self.options.niter

        def y(x):
            return y0 + (x - x0)*(y1-y0)/(x1-x0)
        return y

    def __str__(self):
        """
        String operator
        Returns:
            The string representation of the algorithm
        """
        return "\n".join([str(particle) for particle in self.particles])
