# Set
S1 = {'Python', 'Java'}
S2 = {'C+','.net','Java'}
S3 = S1 | S2 # Merge 2 set and return all values
S4 = S1 & S2 # Merge and return the common value only
FS1 = frozenset(S1)
print(S3)
print(S4)
print(FS1)
for i in FS1:
    print(i)
F1=frozenset(i * i for i in range(5))   
for item in F1:
    print(item)
'''
Key Characteristics of frozenset:
Immutable: Elements cannot be added or removed after
creation, which means methods like add() or remove()
are not available.
Hashable: This immutability allows frozenset objects
to be used as keys in dictionaries or as elements 
within other sets, which mutable sets cannot be.
Unordered: Elements do not have a specific index, 
so you cannot access them using frozenset[0]. 
'''