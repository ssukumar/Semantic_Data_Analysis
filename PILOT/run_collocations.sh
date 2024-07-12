#!/bin/bash

python3.11 detect_collocations.py --input_folder "DATA/GroupA/transcriptions/" --output_folder "DATA/GroupA/transcriptions_collocations/"

python3.11 detect_collocations.py --input_folder "DATA/GroupB/transcriptions/" --output_folder "DATA/GroupB/transcriptions_collocations/"


# In Person Data 
# python3.11 detect_collocations.py --input_folder "DATA/In_person/GroupA/transcriptions/" --output_folder "DATA/In_person/GroupA/transcriptions_collocations/"

# python3.11 detect_collocations.py --input_folder "DATA/In_person/GroupB/transcriptions/" --output_folder "DATA/In_person/GroupB/transcriptions_collocations_gen/"
