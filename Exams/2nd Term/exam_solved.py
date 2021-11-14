#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 19:12:26 2021

@author: nikorose
"""

import pandas as pd 
import numpy as np
from sympy.physics.continuum_mechanics.beam import Beam
from sympy import symbols
def solve_beam(Ft, Lt, Fp, LFp, M, L_M, Fr, L_Fr, show=False): # $F_t$	Lt	Fp	LFp	M	L_M	Fr	L_Fr0
    E, I = symbols('E, I')
    b = Beam(6, E, I)
    b.apply_support(0, "pin")
    b.apply_support(4, "roller")
    R_0, R_4 = symbols('R_0, R_4')
    b.apply_load(Fp, LFp, -1) # Force
    b.apply_load(M, L_M, -2) # Moment
    b.apply_load(Fr, L_Fr, 0, 6) # Rectangular force
    b.apply_load(Ft/Lt, 0, 1, Lt) # Triangle Force
    b.solve_for_reaction_loads(R_0, R_4)
    if show:
        p = b.draw()
        p.show()
        b.plot_bending_moment()
        b.plot_shear_force()
    return {'Moment': b.max_bmoment(), "Max_shear": b.max_shear_force()}

classlist1 = pd.read_excel("https://www.dropbox.com/s/9khod9m3orvc8jl/MoM%202021%20II%20Asistencia.xlsx?dl=1")

not_lock = False
list_ben = classlist1.copy()
if not_lock:
    list_ben['$F_t$'] = np.random.choice(np.arange(6,12,1), 16) #kN/m
    list_ben['Lt'] = np.random.choice(np.arange(1,4,1), 16) #m
    list_ben['Fp'] = np.random.choice(np.arange(6,12,10), 16) #kN
    list_ben['LFp'] = np.random.choice(np.arange(2,6,1), 16) #m
    list_ben['M'] = np.random.choice(np.arange(40,80,10), 16) #kN
    list_ben['L_M'] = np.random.choice(np.arange(1,5,1), 16) #m
    list_ben['Fr'] = np.random.choice(np.arange(6,12,10), 16) #kN
    list_ben['L_Fr0'] = np.random.choice(np.arange(3,5,1), 16) #m
    list_ben.to_csv("List_ben.csv")
else:
    list_ben = pd.read_csv("List_ben.csv", index_col=0)

process_bending = True
if process_bending:
    info= {}
    for ind in list_ben.index:
        nombre = list_ben.loc[ind, 'Nombre']
        print("Solving diagrams for {}".format(nombre))
        out = solve_beam(*list(list_ben.loc[ind, '$F_t$':].values))
        info.update({nombre: out})
        
