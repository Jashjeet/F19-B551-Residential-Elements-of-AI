###################################
# CS B551 Fall 2019, Assignment #3
#
# Authors: DEVANSH JAIN - devajain
#           SANYAM RAJPAL - srajpal
#           JASHJEET SINGH MADAN - jsmadan
#
# (Based on skeleton code by D. Crandall)
#

import random
import math
from collections import Counter

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    
    def __init__( self ) :
        # transition probability
        self.dict_tp = { }
        # emission probability
        self.dict_ep = { }
        # dictionary of word and pos
        self.dict_pos = { }
        # dictionary of word, pos and probability
        self.dict_bay_prob = { }
        # dictionary of word and pos , probability
        self.dict_rev_pos = { }
        # initiail probability
        self.init_prob = { }
        # pos count in training data
        self.pos_count = { }
        # word count in training data
        self.word_count = { }
        
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            post_prob = 0.0
            for i in range( len( sentence ) ) :
                if ( sentence[ i ] , label[ i ] ) in self.dict_ep :
                    t = self.dict_ep[ ( sentence[ i ] , label[ i ] ) ]
                    post_prob += math.log( t )
                else :
                    post_prob += math.log( 1e-24 )
            return post_prob
        
        elif model == "Complex":
            post_prob = 0.0

            for i in range( len( sentence ) ) :
                if ( sentence[ i ] , label[ i ] ) in self.dict_ep :
                    t = self.pos_count[ label[ i ] ] * self.dict_ep[ ( sentence[ i ] , label[ i ] ) ]
                    post_prob += math.log( t )
                else :
                    post_prob += math.log( 1e-24 )
                    
            prev_pos = label[ 0 ]
            for i in range( 1 , len( label ) ) :
                t = self.dict_tp[ ( prev_pos , label[ i ] ) ]
                post_prob += math.log( t )
                prev_pos = label[ i ]        
            return post_prob
            
        elif model == "HMM":
            post_prob = 0.0
            for i in range( len( sentence ) ) :
                if ( sentence[ i ] , label[ i ] ) in self.dict_ep :
                    t = self.dict_ep[ ( sentence[ i ] , label[ i ] ) ]
                    post_prob += math.log( t )
                else :
                    post_prob += math.log( 1e-24 )
            
            prev_pos = label[ 0 ]
            for i in range( 1 , len( label ) ) :
                t = self.dict_tp[ ( prev_pos , label[ i ] ) ]
                post_prob += math.log( t )
                prev_pos = label[ i ]
            
            return post_prob
            
        else:
            print("Unknown algo!")
        
    # Do the training!
    #
    def train(self, data):
        self.dict_pos = {'adj' : [], 
               'adv' : [], 
               'adp' : [], 
               'conj' : [], 
               'det' : [], 
               'noun' : [], 
               'num' : [], 
               'pron' : [], 
               'prt' : [], 
               'verb' : [], 
               'x' : [], 
               '.' : []}
        self.init_prob = {'adj' : 0, 
               'adv' : 0,
               'adp' : 0,
               'conj' : 0,
               'det' : 0,
               'noun' : 0,
               'num' : 0,
               'pron' : 0,
               'prt' : 0,
               'verb' : 0,
               'x' : 0,
               '.' : 0}
        self.dict_tp = { }

        self.pos_count = {'adj' : 0, 
               'adv' : 0,
               'adp' : 0,
               'conj' : 0,
               'det' : 0,
               'noun' : 0,
               'num' : 0,
               'pron' : 0,
               'prt' : 0,
               'verb' : 0,
               'x' : 0,
               '.' : 0}

        count = 0
        
        for elem in data :
            for pos in elem[ 1 ] :
                self.pos_count[ pos ] += 1
                count += 1
            for word in elem[ 0 ] :
                if word in self.word_count :
                    self.word_count[ word ] += 1
                else :
                    self.word_count[ word ] = 1
        
        for pos in self.pos_count :
            self.pos_count[ pos ] /= count
        
        for word in self.word_count :
            self.word_count[ word ] /= count
        
        for elem in data :
            if len( elem[ 1 ] ) > 1 :
                for i in range( len( elem[ 1 ] ) - 1 ) :
                    prev = elem[ 1 ][ i ]
                    nextt = elem[ 1 ][ i + 1 ]
                    self.init_prob[ prev ] += 1
                    if ( prev , nextt ) not in self.dict_tp:
                        self.dict_tp.update( { ( prev , nextt ) : 1 } )
                    else:
                        self.dict_tp[ ( prev , nextt ) ] += 1
                    self.dict_pos[ elem[ 1 ][ i ] ].append( elem[ 0 ][ i ] )
                self.dict_pos[ elem[ 1 ][ i + 1 ] ].append( elem[ 0 ][ i + 1 ] )
        
        normal = sum( self.init_prob.values( ) )
        
        for elem in self.init_prob.keys( ) :
            self.init_prob[ elem ] /= normal
        
        for elem in data :
            for i in range( len( elem[ 0 ] ) ) :
                if elem[ 0 ][ i ] not in self.dict_rev_pos :    
                    self.dict_rev_pos[ elem[ 0 ][ i ] ] = [ elem[ 1 ][ i ] ]
                else :
                    self.dict_rev_pos[ elem[ 0 ][ i ] ].append( elem[ 1 ][ i ] )
            
        summ = sum( self.dict_tp.values( ) )
        for i in self.dict_tp:
            self.dict_tp[ i ] = ( float( self.dict_tp[ i ] / summ ) )
        self.dict_ep = { }
        for pos, words in self.dict_pos.items():
            counts = Counter(words)
            counts = Counter (th for th in counts.elements())
        
        for pos, words in self.dict_pos.items():
            normal = 0
            counts= Counter(words)
            counts = Counter (th for th in counts.elements())
            for elem, co in counts.items( ) :
                normal += co
            for elem, co in counts.items( ) :
                self.dict_ep.update( { ( elem , pos ) :  co / normal } )
        
        self.dict_bay_prob = { }
        
        for word , pos in self.dict_rev_pos.items():
            normal = 0
            counts = Counter( pos )
            counts = Counter ( th for th in counts.elements( ) )
            for elem , co in counts.items( ) :
                normal += co
            for elem, co in counts.items( ) :
                if word not in self.dict_bay_prob :
                    self.dict_bay_prob.update( { word : [ [ co / normal , elem ] ] } )
                else :
                    self.dict_bay_prob[ word ].append( [ co / normal , elem ] )
        
        x=['adj' ,'adv' ,'adp' ,'conj','det' ,'noun','num' ,'pron','prt' ,'verb','x'  ,'.' ]
        
        # replacing all the empty elements in the transition probability
        # by a downscaled value.
        temp=[]
        for i in x:
            for j in x:
                temp.append((i,j))
        
        l=list(self.dict_tp)
        
        diff=list(set(temp)-set(l))
        tp_min = min( self.dict_tp.values( ) )
        for i in diff :
            self.dict_tp[i] = tp_min / 20.0 #0.0
        pass
        

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):       
        ans = [ ]
        for word in list( sentence ) :
            if word in self.dict_rev_pos :
                temp = [ ]
                for elem in self.dict_bay_prob[ word ] :
                    temp.append( elem[ 0 ] )
                ans.append( self.dict_bay_prob[ word ][ temp.index( max( temp ) ) ][ 1 ] )
            else :
                ans.append( 'x' )
        return ans

    def complex_mcmc(self, sentence):

        ans = [ "noun" ] * len( sentence )
        states = [ 'adj' ,
               'adv' ,
               'adp' ,
               'conj' ,
               'det' ,
               'noun' , 
               'num' , 
               'pron' ,
               'prt' ,
               'verb' ,
               'x',
               '.' ]
        bias_prob = [ ]

        for word in list( sentence ) :
            temp = [ ]
            for pos in states :
                if ( word , pos ) in self.dict_ep :           
                    temp.append( self.dict_ep[ ( word , pos ) ] )
                else :
                    temp.append( 2.0 )

            min_temp = min( temp )
            
            for i in range( len( temp ) ) :
                if temp[ i ] == 2.0 :
                    temp[ i ] = min_temp * 1e-12
            summ = sum( temp )
            
            for i in range( len( temp ) ) :
                temp[ i ] /= summ
            x = 0.0
            for i in range( len( temp ) ) :
                x += temp[ i ]
                temp[ i ] = x
            bias_prob.append( temp )

        ans = [ ]
       
        l = 0
        for l in range(len( sentence )) :
            k = 1000
            ans.append( [ ] )
            while( k > 0 ) :
                k -= 1
                ran = random.random()
                for i in range( 12 ) :
                    if( ran <= bias_prob[ l ][ i ] ) :
                        ans[ l ].append( states[ i ] )
                        break
        
        sol = [ ]
        for elem in ans :
            sol.append( elem[ -1 ] )
            #sol.append( max([(elem.count(chr),chr) for chr in set(elem)])[ 1 ] )
        return sol

    def hmm_viterbi(self, sentence):
        curr_dist ={'adj' : [], 
               'adv' : [], 
               'adp' : [], 
               'conj' : [], 
               'det' : [], 
               'noun' : [], 
               'num' : [], 
               'pron' : [], 
               'prt' : [], 
               'verb' : [], 
               'x' : [], 
               '.' : []}
        
        states = [ 'adj' ,
               'adv' ,
               'adp' ,
               'conj' ,
               'det' ,
               'noun' , 
               'num' , 
               'pron' ,
               'prt' ,
               'verb' ,
               'x',
               '.' ]
        
        ans = [ ]
        prev_pos = ''
        
        y = {'adj' : None , 
               'adv' : None ,
               'adp' : None ,
               'conj' : None , 
               'det' : None , 
               'noun' : None , 
               'num' : None , 
               'pron' : None , 
               'prt' : None , 
               'verb' : None , 
               'x' : None , 
               '.' : None }



        word = list( sentence )[ 0 ]
        p = 0.0
        for pos in states :
            if ( word , pos ) in self.dict_ep :
                p = self.dict_ep[ ( word , pos ) ] * self.init_prob[ pos ]
                curr_dist[ pos ].append( ( "noun" , p ) )
            else :
                curr_dist[ pos ].append( ( "noun" , 1e-8 ) )
        
        ans.append( prev_pos )
        for word in list( sentence )[ 1: ] :
            t = y
            for pos in states :
                max_p = 0.0
                for prev_pos , prev_prob in curr_dist.items( ) :
                    if ( word , pos ) in self.dict_ep :
                        temp = prev_prob[ -1 ][ 1 ] * self.dict_ep[ ( word , pos ) ] * self.dict_tp[ ( prev_pos , pos ) ]
                        if max_p < temp :
                            max_p = temp
                            new_pos = prev_pos
                if max_p == 0.0 :
                    for prev_pos , prev_prob in curr_dist.items( ) :
                        temp = prev_prob[ -1 ][ 1 ] * self.dict_tp[ ( prev_pos , pos ) ] * 5e-7
                        if max_p < temp :
                            max_p = temp
                            new_pos = prev_pos           
                t[ pos ] = ( new_pos , max_p )
            for i , j in t.items( ) :
                curr_dist[ i ].append( j )
        # Backtracking
        max_p = 0.0
        t_pos = ""
        temp = ""
        for pos , word in curr_dist.items( ) :
            if( max_p < word[ -1 ][ 1 ] ) :
                max_p = word[ -1 ][ 1 ]
                t_pos = word[ -1 ][ 0 ]
                temp = pos

        max_p = 0.0
        ans = [ ]
        if not temp :
            temp = 'noun'
        ans.append( temp )
        if not t_pos :
            max_p = 0.0
            for pos in states :
                if max_p < self.dict_tp[ ( ans[ -1 ] , pos ) ] :
                    max_p = self.dict_tp[ ( ans[ -1 ] , pos ) ]
                    t_pos = pos
        
        ans.append( t_pos )
        
        
        
        for i in range( len( sentence ) - 2 , 0 , -1 ) :
            if t_pos :
                t_pos = curr_dist[ t_pos ][ i ][ 0 ]
            else :
                max_p = 0.0
                for pos in states :
                    if max_p < self.dict_tp[ ans[ -1 ] ][ pos ] :
                        max_p = self.dict_tp[ ans[ -1 ] ][ pos ]
                        t_pos = pos

            ans.append( t_pos )
        ans.reverse( )
        return ans[ :len( sentence ) ]

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")
