import json, pdb, math
from prob_generator import ProbGen

PI = {}

def main(pg, rawname, destname):
#It should return a list of json encoded trees. 
#How do I create a json thingy?    
    sentences = get_sentences(rawname)

    py_trees = [cky_recursive(sent, pg) for sent in sentences]
    json_trees = [tree[0] for tree in py_trees]

    write_trees(json_trees, destname)


def cky_recursive(sentence, probgen):
    print sentence
    global PI 
    PI = {}
    if sentence[-1] == '?':
        return cky_help(0, len(sentence) - 1, sentence, 'SBARQ', probgen)
    else:
        return cky_help(0, len(sentence) - 1, sentence, 'S', probgen)


def cky_help(i,j, sent, X, pg):

    if i == j:
        prob = pg.emm_prob(X, sent[i])
        return [X, sent[i]], prob
    else:
        if not (i, j, X) in PI:
            PI[(i, j, X)] = get_max_of_all(i, j, sent, X, pg)
            
        left, right, prob = PI[(i, j, X)]

        return [X, left, right], prob

        
def get_max_of_all(i, j, sent, X, pg):
    
    rule_possibilites = pg.binary_counts[X].keys()
    best = float("-inf")
    Y = None
    Z = None

    for rule in rule_possibilites:
        for s in range(i, j):

            y, z = rule
            p_rule = pg.branching_prob(X, y, z)
            left, p_left = cky_help(i, s, sent, y, pg)
            right, p_right = cky_help(s+1, j, sent, z, pg)
            
            prob = p_right + p_left + p_rule
            #if i == 0 and j == len(sent) - 1:
             #   print y, z, p_rule, p_right, p_left


            if prob > best:
                best = prob
                Y = left
                Z = right

    return Y, Z, best


#Write a generator!
def get_sentences(rawname):
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
    main(ProbGen('new.counts'), 'problem_sentences.dat', 'out_problem.dat')

