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

from math import sin, cos, exp, pi, sqrt
from pso.PSO import PSO
import matplotlib.pyplot as plt


def ackley(x):
    """
    Ackley function - test case 1
    Arguments:
        x(list): Position
    Returns:
        float: Function evaluation at the given position
    """
    s1 = 0
    s2 = 0
    d = len(x)
    for xi in x:
        s1 += xi**2
        s2 += cos(2*pi*xi)
    s1 = -0.2*sqrt((1/d)*s1)
    s2 = (1/d)*s2
    return -20*exp(s1) - exp(s2) + 20 + exp(1)


def griewank(x):
    """
    Griewank function - test case 2
    Arguments:
        x(list): Position
    Returns:
        float: Function evaluation at the given position
    """
    s1 = 0
    p2 = 1
    d = len(x)
    for i in range(d):
        s1 += (x[i]**2)/4000
        p2 *= cos(x[i]/(sqrt(i+1)))
    return s1 - p2 + 1



def michalewicz(x):
    """
    Michalewicz function - test case 3
    Arguments:
        x(list): Position
    Returns:
        float: Function evaluation at the given position
    """
    s1 = 0
    d = len(x)
    for i in range(d):
        s1 += sin(x[i])*(sin((x[i]**2 * (i+1))/pi))**20
    return -s1


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
    options.niter = 500
    options.wi = 0.7
    options.wf = 0.55015
    options.cgf = 1.50
    options.cpf = 1.50
    options.log = False
    d = 10

    # Test Michalewicz funkcija
    # y* = -9.66015 za d=10
    print("\nMichalewicz")
    options.initspan = 0.4
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


def benchmark(objfunc, dimension, options, logfunc=None):
    """
    Minimizes objfunc using PSO algorithm
    Arguments:
        objfunc(Function): Objective function
        dimension(int): Dimension of the problem, number of variables
        options(PSO.Options): Algorithm options
        logfunc(Function): Callback function which is called every 10 iterations if options.log is enabled
    Returns:
        result[0](float): Global optimum of the objective function
        result[1](list): Position of the global optimum
        result[2](list): List of all the global bests throughout the iterations
    """
    pso = PSO(objfunc, dimension, options)
    result = pso.optimize(logfunc)
    return result[0], result[1], result[2]


if __name__ == '__main__':
    benchmark_ackley()
    benchmark_griewank()
    benchmark_michalewicz()

