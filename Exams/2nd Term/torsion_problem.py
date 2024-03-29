#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 11:10:46 2021
Class method to solve any shaft torsion problem 
@author: nikorose
"""
import pandas as pd
import numpy as np


class angle_twist:
    def __init__(self, series):
        self.student = series['Nombre']
        self.sections = series['L_0':]
        self.num_sections = 3 #Number of sections to calculate
        

    def add_sections(self):
        """
        Here we added the converted modulus G, later it is stored in a df

        Returns
        -------
        Dataframe with the completed sections

        """
        self.complete_secs = {}
        num=0
        for it in range(self.num_sections):
            if self.sections['Mat_{}'.format(it)] == "Steel 308":
                G = 77.1e9
            elif self.sections['Mat_{}'.format(it)] == "Aluminum":
                G = 27e9
            elif self.sections['Mat_{}'.format(it)] == "Brass":
                G = 39e9
            else:
                AssertionError('Material {} is not included in the library'.format(self.sections['Mat_{}'.format(it)]))
            self.complete_secs.update({num: {'G': G, 
                                             'OD': self.sections['OD_{}'.format(it)]/1000,
                                             'ID': self.sections['ID_{}'.format(it)]/1000,
                                             'L': self.sections['OD_{}'.format(it)]/1000,
                                             'T': np.sum([self.sections['T_{}'.format(i)] for i in range(0, it+1)])}})
            num +=1
        self.complete_secs = pd.DataFrame(self.complete_secs).T
        return self.complete_secs
    
    def calc_angle_twist(self):
        """
        Calculate the angle of twist

        Returns
        -------
        TYPE
            Dataframe with the completed sections

        """
        if hasattr(self, r'complete_secs'):
            self.complete_secs['J'] = self.complete_secs.apply(lambda x: ((x.OD/2)**4-(x.ID/2)**4)*np.pi/2, axis=1)
            self.complete_secs['Angle'] = (self.complete_secs['T']*self.complete_secs['L'])/(self.complete_secs['G']*self.complete_secs['J'])
            return self.complete_secs
        
    def calc_complete_angle(self):
        """
        Completes the total angle of twist

        Returns
        -------
        TYPE
            Dataframe with the completed sections
        """
        if hasattr(self, r'complete_secs'):
            self.total_ang = self.complete_secs['Angle'].sum()
            return self.complete_secs
    def calc_max_stress(self):
        """
        Calculate the stresses on each section

        Returns
        -------
        TYPE
            Dataframe with the completed sections

        """
        if hasattr(self, r'complete_secs'):
            self.complete_secs['Stress'] = self.complete_secs.apply(lambda x: (x['T']*x['OD']/2)/x['J'], axis=1)
            return self.complete_secs
    def reindex(self):
        """
        

        Returns
        -------
        TYPE
            Dataframe with the completed sections
        """
        if hasattr(self, r'complete_secs'):
            index = pd.MultiIndex.from_product([[self.student], [self.total_ang], 
                                                list(range(self.num_sections))], 
                                               names=['Student', 'TotalTwist', 'Sections'])
            self.complete_secs.index = index
            return self.complete_secs

read_students = pd.read_csv("List_tor.csv", index_col=0)
res_list = []
for student in read_students.index:
    case = read_students.loc[student,:]
    shaft_obj = angle_twist(case)
    shaft_obj.add_sections()
    shaft_obj.calc_angle_twist()
    shaft_obj.calc_complete_angle()
    shaft_obj.calc_max_stress()
    shaft_obj.reindex()
    res_list.append(shaft_obj.complete_secs)

res_list_df = pd.concat(res_list)



    
        

    