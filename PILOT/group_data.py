import os
import pandas as pd
import argparse

def identify_category(metadata_csv, trial_str):
    
    metadata = pd.read_csv(metadata_csv)
    
    # keeping only trial relevant rols
    if 'Mic_cattestresgis.clip' in metadata.columns:
        metadata= metadata[ metadata['Mic_cattestresgis.clip'].str.len() > 0 ]
    
    for index, row in metadata.iterrows():
        
        if trial_str in row['Mic_cattestresgis.clip']:
            return row["items"]
            
def identify_category2(metadata_csv, trial_num):
    
    metadata = pd.read_csv(metadata_csv)
    
    # keeping only trial relevant rols
    metadata= metadata[ metadata['items'].str.len() > 0 ]
    
    for index, row in metadata.iterrows():
        
        if trial_num == row['trials.thisTrialN']:
            return row["items"]
    
    
def find_metadata_file( metadata_dir, subj_id):
    
    for file in os.listdir(metadata_dir):
        
        if file.endswith('.csv') and subj_id in  file:
            return file
            
def convert_txt_files(output_folder):

        # Convert to txt files:
    for filename in os.listdir(output_folder):
        if filename.endswith('.csv') and not filename.startswith('.'):
            trial_file_df = pd.read_csv(os.path.join(output_folder, filename), header = 0, encoding = "utf-8")
            output_txt_file= os.path.join(output_folder, filename[:-4] + '.txt')
            print(output_txt_file)
            
            
            
            with open(output_txt_file, 'w+') as f:
                trial_file_string = trial_file_df.to_string(index = False, header =  ['id', 'entry', 'timestamp', 'endtimestamp', 'confidence'])
                f.write(trial_file_string)


def group_data_by_category(input_folder, output_folder, metadata_dir=None, data_in_person = False):
    
    if metadata_dir is None:
        metadata_dir = input_folder
        
    for filename in os.listdir(input_folder):
        print(f"filename : {filename}\n")
        flag_ = True
        if "trials" in filename:
        
            subj = filename.split('_')[0]
            
            print(f"Subject: {subj}\n")
            metadata_subj = find_metadata_file(input_folder, subj)
            
            if metadata_subj is not None:
                
                
                trial_str = filename[filename.find('trials')+ len('trials')+1:(filename.find('trials')+ len('trials')+3)]
                
                
                try:
                    int(trial_str)
                except ValueError:
                    flag_ = False
                    trial_str = filename[filename.find('trials')+ len('trials')+1:(filename.find('trials')+ len('trials')+2)]
                    
                
                print(f"Subject identified: {subj}; trial_string: {trial_str}; metadata_subj : {metadata_subj}")
                
                # if data_in_person == False:
#                     cat = identify_category(os.path.join(metadata_dir, metadata_subj), trial_str)
#                 else:
                
                cat = identify_category2(os.path.join(metadata_dir, metadata_subj), int(trial_str))
                if cat == 'PLACES TO STAY':
                    cat = 'ACCOMODATIONS'
                output_file = os.path.join(output_folder, cat + "_outputs.csv")
                # output_txt_file = os.path.join(output_folder,  cat + "_outputs.txt")
                trial_file_df = pd.read_excel(os.path.join(input_folder, filename), header = 0)
                print(trial_file_df)
                trial_file_df.insert(0, "subj_id", subj)
                print(trial_file_df)
                if not os.path.exists(output_file):
                    trial_file_df.to_csv(output_file, index =False, sep='\t')

                else:
                    output_df = pd.read_csv(output_file, header = 0, sep = '\t')
                    print("NEED TO ADD A CONDITION HERE FOR EMPTY DATAFRAME \n\n")
                    
                    if not any(output_df['subj_id'].isin([subj])):
                        print(trial_file_df.dtypes)
                        trial_file_df.to_csv(output_file, mode = 'a', index =False,header = False, sep='\t')
            

            
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Execute Data Grouping')
    parser.add_argument('--input_folder', type=str,  help='Path where final transcribed word files are stored')
    parser.add_argument('--output_folder', type=str,  help='Path for output word file is to be stored')
    args = parser.parse_args()
    group_data_by_category(args.input_folder, args.output_folder)
    
    # convert_txt_files(args.output_folder)