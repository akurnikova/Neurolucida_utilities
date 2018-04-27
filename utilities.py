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

stack1 = 'RV4_L_align'
stack2 = 'RV4_R_align'
ET.register_namespace('', 'http://www.mbfbioscience.com/2007/neurolucida')
prefix = '{http://www.mbfbioscience.com/2007/neurolucida}'

def merge_stacks(stack1,stack2):
    ## Code to combine across files:
        
    xmlfile1 = '/home/asya/Documents/Neurolucida_utilities/%s.xml' % stack1
    tree1 = ET.parse(xmlfile1)
    root1 = tree1.getroot()
    
    xmlfile2 = '/home/asya/Documents/Neurolucida_utilities/%s.xml' % stack2
    tree2 = ET.parse(xmlfile2)
    root2 = tree2.getroot()
    
 #   ET.register_namespace('', prefix)
    
    numsections_1 = len(list(root1[1]))-1
    
    ## process list of sections
    for item in root2[1].findall(prefix+'section'):
        old_val = item.get('sid')
        new_section_number = int(old_val[1:])+numsections_1
        item.set('sid','S'+ str(new_section_number))
        item.set('name','Section '+ str(new_section_number))
        root1[1].append(item)
        
    ## process contours
    for item in root2.findall(prefix+'contour'):
        for pt in item.findall(prefix+'point'):
            old_val = pt.get('sid')
            new_section_number = int(old_val[1:])+numsections_1
            pt.set('sid','S'+ str(new_section_number))
        root1.append(item)
    
    ## process markers
    for item in root2.findall(prefix+'marker'):
        for pt in item.findall(prefix+'point'):
            old_val = pt.get('sid')
            new_section_number = int(old_val[1:])+numsections_1
            pt.set('sid','S'+ str(new_section_number))
        root1.append(item)
    
    ## process dendrites
    for item in root2.findall(prefix+'tree'):
        for pt in item.findall(prefix+'point'):
            old_val = pt.get('sid')
            new_section_number = int(old_val[1:])+numsections_1
            pt.set('sid','S'+ str(new_section_number))
        root1.append(item)
        
    tree1.write(stack1+'+'+stack2+'.xml')
    resort_sections(stack1+'+'+stack2)


def resort_sections(stack):
    xmlfile = '/home/asya/Documents/Neurolucida_utilities/%s.xml' % stack
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    for child in root[1]:
        str_val = child.get('top')
        if str_val == None:
            save_start_line = child
            root[1].remove(child)
            
    def sortchildrenby(parent, attr):
        parent[:] = sorted(parent, key=lambda child: int(child.get(attr)))
    sortchildrenby(root[1], 'top')
    map_new_section_dict = {}
    for i,item in enumerate(root[1].findall(prefix+'section')):
        map_new_section_dict[item.get('sid')] = 'S'+str(i+1)
    
    ## process list of sections
    for item in root[1].findall(prefix+'section'):
        new_section_id = map_new_section_dict[item.get('sid')]
        item.set('sid',new_section_id)
    root[1].append(save_start_line)
    ## process contours
    for item in root.findall(prefix+'contour'):
        for pt in item.findall(prefix+'point'):
            new_section_id = map_new_section_dict[pt.get('sid')]
            pt.set('sid',new_section_id)
    
    ## process markers
    for item in root.findall(prefix+'marker'):
        for pt in item.findall(prefix+'point'):
            new_section_id = map_new_section_dict[pt.get('sid')]
            pt.set('sid',new_section_id)
            
    ## process dendrites
    for item in root.findall(prefix+'dendrite'):
        for pt in item.findall(prefix+'point'):
            new_section_id = map_new_section_dict[pt.get('sid')]
            pt.set('sid',new_section_id)
    tree.write(stack+'_resorted.xml')
    with open(stack+'_resorted.xml', 'a') as f:
        f.write("\n\n")


## Code to correct z-depth
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
    
merge_stacks(stack1,stack2)
fix_depth(stack1+'+'+stack2+'_resorted')
