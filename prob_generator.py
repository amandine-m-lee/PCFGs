from collections import defaultdict
from __future__ import division


class ProbGen(object):


    def __init__(self, source_file):
        if source_file is None:
            self.srcname = self.get_sourcename()
        else:
            self.srcname = source_file

        self.nonterm_counts = defaultdict(int)
        self.unary_counts = defaultdict(defaultdict(int))
        self.binary_counts = defaultdict(dict)

    def get_sourcename(self):
    
        """ FUNCTION: get_sourcename 
            ARGUMETNS: self

            Gets user input for the filename of the source file (should 
            be of the same form as gene.counts). Checks for valid file and 
            if invalid prompts again"""

        valid_file = False
        while not valid_file:
            print "Please supply a valid filename for the source file."
            file_name = raw_input('> ')
            try:
                valid_file = file(file_name)
            except IOError:
                pass
        return file_name


    def get_counts(self, filename):
#Not super sure if this is the best way of doing it. 
        lines = self.get_lines(filename)

        nonterms = [line.split() for line in lines if 'NONTERMINAL' in line]
        unarys = [line.split() for line in lines if 'UNARYRULE' in line]
        binarys = [line.split() for line in lines if 'BINARYRULE' in line]

#Make this a decorator?
        for line in nonterms:
            count, rule, nt = line
            count = int(count)
            self.nonterm_counts[nt] = count

        for line in unarys:
            count, rule, tag, word = line.split()
            count = int(count)
            self.unary_counts[tag][word] = count

        for line in binarys:
            count, rule, root, left, right = line.split()
            count = int(count)
            self.binary_counts[root][(left, right)] = count


    def get_lines(self, filename):
        with file(filename) as src:
            return src.readlines()
#TODO: Get defaults working correctly. Divide by zero conern. 
    def branching_prob(self, root, left, right):
        return self.binary_counts[root][(left, right)] /\
                self.nonterm_counts[root]
       
    def emm_prob(self, tag, word):
        return self.unary_counts[tag][word] / self.nonterm_counts[tag]

    
def cky_aglo(probgen, srcfile, destfile):


