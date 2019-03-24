import time

import sys
import os

################################
# Functional Apriori Algorithm #
################################

def build_sub_trans_list_for_next_prun(last_list):
    result_list = []
    last_list = list(last_list)
    length = len(last_list)
    
    if length == 0:
        return []
    else:
        k = len(last_list[0])
    
    for i in range(length):
        for j in range(i+1,length):
            l1 = list(last_list[i])[:k-1]
            l2 = list(last_list[j])[:k-1]
            l1.sort()
            l2.sort()
            if l1 == l2:
                lr = set(last_list[i])| set(last_list[j])
                lr_list = list(lr)
                lr_list.sort()
                result_list.append(tuple(lr_list))
                
    return result_list

def prun_once_by_support(data, sub_trans_list, threshold = 0.5):
    result_dict = dict()
    data_len = len(data)
    
    for sub_trans in sub_trans_list:
        support = 0
        
        for line in data:
            if set(sub_trans).issubset(set(line)):
                support += 1
        
        if support / data_len >= threshold:
            result_dict[sub_trans] = support
    
    return result_dict

def apriori_get_l_by_support(data, threshold = 0.5, cycles = 100):
    result = dict()
    
    time_start=time.time()
    
    pruned_dict = dict()
    for line in data:
        for item in line:
            key = tuple([item])

            if key in pruned_dict:
                pruned_dict[key] += 1
            else:
                pruned_dict[key] = 1
                
    key_list =  list(pruned_dict.keys())
    key_list.sort()
        
    inner_result = prun_once_by_support(data, key_list, threshold)
    
    result.update(inner_result)
    
    for i in range(cycles):
        sub_trans_list = build_sub_trans_list_for_next_prun(inner_result.keys())
        new_inner_result = prun_once_by_support(data, sub_trans_list, threshold)
        
        inner_result_length = len(new_inner_result)
        
        print(f"The {i+1}th cycle finished. Ended up with {inner_result_length} transactions.")
        
        inner_result = new_inner_result
        result.update(inner_result)
        
        if inner_result_length == 1 or inner_result_length == 0:
            break
        
    time_end=time.time()
            
    print(f"All cycles finished in {time_end-time_start}s.")
    
    return result

##################
# Main Procedure #
##################

# process arguments

argv = sys.argv
argc = len(argv)

output_filename = 'apriori_output.txt'
support_threshold = 0.5

def print_help():
    print('Usage: python apriori.py FILENAME [OUTPUT_FILENAME] [SUPPORT_THRESHOLD]\n')
    print(f'FILENAME             File path for data input')
    print(f'OUTPUT_FILENAME      File path for output (default "{output_filename}")')
    print(f'SUPPORT_THRESHOLD    Support threshold when generating frequent set (default "{support_threshold}")')

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
    support_threshold = float(argv[3])

# read file

data = []

with open(filename, 'r') as f:
    while True:
        text_line = f.readline()
        if text_line:
            data.append(tuple(text_line.split()))
        else:
            break

# run algorithms

print("Starting generating frequent item set...")
l = apriori_get_l_by_support(data, threshold=support_threshold)

# write output

print("Writing output...")

with open(output_filename, 'w') as f:
    for trans, support in l.items():
        f.write(' '.join(trans) + ' ' + str(support) + '\n')

print(f"Done. Check out {output_filename}.")