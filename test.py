"""
        0   1   2   3                       0   2   3
    0   1   0   1   1                    0  1   1   1
    1   0   1   0   0         =>         2  1   1   1
    2   1   0   1   1                    3  1   1   1
    3   1   0   1   1                    
    
            0 => 2              [ [1],[2],[3],[4] ]  =>  [ [], [], [3, 1], [4, 3], [4, 1]  ] => [ [], [], [], [4, 3, 1]  ]
            0 => 3
            2 => 3
"""
import numpy as np

hash_l2h = {}
hash_l2h[0] = [2, 3]
hash_l2h[2] = [3]

hash_h2l = {}
hash_h2l[3] = [0, 2]
hash_h2l[2] = [0]

hash_stat = [ [0], [1], [2], [3] ]
hash_stat = [ [0,2], [0,3], [2,3] ]
hash_stat = []
for k, v in hash_h2l.iteritems():
    for vv in v:
        hash_stat.append([k, vv])

#hash_stat = [ [0,2,3] ]
l_out = []


for l_elem in hash_stat:
    l_tmp = []
    for i in l_elem:
        if i in  hash_h2l:
            l_tmp.append( hash_h2l[i])
        else:
            l_tmp.append([])
    
    tmp = np.array(l_tmp)
    elem_new = reduce(np.intersect1d, tmp)
    print tmp, elem_new, l_elem
    if elem_new.shape[0] > 0:
        for new in elem_new:
            l_new = l_elem + [new]
            if len(set(l_new)) == len(l_new):
                l_out.append(sorted(l_new))
                

print np.unique(np.array(l_out))
        
        
        