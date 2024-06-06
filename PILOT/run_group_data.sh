#!/bin/bash

# python3.11 group_data.py --input_folder "DATA/GroupA/transcriptions_collocations/" --output_folder "DATA/Grouped"
# python3.11 group_data.py --input_folder "DATA/GroupA/transcriptions_collocations_gen/" --output_folder "DATA/Grouped_Improved"
# python3.11 group_data.py --input_folder "DATA/GroupB/transcriptions_collocations/" --output_folder "DATA/Grouped"
# python3.11 group_data.py --input_folder "DATA/GroupB/transcriptions_collocations_gen/" --output_folder "DATA/Grouped"


# Test

# echo "ONLY RUNNING THE CORRECTED TEST"
#
# python3.11 group_data.py --input_folder "DATA/Test/GroupB/transcriptions_corrected/" --output_folder "DATA/Test/Grouped_corrected"

# echo "ONLY RUNNING THE UNCORRECTED TEST"
#
# python3.11 group_data.py --input_folder "DATA/Test/GroupB/transcriptions_uncorrected/" --output_folder "DATA/Test/Grouped_uncorrected"



# echo "ONLY RUNNING THE CORRECTED TEST"
#
# python3.11 group_data.py --input_folder "DATA/Test/GroupA/transcriptions_corrected/" --output_folder "DATA/Test/Grouped_corrected"

# echo "ONLY RUNNING THE UNCORRECTED TEST"
#
# python3.11 group_data.py --input_folder "DATA/Test/GroupA/transcriptions_uncorrected/" --output_folder "DATA/Test/Grouped_uncorrected"/


# In person data grouping

# python3.11 group_data.py --input_folder "DATA/In_person/GroupA/transcriptions_collocations/" --output_folder "DATA/In_person/Grouped"
# python3.11 group_data.py --input_folder "DATA/In_person/GroupB/transcriptions_collocations/" --output_folder "DATA/In_person/Grouped"


# hand corrected data grouping

# python3.11 group_data.py --input_folder "DATA/Corrected/GroupA/transcriptions_corrected/" --output_folder "DATA/Corrected/Grouped_corrected"

python3.11 group_data.py --input_folder "DATA/Corrected/GroupB/transcriptions_corrected/" --output_folder "DATA/Corrected/Grouped_corrected"


# python3.11 group_data.py --input_folder "DATA/Corrected/GroupA/transcriptions_Uncorrected/" --output_folder "DATA/Corrected/Grouped_uncorrected"