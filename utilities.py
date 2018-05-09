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
stack = 'RV19'
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
            
    ## process trees
    for item in root.findall(prefix+'tree'):
        for pt in item.findall(prefix+'point'):
            new_section_id = map_new_section_dict[pt.get('sid')]
            pt.set('sid',new_section_id)
    tree.write(stack+'_resorted.xml')
    with open(stack+'_resorted.xml', 'a') as f:
        f.write("\n\n")


## Code to correct z-depth
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
        item.set('top',str(int(new_top)))
    tree.write(stack+'_corrected.xml')
    with open(stack+'_corrected.xml', 'a') as f:
        f.write("\n\n")
        
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
    for item in root.findall(prefix+'tree'):
            for pt in item.findall(prefix+'point'):
                sid = pt.get('sid')
                pt.set('z',"{0:.2f}".format(float(section_z_dict[sid])))    
    
    tree.write(stack+'_corrected.xml')
    with open(stack+'_corrected.xml', 'a') as f:
        f.write("\n\n")
    
#merge_stacks(stack1,stack2)
#fix_depth(stack1+'+'+stack2+'_resorted')
fix_section_tops(stack)
fix_depth(stack+'_corrected')