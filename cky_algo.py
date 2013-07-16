import json
from prob_generator import ProbGen

PROBTABLE = {}

def main(pg, rawname, destname):
#It should return a list of json encoded trees. 
#How do I create a json thingy?    
    sentences = get_sentences(rawname)

    py_trees = [cky_recursive(sent, pg) for sent in sentences]
    json_trees, prob = [json.dumps(tree) for tree in py_trees]

    write_trees(json_trees, destname)


def cky_recursive(sentence, probgen):
    return cky_help(1, len(sentence), 'S', probgen)

def cky_help(i,j, sent, X, pg):

    if i == j:
        X = max(pg.nonterm_counts.key(), key= lambda x: pg.emm_prob(x, sent[i]))
        pi = pg.emm_prob(X, sent[i])
        return [X, sent[i]], pi
    else:
        left, right, pi = get_max_of_all(i, j, sent, X, pg)

        return [X, left, right], pi

        
def get_max_of_all(i, j, sent, X, pg):
    rule_possibilites = pg.binary_counts[X].keys()
    best = 0
    Y = []
    Z = []

    for rule in rule_possibilites:
        for s in xrange(i, j+1):
            y, z = rule
            p_rule = pg.branching_prob(X, y, z)
            left, p_left = cky_help(i, s, sent, y, pg)
            right, p_right = cky_help(s+1, j, sent, z, pg)
            pi = p_rule * p_left * p_right
            
            if pi > best:
                best = pi
                Y = left
                Z = right

    return Y, Z, best



#Write a generator!
def get_sentences(rawname):
    with open(srcfile) as f:
        return [line.split() for line in f.getlines()]



def write_trees(json_trees, destname):
    """Takes a name for the destination function and a list of json encoded trees
    and prints to file, separated by newline characters"""

    dest = open(dest_name, 'w')

    for tree in json_trees:
        dest.write(json.dumps(tree))
        dest.write('\n')

    




if __name__ == '__main__':
    main('new.counts', 'parse_dev.dat', 'out_dev.dat')

