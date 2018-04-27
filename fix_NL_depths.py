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


ET.register_namespace('', 'http://www.mbfbioscience.com/2007/neurolucida')
prefix = '{http://www.mbfbioscience.com/2007/neurolucida}'


def fix_depth(stack):
    xmlfile = '/home/asya/Documents/Neurolucida_utilities/%s.xml' % stack
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    numsections_1 = len(list(root[1]))-1
    
    section_name_dict = {}
    section_z_dict = {}
    for item in root[1].findall(prefix+'section'):
        section_name_dict[item.get('name')] = item.get('sid')
        section_z_dict[item.get('sid')] = item.get('top')
        
    ## process contours
    for item in root.findall(prefix+'contour'):
            for pt in item.findall(prefix+'point'):
                sid = pt.get('sid')
                pt.set('z',"{0:.2f}".format(float(section_z_dict[sid])))    
                
    ## process markers
    for item in root.findall(prefix+'marker'):
            for pt in item.findall(prefix+'point'):
                sid = pt.get('sid')
                pt.set('z',"{0:.2f}".format(float(section_z_dict[sid])))
    
    ## process dendrites
    for item in root.findall(prefix+'dendrite'):
            for pt in item.findall(prefix+'point'):
                sid = pt.get('sid')
                pt.set('z',"{0:.2f}".format(float(section_z_dict[sid])))    
    
    tree.write(stack+'_corrected.xml')
    with open(stack+'_corrected.xml', 'a') as f:
        f.write("\n\n")
    
def main(argv):
   a,stack = sys.argv

   print 'Input stack is ', stack
   
   fix_depth(stack)
   
   print 'merged file saved as ', stack+'_corrected.xml'

if __name__ == "__main__":
   main(sys.argv[1:])

