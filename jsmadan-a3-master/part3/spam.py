# Authors: DEVANSH JAIN - devajain
#           SANYAM RAJPAL - srajpal
#           JASHJEET SINGH MADAN - jsmadan

import numpy as np
from pandas import DataFrame
import re
from collections import Counter
import csv
import os
import sys
def count_word_frequency(email_list):
    allwords=[]
    for i in range(len(email_list)):
        for j in range( len(email_list[i][0])):
            allwords.append(email_list[i][0][j])
            
    counts  = Counter (allwords)
    counts = Counter (th for th in counts.elements() if counts[th] >= 0)
    return(counts)

def split_to_words(email_list):
    stop_words=["is", "a", "an", "the", "to", "for", "at", "of" ]
    for i in range(len(email_list)):
        email_list[i][0] = (email_list[i][0].split())
        email_list[i][0] = [word for word in email_list[i][0] if word not in stop_words]
    return(email_list)

def read_mail_body(file_location):
    for root, directory, files in os.walk(file_location):
        for file in files:
            lines = []
            file = os.path.join(root, file)
            with open (file, "r", encoding="latin1") as f:
                for line in f:
                    line= (line.lower()).replace('\n',' ')
                    lines.append(line)
            f.close()
            email_body= "\n".join(lines)
            yield file, email_body
                        
def read_email(file_location, email_type):
    emails= []
    files= []
    for filename, email_body in read_mail_body(file_location):
        emails.append({'email_body': email_body, 'type': email_type})
        files.append(filename)
    return(DataFrame(emails, files), files)

def priori_probabilities( word_count , word_prob ) :
    normal = sum( word_count.values( ) )
    for word in word_count :
        word_prob.update( { word : np.exp( word_count[ word ] / normal ) } )


if __name__== "__main__":
    if(len(sys.argv) != 4):
        raise Exception("usage: ./break_code.py coded-file corpus output-file")

    
    email_dictionary = DataFrame({'email_body': [], 'type': []})
    filenames , files, test_result_file, ground = [], [], [], []
    email_spam = split_to_words( ( email_dictionary.append(read_email(sys.argv[1]+'/spam', 'spam')[0]) ).values.tolist( ) )
    email_notspam = split_to_words(( email_dictionary.append(read_email(sys.argv[1]+'/notspam', 'notspam')[0])).values.tolist( ) )
    
    email_test_0, filenames = (read_email(sys.argv[2], 'test'))
    email_test_0 = email_dictionary.append(email_test_0)
    email_test = split_to_words((email_test_0).values.tolist( ) )
    
    counts , spam_word_prob , notspam_word_prob = { } , { } , { }
    
    spam_word_count = count_word_frequency(email_spam)
    notspam_word_count = count_word_frequency(email_notspam )
    priori_probabilities( spam_word_count , spam_word_prob )
    priori_probabilities( notspam_word_count , notspam_word_prob )
    
    prob_spam = len( email_spam ) / ( len( email_spam ) + len( email_notspam ) )
    prob_notspam = 1.0 - prob_spam
    
    spam_prob, notspam_prob = [ ], [ ]
    
    for elem in email_test :
        prob_s = 1.0
        prob_ns = 1.0
        for word in elem[ 0 ] :
            if( word in spam_word_prob ) :
                prob_s *= spam_word_prob[ word ]
            else: 
                prob_s *= 0.85
                
            if( word in notspam_word_prob ) :
                prob_ns *= notspam_word_prob[ word ]
            else:
                prob_ns *= 0.85
        prob_s *= prob_spam
        prob_ns *= prob_notspam
        spam_prob.append( prob_s / max( ( prob_s + prob_ns ) , 1.0e-6 ) )
        notspam_prob.append( prob_ns / max( ( prob_s + prob_ns ) , 1.0e-6 ) )
    
    for filename in filenames:
        path, file = os.path.split(filename)
        files.append(file)
        
    with open(sys.argv[3], "a" ) as f:
        writer=csv.writer(f)
        for i in range( len( spam_prob ) ) :
            if spam_prob[ i ] > 0.5 :
                temp = [str(files[ i ] + " spam")]
                writer.writerow( temp)
                test_result_file.append([files[ i ] , "spam"])
            
            else :
                temp = [str(files[ i ] + " notspam")]
                writer.writerow( temp )
                test_result_file.append([files[ i ] , "notspam"])
    
    with open("test-groundtruth.txt", "r") as f:
        [ground.append(line) for line in f]
    
    groundtest = [i.split() for i in ground]
    count= 0 
    
    for i in groundtest:
        for j in test_result_file:
            if i[0] == j[0]:
                if i[1] == j[1]:            
                    count += 1
    print("Accuracy: " , ((count/len(groundtest))*100))
