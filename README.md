#The question

316 sequecing (316 line, column1+column2)

Select a subgroup. Inside this group, all sequence should have more than or equal to m mismatch. 

Maxinum this subgroup.

First, generating mismatch matrix. In this matrix, the manhatten distance between two sequences were calculated.

Secondly, convert mismatch matrix to "is pass" matrix. Pass means for the given two sequences, the manhatten distance should be more than or equal to m mismatches. In this matrix, if two sequence has more than m mismatches, than this value should be 1. Else, zero.

Now, the question came to find the maximun submatrix which contains only 1 in the "is pass" matrix.

#Algorithm:
The initiation matrix:

col| 0 | 1 | 2 | 3
---|---|---|---|---
0  | 1 | 0 | 1 | 1 
1  | 0 | 1 | 0 | 0 
2  | 1 | 0 | 1 | 1 
3  | 1 | 0 | 1 | 1 


Using a graph to present this matrix.
The low\_to\_high hash could be like this reversly:

```
0 => 2
0 => 3
2 => 3
```

The high\_to\_low hash could be like:

```
3 => 0
3 => 2
2 => 0
```

Initiation for the submatrix. Using the sub-index to represent the sub-matrix. When initiation, the length of the sub-index should be 2. Here, using the key-value pairs as this sub-index. As a result, the initiated sub-index should be like this:

```
[ [0,2], [0,3], [2,3] ]
```

Next, search all index( e.g, [0,2] ) in sub-index lists (e.g. [ [0,2], [0,3], [2,3] ] ). For each element (0, 2 in [0, 2] for example) in all index, scan the high\_to\_low hash to see if this index can add one more element.

e.g.:
for [0, 2], the high\_to\_low hash is:

```
0 => NULL
2 => 0
```

which indicates there is no more elements that could be added to this index.

however, for [2, 3], the high\_to\_low hash is:

```
2 => 0
3 => 2, 0
```

the intersect for the two values is 0, which means 0 could be added to index [2, 3].

After scanning all indexes with length of 2, the new sub-index list with length of 3 is [ [0, 2, 3] ].
As no hash key for 0, this sub-index is the answer. 

So the resulting output matrix is like:

 col| 0 | 2 | 3
----|---|---|---
0   | 1 | 1 | 1 
2   | 1 | 1 | 1 
3   | 1 | 1 | 1 

Which is the maximun submatrix containing only 1 in the "is pass" matrix.
