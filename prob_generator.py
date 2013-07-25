from __future__ import division
from collections import defaultdict
import math


class ProbGen(object):
    """ The ProbGen classes allows you to read and store a file of unary and binary
    rule counts and nonterminal counts, extracted from a training lexical tree, and then
    generate the probabilties of a specific rule or terminal emission"""

    def __init__(self, source_file):
        """MEMBERS:
        nonterm_counts - Dictionary of {nonterminal::str : count::int}
        unary_counts - Dictionary of {word::string : {tag::string : count::int}}
        binary_counts - Dictionary of 
            {root::string : {(left::string, right::string) : count::int}}"""

        if source_file is None:
            self.srcname = self.get_sourcename()
        else:
            self.srcname = source_file

        self.nonterm_counts = {}
        self.unary_counts = defaultdict(dict)
        self.binary_counts = defaultdict(dict)

        self.populate_dicts()

    def get_sourcename(self):
    
        """ Gets user input for the filename of the source file, which should be of form:
            <#> <RULETYPE> <other arguments...>
            Checks for valid file and if invalid prompts again"""

        valid_file = False
        while not valid_file:
            print "Please supply a valid filename for the source file."
            file_name = raw_input('> ')
            try:
                valid_file = file(file_name)
            except IOError:
                pass
        return file_name


    def populate_dicts(self):
        """ Using the srcname member, get_counts separates the records into the 
            respective tyeps: counts of nonterminals (i.e. VP = verbphrase, DT determiner)
            counts unary rules (i.e. DT -> 'the') and binary rules (i.e NP -> JJ, NP)
            """

        lines = self.get_lines(self.srcname)

        for line in lines:
            parts = line.split()
            rt = parts[1]

            if rt == 'NONTERMINAL':
                count, _, nt = parts
                self.nonterm_counts[nt] = int(count)

            elif rt == 'UNARYRULE':
                count, _, tag, word = parts
                self.unary_counts[word][tag] = int(count)
            
            elif rt == 'BINARYRULE':
                count, _, root, right, left = parts
                self.binary_counts[root][(right, left)] = int(count)


    def get_lines(self, filename):
        """Opens the file and returns a list of strings representing each line"""
        with file(filename) as src:
            return src.readlines()
    
    def branching_prob(self, root, left, right):
        """Returns log(p(left, right | root)), i.e. the probability of a binary rule given
        the root"""

        num = self.binary_counts[root].get((left, right), None)
        try:
            denom = self.nonterm_counts[root] 
        except KeyError as e: #Not sure what to do with this error
            print "Undefined probabilty: root nonterminal does not exist"
            raise

        if num is None:
            return float("-inf")
        else:
            return math.log(num/denom)
       
    def emm_prob(self, tag, word):
        """Returns log(p(word | tag)), the emission probability"""
        
        if word in self.unary_counts:
            num = self.unary_counts[word].get(tag, None)
        elif tag in self.unary_counts['_RARE_']:
            num = self.unary_counts['_RARE_'][tag]
        else:
            num = None            
        try:
            denom = self.nonterm_counts[tag]
        except KeyError:
            print "Tag never seen before"
            raise
        
        if num is None:
            return float("-inf")
        else: 
            return math.log(num/denom)


