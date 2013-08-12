Collins's NLP Lab II: PROBABLISTIC CONTEXT FREE GRAMMERS
========================================================

The goal is to generate parse trees for English sentences, which in this case happen to be trivia questions. 
My job was to compile the probabilities of specific rules governing the branching of the tree using training data with smoothing,
and then implement the CKY dynamic programming algorithm, which recursively finds the subtree with the maximum probability 
given my estimated probabilies.

Author: Amandine Lee

Email: amandine.m.lee@gmail.com

Files
------
PYTHON FILES CREATED BY ME **ie. the most important parts**:

1. replace_rare_tree.py - Can be imported for member functions or run as a script for the given data files. Takes a JSON nested list representing a parse tree (the training data) and a text file with the counts output by count_cfg_freq.py. Tallies the words that occur with a given tag < 5 times, creates a new training JSON file with those words replaced by '_RARE_'
2. probability_generator.py - A class that stores the counts of different rules from training data, and can be called to calculate probabilities from those counts.
3. cky_algo.py - Script that implements the CKY algorithm, calculating the maximum probable parse trees from newline seaparated sentences, and writes JSON-encoded trees to a file.

GIVEN PYTHON FILES:

1. count_cfg_freq.py - Takes a JSON tree file, outputs the counts and types of each: NONTERMINAL, UNARYRULE, BINARYRULE
2. eval_parser.py - compares two files (for the development sent) and gives the efficiency of your analysis. 
3. pretty_print_tree.py - Makes indented versions of trees. Takes single-line-tree fomrat files. 

GIVEN TEXT FILES:

1. parse_train.dat - Each line represents a sentences, parsed into its lexical tree, stored in JSON format. The first is the data, the second the right branch, the third the left branch, until it terminates with a terminal (actual word) and it's tag, stored as ["TAG", "word"]
2. cfg.counts - Original counts from training data. Each line represents one piece of data, as:  <count> <count-type> <nonterminal/terminal sympbols...>
3. parse_dev.dat - Each line is a sentence to be analyzes.
4. parse_dev.key - The correct trees stored in JSON format
5. parse_test.dat - More single-line sentences, the test file. 
6. tree.example - A single tree in JSON as an example

GENERATED TEXT FILES

1. new.counts - Counts with _RARE_ type

