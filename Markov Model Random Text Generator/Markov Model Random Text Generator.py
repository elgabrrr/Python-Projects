import math
import random
from typing import Any, List, Tuple, Set, Dict, DefaultDict, Counter, Deque
from typing import Sequence, Mapping, Iterable, Iterator, Generator
from collections import defaultdict, Counter, deque
from itertools import product, islice, chain
import doctest

dna = 'ATGCGCATGCGTGCATGTATATACACACGTGTACGCGCGTACGCACATGTGCGTATGTGCGCACACGTACACGCGTATGT'

####################################################################################################################################################################
########################################################################-TYPE DEFINITIONS-##########################################################################
####################################################################################################################################################################

Distribution = Mapping[str, int]

MarkovModel = Mapping[str, Distribution]

allowed_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
                   'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
                   'Y', 'Z', '¡', '!', ' ', ',', '(', ')', '.', ':', ';', '?', '¿', 'á', 'é', 'í', 'ó', 'ú']

####################################################################################################################################################################
######################################################################-FUNCTION DEFINITIONS-########################################################################
####################################################################################################################################################################

def cleanup(string: Iterable[str]) -> Generator[str, None, None]:
    """Function takes an iterable over characters and reutrns a generator for characters that yields a cleaned up
        version of the result.
        
    >>> ''.join(i for i in cleanup("Emma\\n by Jane         Austen"))
    'Emma by Jane Austen'
    >>> ''.join(i for i in cleanup("      Hi, this    \\n is a    doctest.     "))
    ' Hi, this is a doctest.'
    """
    is_space = False
    for character in string:
        if character.isspace():
            is_space = True
        else:
            if character not in allowed_characters:
                continue
            if is_space:
                is_space = False                
                yield " "
            yield character

####################################################################################################################################################################

def make_model(s: Iterable[str], order: int) -> dict:
    """Function takes in an iterable string and an integer n and outputs the Marcov Model of order n of that string.
    
    Assumptions: order >= 0, s is an iterable string.
    
    >>> make_model(dna, 0) == {'': {'A': 18, 'C': 21, 'G': 22, 'T': 19}}
    True
    >>> make_model(dna, 1) == {'A': {'C': 10, 'T':  8}, 'C': {'A':  9, 'G': 12}, 'G': {'C': 11, 'T': 11}, 'T': {'A':  8, 'G': 10}}
    True
    """
    assert order >= 0
    
    
    d: Deque[str] = deque([], order)                      #deque of maximum length 'order'
    mm = defaultdict(Counter)
    
    if order == 0:
        mm = {'': Counter(s)}                             #mm of order 0 as defined above
    else:
        for i in s:
            if len(d) == order:                           
                l = ''.join(x for x in d)                 #l will be the keys of mm, strings of order 'order'
                mm[l].update(i)                           #key takeaway: mm[l] is updated before d.append(i), so -
            d.append(i)                                   #i is always one character after the last one in d
    for i in mm:       
        mm[i] = dict(mm[i])                               #for loop turns counters in mm to dictionary types for aesthetics
        
    return dict(mm)

####################################################################################################################################################################

def generate(mm: dict, target_len: int) -> str:
    """Function takes in a Marcov Model and a target length and outputs a string of at most the target length,
    based on a weighted first choice and the distribution of the marcov model.
    
    Assumptions: Marcov Model is a  dictionary of n-grams and distiributions, target length is bigger than or equal to
    the length of the n-grams in the Marcov Model
    >>> len(generate(emma_model[1], 100)) <= 100
    True
    >>> type(generate(emma_model[1], 10)) == str
    True
    """
    
    
    total_ngrams = sum((sum(mm[i].values()) for i in mm.keys()))      #defined out of probability_of_ngram
                                                                      #to avoid re-computations
#------------------------------------------------------------------------------------------------------------------------------------
    def order(mm: dict) -> int:
        """Gives the length of a dictionary's first key.
        """
        for i in mm:                                                  #for loop only goes over first element because             
            return len(i)                                             #return acts as break statement
        
#------------------------------------------------------------------------------------------------------------------------------------
    def probability_of_n_gram(ngram: str, mm: dict, previous: str = '', first_time: str = 'Yes') -> float:
        """Calculates the probability of a given n-gram appearing, if it is called for the first time,
        if not, it calculates the probability of a character appearing when knowing the previous n-gram.
        """                                                                              
                                                                              
        if first_time == 'Yes':
            count_ngram = sum(mm[ngram].values())                      #total count of an n-gram
            nonlocal total_ngrams                                      #total n-grams in marcov-model
            
        elif first_time == 'No':
            count_ngram = mm[previous][ngram]                          #number of times ngram appears after previous_ngram                                                              
            total_ngrams = sum([mm[previous][i] for i in mm[previous].keys()])   #total times a symbol appeared afterwards
                                                                                          
        return count_ngram / total_ngrams                            
        
        
        
#------------------------------------------------------------------------------------------------------------------------------------

    order = int(order(mm))
    assert target_len >= order
    
    d: Deque[str] = deque([], order)                                   
    b: Deque[str] = deque([], 1)                                       

    result = random.choices(list(mm.keys()),[probability_of_n_gram(i, mm) for i in mm])[0] #weighted choice for first n-gram
    
    b.append(result)                                                   #b contains the current n-gram separated for apending
    
    for i in iter(result):                                             #d contains the n-gram in str form in just one cell
        d.append(i)
    
    while b[0] in mm:
        x = random.choices(list(mm[b[0]].keys()), (probability_of_n_gram(i, mm, b[0], 'No') for i in mm[b[0]]))[0]
        result = result + x
        
        d.append(x)                      
        b.append(''.join(i for i in d))                                #appends new current n-gram for checking while statement
        
        if len(result) == target_len:                                  #as to not exceed the target length
            break
        
    
    return result

####################################################################################################################################################################
###########################################################################-DOCTESTS-###############################################################################
####################################################################################################################################################################

print('################################################ DOCTESTS ################################################')

doctest.run_docstring_examples(cleanup, globals(), verbose=True, name='cleanup')

doctest.run_docstring_examples(make_model, globals(), verbose=True, name='make_model')

print('##########################################################################################################')

####################################################################################################################################################################
###########################################################################-MAKE MODEL-#############################################################################
####################################################################################################################################################################

with open('The Quixote Text.txt') as f:
    quixote_model = make_model(cleanup(chain.from_iterable(f)), 10)

with open('T.txt') as f:
    bee_movie_model = make_model(cleanup(chain.from_iterable(f)), 2)


####################################################################################################################################################################
######################################################################-GENERATE NEW TEXT-###########################################################################
####################################################################################################################################################################

#sorted_quixote = '| ' + ' | '.join(i for i in sorted([i for i in bee_movie_model[''].keys()])) + ' |'

#print('Symbols in text:', sorted_quixote)


print(generate(bee_movie_model, 2000))