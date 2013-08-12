import json, pdb, math
from prob_generator import ProbGen

#The probability table cache
PI = {}

def main(pg, rawname, destname):
    """The main function takes a ProbGen class, the name of the file with newline separated 
    sentences of the passages to be analyzed, and the name of the file to be written with the
    json encoded trees."""

    sentences = get_sentences(rawname)

    py_trees = [cky_recursive(sent, pg) for sent in sentences]
    json_trees = [tree[0] for tree in py_trees]

    write_trees(json_trees, destname)


def cky_recursive(sentence, probgen):
    """Accepts a sentence (list of words) and a probability generator class, returns 
    a nested list of strings representing the tree"""

    print sentence
    global PI 
    PI = {} #Initialize a fresh cache
    #Check sentence type
    if sentence[-1] == '?':
        return cky_help(0, len(sentence) - 1, sentence, 'SBARQ', probgen)
    else:
        return cky_help(0, len(sentence) - 1, sentence, 'S', probgen)


def cky_help(i,j, sent, X, pg):
    """Accepting the starting position i, ending position j, sentence, parent tag X, and a 
    probability generator pg, it returns a string with the most likely subtree given the 
    info and the probability of that subtree"""

    if i == j: #Analyzing a single word - must be a unary rule
        prob = pg.emm_prob(X, sent[i])
        return [X, sent[i]], prob
    else: #Binary rule
        if not (i, j, X) in PI: #Check the cache
            PI[(i, j, X)] = get_max_of_all(i, j, sent, X, pg)
            
        s

        return [X, left, right], prob

def get_max_of_all(i, j, sent, X, pg):
    """Searches through all the combinations of split points and binary rules associated
    with the root X, finding the max. Returns null and negative infinity if none found"""
    
    rule_possibilites = pg.binary_counts[X].keys()
    best = float("-inf")
    Y = None
    Z = None
    best_right = float("-inf")
    best_left = float("-inf")
    LEFT = ''
    RIGHT = ''

    for rule in rule_possibilites:
        for s in range(i, j):

            y, z = rule
            p_rule = pg.branching_prob(X, y, z)
            left, p_left = cky_help(i, s, sent, y, pg)
            right, p_right = cky_help(s+1, j, sent, z, pg)
            
            prob = p_right + p_left + p_rule


            if prob > best: #Update
                best = prob
                Y = left
                Z = right
   
    return Y, Z, best

def get_sentences(rawname):
    """Opens the file of name rawname, returns an array of arrays of strings. The base unit is
    a word"""
    with open(rawname) as f:
        return [line.split() for line in f.readlines()]



def write_trees(json_trees, dest_name):
    """Takes a name for the destination function and a list of json encoded trees
    and prints to file, separated by newline characters"""

    with open(dest_name, 'w') as dest:

        for tree in json_trees:
            dest.write(json.dumps(tree))
            dest.write('\n')

if __name__ == '__main__':

    main(ProbGen('new.counts'), 'parse_dev.dat', 'latest_out.dat')

