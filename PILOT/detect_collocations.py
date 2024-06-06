import os
import pandas as pd
import argparse
from nltk.corpus import webtext, wordnet, genesis
from nltk.corpus import brown, reuters
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk.collocations import QuadgramCollocationFinder
import pdb


def identify_ngrams(word_list):
    print("word list")
    word_list = [word_in.lower() for word_in in word_list]
    print(word_list)
    
    # Load the Brown Corpus (must be downloaded already)
    # other corpuses to try: https://www.nltk.org/book/ch02.html
    brown_words = brown.words()

    # Create a BigramCollocationFinder object with the Brown Corpus
    finder = BigramCollocationFinder.from_words(webtext.words())
    print(finder)

    # Filter bigrams to only include those present in the given word list
    finder.apply_word_filter(lambda w: w.lower() not in word_list)
    
    # the threshold for this is very arbitrary, maybe we can do some cross-validation to identify threshold
    # finder.apply_freq_filter(5)

    # Get the frequency ranks of bigrams
    # Can also use nbest() funciton to use other parameters to filter the n-gram
    bigram_freq_ranking = sorted(finder.ngram_fd.keys(), key=lambda item: item[1], reverse=True)
    
    # Convert from list of tuples to list of strings for easy comparison
    bigram_list = [' '.join(bg) for bg in bigram_freq_ranking]

    print(bigram_freq_ranking)
    
    # Obtain trigrams in descending order of frequency of occurence 
    tcf = TrigramCollocationFinder.from_words(webtext.words())
    tcf.apply_word_filter(lambda w: w.lower() not in word_list)
    # tcf.apply_freq_filter(3)
    trigram_freq_ranking = sorted(tcf.ngram_fd.keys(), key=lambda item: item[1], reverse=True)
    trigram_list = [' '.join(tg) for tg in trigram_freq_ranking]
    print(trigram_list)
    
    # Obtain quadgrams in descending order of frequency of occurence 
    qcf = QuadgramCollocationFinder.from_words(webtext.words())
    qcf.apply_word_filter(lambda w: w.lower() not in word_list)
    # qcf.apply_freq_filter(1)
    quadgram_freq_ranking = sorted(qcf.ngram_fd.keys(), key=lambda item: item[1], reverse=True)
    quadgram_list = [' '.join(qg) for qg in quadgram_freq_ranking]
    print(quadgram_list)
    
    
    # pdb.set_trace()
    return bigram_list, trigram_list, quadgram_list


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def detect_collocations (input_folder, output_folder):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else: 
        output_files = os.listdir(output_folder)
    
    # not redo collocations if already done
    intersect_ip_op = intersection(os.listdir(input_folder), os.listdir(output_folder))
    
    print(intersect_ip_op)
    
    for word_list_path in os.listdir(input_folder):
        
        if word_list_path.endswith('.xlsx') and not word_list_path.startswith('.') and word_list_path not in intersect_ip_op:
        # read response word list from initial transcription 
            word_df = pd.read_excel(os.path.join(input_folder, word_list_path), header = 0)
            word_df = word_df.iloc[:, :4]
            word_list = word_df["Word"].tolist()
            
            # Check if list is empty
            if word_list: 
                # create list to append new compounded data 
                new_rows =[]
    
                # Identify top bigrams, trigrams and quadgrams from the list 
                bigram_list, trigram_list, quadgram_list = identify_ngrams(word_list)
    
                # Iterate through all words to id collocations
                for index, row in word_df.iterrows():
                    word = row["Word"]
                    start_time = row["Start_time"]
                    end_time = row["End_time"]
                    confidence = row["Confidence"]
            
                    if not (bigram_list or trigram_list or quadgram_list):
                         new_rows.append([word, start_time, end_time, confidence])
            
                    elif len(new_rows)>0 and new_rows[-1][0].count(' ') < 3:
                        if start_time == new_rows[-1][2]:
                
                            # Create compound word to check against bigram 
                            check_wd = new_rows[-1][0] + " "+word
                            spaces_ct = check_wd.count(' ')
                
                            # Maybe this if statement can be made more efficient
                            if (spaces_ct == 1 and check_wd in bigram_list) or  (spaces_ct == 2 and check_wd in trigram_list) or (spaces_ct == 3 and check_wd in quadgram_list):
                                new_rows[-1][0]+= " "+word
                                new_rows[-1][2] = end_time
                            else:
                                new_rows.append([word, start_time, end_time, confidence])
                        else:
                            new_rows.append([word, start_time, end_time, confidence])
                    else:
                        new_rows.append([word, start_time, end_time, confidence])

                df = pd.DataFrame(new_rows)

                # Save the dataframe to excel
                # filename_xl = word_list_path[len(prefix):]
                output_path = os.path.join(output_folder, f"{os.path.splitext(word_list_path)[0]}.xlsx")
                df.to_excel(output_path, index=False, header = ["Word", "Start_time", "End_time", "Confidence"])

                print(f"Transcription for {word_list_path} saved in {output_path}")
            else:
                continue
            
        elif word_list_path.endswith('.csv'):
            os.rename(os.path.join(input_folder, word_list_path),os.path.join(output_folder, word_list_path))
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Execute Collocation Finder')
    parser.add_argument('--input_folder', type=str,  help='Path where transcripted word files are stored')
    parser.add_argument('--output_folder', type=str,  help='Path for output word file is to be stored')
    args = parser.parse_args()
    detect_collocations(args.input_folder, args.output_folder)
    
