# Neurolucida_utilities
Functions to correct issues with neurolucida (mbf)  xml files

To merge 2 neurolucida files (while preserving section assignment) run:
  python merge_NL_stacks.py stack1 stack2
  
To fix depths of structures - aka assign all to value of section 'top' run:
  python fix_NL_depths.py stack
