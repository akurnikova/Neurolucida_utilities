# Neurolucida_utilities

Functions to correct issues with neurolucida (mbf)  xml files

To merge 2 neurolucida files (while preserving section assignment) run:

  python merge_NL_stacks.py stack1 stack2
  
  In Windows, need to open the command prompt and run the full path:
  
  1) open 'cmd'
  2) cd C:\Users\dklab\Desktop\Neurolucida_utilities
  3) C:\Python27\python.exe C:\Users\dklab\Desktop\Neurolucida_utilities\merge_NL_stacks.py stack1 stack2

for example:
C:\Python27\python.exe C:\Users\dklab\Desktop\Neurolucida_utilities\merge_NL_stacks.py RV4_align_R_2 RV4_L_align

  
To fix depths of structures - aka assign all to value of section 'top' run:

  python fix_NL_depths.py stack

  In Windows, need to run the full path:
  
  1) open 'cmd'
  2) cd C:\Users\dklab\Desktop\Neurolucida_utilities
  3) C:\Python27\python.exe C:\Users\dklab\Desktop\Neurolucida_utilities\fix_NL_depths.py stack
  
  Stacy 04/2018