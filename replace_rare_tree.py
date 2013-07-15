"""This script and its memeber fuunctions can be used to take a JSON encripted
list of trees, separated by newlines, and a file of the unary rule counts (i.e.
NOUN -> apple) and replace the terminals with (apple) fewer than 5 counts given 
a specific tag (NOUN) with '_RARE_'"""

import json
from sys import argv

def get_rares(countsname):
    """Compiles and returns a set of the "rare" (word, tag) values from a file of unary
    rule counts of name 'countsname'."""

    with open(countsname) as countsrc:
        
        rares = set()

        for line in countsrc.readlines():
            if 'UNARYRULE' in line:
                count, rule, tag, word = line.split()
                
                if int(count) < 5:
                    rares.add((word, tag))
        return rares
            
def recursive_rr(tree, rareset):
    """Takes a nested list in loaded JSON format and a set of rare (word, tag) pairs
    and returns the """ #TODO fix this thingy. 
#tree must be a json object
#TODO: Make flexible, make a decorator with two functions as arguments? one for terminals
#one for non-terminals
    if len(tree) == 2:
        tag = tree[0]
        word = tree[1]
        if (word, tag) in rareset:
            tree[1] = "_RARE_"
    elif len(tree) == 3:
        recursive_rr(tree[1], rareset)
        recursive_rr(tree[2], rareset)
    else:
        error("Not lexical tree")
#TODO: Apply to every item in a list more directly? Well that's what list comprehension does
#

def replace_all_trees(jtrees, rareset): #Apply to every tree in list, make more general. 
    for tree in jtrees:
        recursive_rr(tree, rareset)

def write_trees(dest_name, json_trees):

    dest = open(dest_name, 'w')

    for tree in json_trees:
        dest.write(json.dumps(tree))
        dest.write('\n')

def get_json_trees_from_file(filename):
    tree_strings = open(filename).readlines()
    return [json.loads(line) for line in tree_strings]

#TODO: Make ordering more logical

if __name__ == "__main__":
    script, counts_file, train_file, dest_file = argv

    rares = get_rares(counts_file)

    jtrees = get_json_trees_from_file(train_file)
    replace_all_trees(jtrees, rares)

    write_trees(dest_file, jtrees)
    
    
