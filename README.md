# Semantic_Data_Analysis

## Required order of operations:

1. Ensure you have the right transcribed data in the folder '/PILOT/DATA/GroupA' and '/PILOT/DATA/GroupB'
   Note: Alternately, if we are working with hand a subset of corrected data '/PILOT/DATA/Corrected/GroupA' and '/PILOT/DATA/Corrected/GroupB'.
   Eventually, all the data in '/PILOT/DATA/GroupA' and '/PILOT/DATA/GroupB' will consist of fully hand corrected data.
   This note should be removed once this has been completed.

2. Run automatic collocations by running the shell script using the following command in command line:
   > `sh run_collocations.sh`
   
   Make sure you're pulling data from the right folders to run collocations on.
4. Once the collocations are extracted, make sure the hand corrections are done and sent to the right folders
5. Group the data by category by running the following command:
   > `sh run_group_data.sh`
   
   NOTE: before running the command, open the shell script and make sure the files you want to be grouped are grouped. Right now the grouping is being done only for hand corrected data in Group A
