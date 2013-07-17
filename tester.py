from prob_generator import * 

pg = ProbGen("new.counts")

assert pg.nonterm_counts['ADJP'] == 81
assert pg.unary_counts['years']['NOUN'] == 5 
assert pg.binary_counts['SQ'][('VERB', 'NP+DET')] == 8

assert pg.nonterm_counts['NP+ADVP'] == 1

tags = pg.unary_counts['a'].keys()

for tag in tags:
    print tag, pg.emm_prob(tag, 'a')
    print '_RARE_', pg.emm_prob(tag, '_RARE_')
