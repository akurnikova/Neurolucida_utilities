#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Functions to edit neurolucida xml files:
    
merge_stacks(stack1,stack2):
        Merge two stacks while preserving section assignment
        
fix_depth(stack)
        Fixes section depths
Created on Tue Apr 24 14:54:29 2018

@author: asya
"""
import xml.etree.ElementTree as ET
global prefix
import sys
import numpy as np


ET.register_namespace('', 'http://www.mbfbioscience.com/2007/neurolucida')
prefix = '{http://www.mbfbioscience.com/2007/neurolucida}'

def fix_section_tops(stack):
## recalculates stack 'tops' based on section thicknesses
    xmlfile = '/home/asya/Documents/Neurolucida_utilities/%s.xml' % stack
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    section_sid_list = list()
    section_z_list = list()
    section_thickness_list = list()
    for item in root[1].findall(prefix+'section'):
        section_sid_list.append(item.get('sid'))
        section_z_list.append(float(item.get('top')))
        section_thickness_list.append(float(item.get('cutthickness')))
    
    section_z = np.asarray(section_z_list)
    section_thicknesses = np.asarray(section_thickness_list)
    
    idx_center = np.where(section_z ==0)[0][0]
    
    for i in range(idx_center+1,len(section_thicknesses)):
        section_z[i] = section_z[i-1]+section_thicknesses[i]
    for i in range(idx_center-1,-1,-1):
        section_z[i] = section_z[i+1]-section_thicknesses[i]
    
    dict_z_to_sid = dict(zip(section_sid_list, section_z))
    ## process list of sections
    for item in root[1].findall(prefix+'section'):
        new_top = dict_z_to_sid[item.get('sid')]
        item.set('top',new_top)
    tree.write(stack+'_top_corrected.xml')
    with open(stack+'_top_corrected.xml', 'a') as f:
        f.write("\n\n")
    
def main(argv):
   a,stack = sys.argv

   print 'Input stack is ', stack
   
   fix_section_tops(stack)
   
   print 'merged file saved as ', stack+'_corrected.xml'

if __name__ == "__main__":
   main(sys.argv[1:])

