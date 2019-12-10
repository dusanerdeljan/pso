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


# Ackley - test case 1
def ackley(x):
    s1 = 0
    s2 = 0
    d = len(x)
    for xi in x:
        s1 += xi**2
        s2 += cos(2*pi*xi)
    s1 = -0.2*sqrt((1/d)*s1)
    s2 = (1/d)*s2
    return -20*exp(s1) - exp(s2) + 20 + exp(1)


# Griewank - test case 2
def griewank(x):
    s1 = 0
    p2 = 1
    d = len(x)
    for i in range(d):
        s1 += (x[i]**2)/4000
        p2 *= cos(x[i]/(sqrt(i+1)))
    return s1 - p2 + 1


# Michalewicz - test case 3
def michalewicz(x):
    s1 = 0
    d = len(x)
    for i in range(d):
        s1 += sin(x[i])*(sin((x[i]**2 * (i+1))/pi))**20
    return -s1


# Easom - test case 4
def easom(x):
    p1 = -cos(x[0])*cos(x[1])
    p2 = exp(-(x[0] - pi)**2 - (x[1] - pi)**2)
    return p1*p2

