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

from PSO import PSO
import matplotlib.pyplot as plt
from Benchmark import ackley, griewank, michalewicz, easom
from math import pi


def benchmark_ackley():
    options = PSO.Options()
    options.wi = 0.6
    options.wf = 0.6
    options.cpi = 2
    options.cpf = 2
    options.cgi = 1
    options.cgf = 1
    options.npart = 40
    options.niter = 200
    options.log = False
    d = 10

    # Test Ackley funkcije
    # x*=[0 0 0 ... 0], y* = 0
    print("Ackley")
    pso = PSO(ackley, d, options)
    result = pso.optimize()
    print("Gopt: {}".format(result[0]))
    print("Position: {}".format(result[1]))
    if options.plot:
        plt.scatter([_ for _ in range(1, options.niter + 1)], result[2], marker='x')
        plt.title("Ackley function")
        plt.xlabel("Iteration")
        plt.ylabel("Global best")
        plt.show()


def benchmark_griewank():
    options = PSO.Options()
    options.npart = 40
    options.niter = 200
    options.log = False
    d = 10

    # Test Griewank funkcije
    # x*=[0 0 0 ... 0], y* = 0
    print("\nGriewank")
    pso = PSO(griewank, d, options)
    result = pso.optimize()
    print("Gopt: {}".format(result[0]))
    print("Position: {}".format(result[1]))
    if options.plot:
        plt.scatter([_ for _ in range(1, options.niter + 1)], result[2], marker='x')
        plt.title("Griewank function")
        plt.xlabel("Iteration")
        plt.ylabel("Global best")
        plt.show()


def benchmark_michalewicz():
    options = PSO.Options()
    options.npart = 400
    options.niter = 1000
    options.wi = 0.7
    options.log = False
    d = 10

    # Test Michalewicz funkcija
    # y* = -9.66015 za d=10
    print("\nMichalewicz")
    options.initspan = 0.5
    options.initoffset = 1.7
    options.log = True
    options.plot = False
    pso = PSO(michalewicz, d, options)
    result = pso.optimize()
    print("Gopt: {}".format(result[0]))
    print("Position: {}".format(result[1]))
    if options.plot:
        plt.scatter([_ for _ in range(1, options.niter + 1)], result[2], marker='x')
        plt.title("Michalewicz function")
        plt.xlabel("Iteration")
        plt.ylabel("Global best")
        plt.show()


def benchmark_easom():
    options = PSO.Options()
    options.npart = 40
    options.niter = 200
    options.log = False
    options.initspan = 100
    d = 2

    # Test Easom funkcije
    # x* = [pi,pi], y*=-1
    print("\nEasom")
    pso = PSO(easom, d, options)
    result = pso.optimize()
    print("Gopt: {}".format(result[0]))
    print("Position: {}".format(result[1]))
    if options.plot:
        plt.scatter([_ for _ in range(1, options.niter + 1)], result[2], marker='x')
        plt.title("Easom function")
        plt.xlabel("Iteration")
        plt.ylabel("Global best")
        plt.show()


if __name__ == '__main__':
    benchmark_ackley()
    benchmark_griewank()
    #benchmark_easom()
    benchmark_michalewicz()



