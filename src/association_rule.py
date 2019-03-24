import time

import sys
import os

#########################################
# Functional Association Rule Algorithm #
#########################################

def get_association_rules_by_conf(l, threshold = 0.4):
    rule_list = []
    sub_set_list = []
    
    time_start=time.time()
    
    for trans in l.keys():
        trans_set = set(trans)
        
        for sub_set in sub_set_list:
            if sub_set.issubset(trans_set):
                dev_list = list(trans_set - sub_set)
                dev_list.sort()
                dev_tuple = tuple(dev_list)
                conf = l[trans] / l[dev_tuple]
                
                rule = (dev_tuple, tuple(sorted(sub_set)), conf)
                
                if conf >= threshold and rule not in rule_list:
                        rule_list.append(rule)
                        
        sub_set_list.append(trans_set)
    
    time_end=time.time()
    
    print(f"Rules generated in {time_end-time_start}s.")
            
    return rule_list


##################
# Main Procedure #
##################

# process arguments

argv = sys.argv
argc = len(argv)

output_filename = 'association_rule_output.txt'
conf_threshold = 0.4

def print_help():
    print('Usage: python association_rule.py FILENAME [OUTPUT_FILENAME] [CONF_THRESHOLD]\n')
    print(f'FILENAME          File path for data input')
    print(f'OUTPUT_FILENAME   File path for output (default "{output_filename}")')
    print(f'CONF_THRESHOLD    Confidence threshold when generating rules (default "{conf_threshold}")')

if argc < 2:
    print('Error: Invalid Arguments\n')
    print_help()
    exit()

if argv[1] == '--help' or argv[1] == '?':
    print_help()
    exit()

filename = argv[1]

if argc >= 3:
    output_filename = argv[2]

if argc >= 4:
    conf_threshold = float(argv[3])

# read file

data = dict()

with open(filename, 'r') as f:
    while True:
        text_line = f.readline()
        if text_line:
            numbs = text_line.split()

            num_len = len(numbs)

            if num_len <= 1:
                continue
            
            trans = tuple(numbs[:num_len-1])
            support = int(numbs[num_len - 1])

            data[trans] = support
        else:
            break

# run algorithms

print("Generating association rule list...")
rules = get_association_rules_by_conf(data, threshold=conf_threshold)

# write output

with open(output_filename, 'w') as f:
    for rule in rules:
        f.write('(' + ','.join(rule[0]) + ') => (' + ','.join(rule[1]) + ") " + str(rule[2]) + '\n')

print(f"Done. Check out {output_filename}.")