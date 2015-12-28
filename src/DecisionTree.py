'''
NAME- VINAYAK MITTAL
SBU ID - 110385943
NET ID - VMITTAL    

NAME - ALPIT KUMAR GUPTA
SBU ID - 110451714
NET ID - ALGUPTA
'''

import math
import sys

def loadData(data_file, split_ratio):    
    
    f = open(data_file)
    data_set = []
    line = f.readline()        
    
    while line:
        temp = line.strip('\n').split(',')            
        data_set.append(temp)        
        line = f.readline()
        
    split_point = int(len(data_set)*split_ratio)     
    train_set = data_set[:split_point]
    test_set = data_set[split_point:]
    
    print "Total DataSet Size: ", len(data_set)
    print "Training DataSet Size: ", len(train_set)
    print "Testing DataSet Size: ", len(test_set)
    return train_set, test_set
    
def find_pos_neg(data_set):
    
    pos_cnt = 0        
        
    for row in data_set:    
        if row[-1] == '+':
            pos_cnt = pos_cnt + 1
        
    return pos_cnt

def find_unique_attr(data_set):
    
    attr_list = [[] for x in range(len(data_set[0])-1)]    
    
    for row in data_set:
        for i in range(len(row)-1):
            if row[i] not in attr_list[i]:
                attr_list[i].append(row[i])
                
    return attr_list

def calculate_entropy(pos_cnt, tot_cnt):    
    neg_cnt = tot_cnt - pos_cnt    
    tot_cnt = float(tot_cnt)    
    
    if neg_cnt == 0 or pos_cnt == 0:        
        entropy = 0.0
    elif pos_cnt == neg_cnt:
        entropy = 1.0
    else:
        entropy = -(pos_cnt/tot_cnt)*math.log(pos_cnt/tot_cnt,2) - (neg_cnt/tot_cnt)*math.log(neg_cnt/tot_cnt,2)
        
    return entropy
        
def find_updated_data_set(data_set, clm_indx, sub_attr):
    updated_data_set = []
        
    for row in data_set:                
        if sub_attr in row[clm_indx]:
            updated_data_set.append(row)
             
    return updated_data_set

def check_if_same(data_set):
    data_label = [row[-1] for row in data_set]    
    data_label = list(set(data_label))
    
    if len(data_label) == 1:
        return data_label[0]    
        
    return False

def build_decision_tree(data_set, attr_list, used_col):
    
    #print "Used Column=> ", used_col
    isSame = check_if_same(data_set)
    
    if isSame is not False:
        return isSame
    
    if len(used_col) == 9:
        return
    
    len_ds = len(data_set)    
    pos_cnt = find_pos_neg(data_set)
    
    base_entropy = calculate_entropy(pos_cnt, len(data_set))
        
    max_info = -1
    clm_indx = -1
    
    for i in range(len(attr_list)):        
        if i in [1,2,7,10,13,14]:
            continue
        
        if i in used_col:            
            continue
        
        column = attr_list[i]
        attr_entropy = 0            
                                    
        for attr in column:
            pos_cnt = 0
            tot_cnt = 0
            for row in data_set:
                if attr in row:
                    tot_cnt = tot_cnt + 1
                    if row[-1] == '+':
                        pos_cnt = pos_cnt + 1
                                                        
            entropy = calculate_entropy(pos_cnt, tot_cnt)
            entropy = (tot_cnt/(float)(len_ds))*entropy
                                
            attr_entropy = attr_entropy + entropy      
        
        info_gain = base_entropy - attr_entropy
        if info_gain > max_info:
            max_info = info_gain
            clm_indx = i                                      
    
    decision_tree = {clm_indx:{}}
    sub_attr = attr_list[clm_indx]    
    used_col.append(clm_indx)           
    
    for sattr in sub_attr:
        updated_data_set = find_updated_data_set(data_set, clm_indx, sattr)
        decision_tree[clm_indx][sattr] = build_decision_tree(updated_data_set, attr_list, used_col)    
    
    print decision_tree
    
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print "Invalid arguments passed!"
        
        
    data_file = sys.argv[1]
    split_ratio = float(sys.argv[2])
    print "File Received :", data_file
    print "Split Ratio: ",split_ratio
    data_set, train_set = loadData(data_file,split_ratio)
    attr_list = find_unique_attr(data_set)    
    build_decision_tree(data_set, attr_list, [])