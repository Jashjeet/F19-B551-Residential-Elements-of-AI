#!/usr/local/bin/python3
# CSCI B551 Fall 2019
#
# Authors: DEVANSH JAIN - devajain
#           SANYAM RAJPAL - srajpal
#           JASHJEET SINGH MADAN - jsmadan
#
# based on skeleton code by D. Crandall, 11/2019
#
# ./break_code.py : attack encryption
#


import random
import math
import copy 
import sys
import encode

# put your code here!
def generate_random_decipher_key():
    key=""
    for i in random.sample(range(ord('a'),ord('z')+1),26):
        key+=chr(i)
    dk={}
    
    start=ord('a')
    for i in key:
        dk[chr(start)]=i
        start+=1
    
    return dk


def generate_sequential_decipher_key():
    
#    key=""
    dk={}
    
    for i in range(ord('a'),ord('z')+1):
#        key+=chr(i)
        dk[chr(i)]=chr(i)
    return dk
        



def switch_two_letters(dictionary):   
    while True:
        num1=random.randint(1,26)+96
        num2=random.randint(1,26)+96
        if num1!=num2:
            dictionary[chr(num1)],dictionary[chr(num2)]=dictionary[chr(num2)],dictionary[chr(num1)]
            return (dictionary)

    
        
    
def coin_toss(prob):
    num=random.random()
    
    if num>=prob:
        return False
    
    return True
    


def decode(string,decipher):
    decrypted=''
    for i in string:
        if i !=' ':
            decrypted+=decipher[i]
        else:
            decrypted+=' '
    
    return(decrypted)
        
    

    

    
def rearrange(string,re):
    n=len(re)
    temp=''

    for j in range(0,len(string),n):
        for k in re:
            temp+=string[k+j]

    return(temp)
    
    



def calculate_probability(string,tp):
    s=0
    for i in range(len(string)-1):
        first=string[i]
        second=string[i+1]
        
        key=first+second
        
        if key in tp:
            s+=math.log(tp[key])
        
        
        
    return(s)
        
    pass
    
      







def break_code(string, corpus):
    spaces_to_append=len(string)%4
    spaces=' '*(4-spaces_to_append)
    string+=spaces
    tp={}
    len_corpus=len(corpus)
    for i in range(len(corpus)-1):
        prev=corpus[i]
        nextt=corpus[i+1]
        
        if prev+nextt not in tp:
            tp[prev+nextt]=1
        else:
            tp[prev+nextt]+=1


        
    

    count={}
    for i in range(len(string)-1):
        prev=string[i]
        nextt=string[i+1]
        
        if prev+nextt not in count:
            count[prev+nextt]=1
        else:
            count[prev+nextt]+=1
            




    decipher=generate_random_decipher_key()
#    decipher=generate_sequential_decipher_key()
    
    
    
    
    best_score=0
    best_answer=''
    guess=[0,1,2,3]
    random.shuffle(guess)
    best_guess=guess
    best_decipher=decipher
    for i in range(1000000):    
   
        
        
        
          
        decoded_text=decode(string,decipher)
        rearranged_text=rearrange(decoded_text,guess)
        PD=calculate_probability(rearranged_text,tp)
        if PD>best_score:
            best_score=PD
            best_answer=copy.deepcopy(rearranged_text)
            best_decipher=copy.deepcopy(decipher)
            best_guess=copy.deepcopy(guess)
            
        new_decipher=switch_two_letters(decipher)
        new_guess=copy.deepcopy(guess)


        
        
        
        new_decipher=switch_two_letters(new_decipher)
#        new_decipher=generate_random_decipher_key()
        random.shuffle(new_guess)
        
      
     
        decoded_text_new=decode(string,new_decipher)
        rearranged_text_new=rearrange(decoded_text_new,new_guess)
        PDdash=calculate_probability(rearranged_text_new,tp)

        

        
        if PDdash>best_score:
            best_score=PDdash
            best_answer=copy.deepcopy(rearranged_text_new)
            best_decipher=copy.deepcopy(new_decipher)
            best_guess=copy.deepcopy(new_guess)



        
        if PDdash>PD:
            decipher=copy.deepcopy(new_decipher)
            guess=copy.deepcopy(new_guess)

            
            
        elif coin_toss(math.exp(PDdash-PD)):
            decipher=copy.deepcopy(new_decipher)
            guess=copy.deepcopy(new_guess)




    

#        if (i%1000==0):
#            print(i)
#            print('best_answer',best_answer)
#            print('rearranged_text',rearranged_text)
#            print('rearranged_text_new',rearranged_text_new)
#            print('iteration ',i)
#            print('best_decipher ',best_decipher)  
#            print('decipher',decipher)
#            print('new_decipher',new_decipher)
#            print('best_score ',best_score)
#            print('best_guess ',best_guess)
#            print('PD ',PD)
#            print('PDdash ',PDdash)
#            print('PDdash2 ',PDdash2)



    return best_answer


if __name__== "__main__":
    if(len(sys.argv) != 4):
        raise Exception("usage: ./break_code.py coded-file corpus output-file")

    encoded = encode.read_clean_file(sys.argv[1])
    corpus = encode.read_clean_file(sys.argv[2])
    decoded = break_code(encoded, corpus)

    
    with open(sys.argv[3], "w") as file:
        print(decoded, file=file)
