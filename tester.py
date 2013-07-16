from prob_generator import * 

pg = ProbGen("new.counts")

assert pg.nonterm_counts['ADJP'] == 81
assert pg.unary_counts['NOUN']['years'] == 5 
assert pg.binary_counts['SQ'][('VERB', 'NP+DET')] == 8

assert pg.nonterm_counts['NP+ADVP'] == 1

print sum([pg.unary_counts[d]['_RARE_'] for d in pg.unary_counts.keys()])
