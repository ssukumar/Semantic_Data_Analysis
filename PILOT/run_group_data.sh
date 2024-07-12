#!/bin/bash

# python3.11 group_data.py --input_folder "DATA/GroupA/transcriptions_collocations/" --output_folder "DATA/Grouped"
# python3.11 group_data.py --input_folder "DATA/GroupA/transcriptions_collocations_gen/" --output_folder "DATA/Grouped_Improved"
# python3.11 group_data.py --input_folder "DATA/GroupB/transcriptions_collocations/" --output_folder "DATA/Grouped"
# python3.11 group_data.py --input_folder "DATA/GroupB/transcriptions_collocations_gen/" --output_folder "DATA/Grouped"


# hand corrected data grouping

python3.11 group_data.py --input_folder "DATA/Corrected/GroupA/transcriptions_corrected/" --output_folder "DATA/Corrected/Grouped_corrected"

# python3.11 group_data.py --input_folder "DATA/Corrected/GroupB/transcriptions_corrected/" --output_folder "DATA/Corrected/Grouped_corrected"


