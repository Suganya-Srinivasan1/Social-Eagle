#Loop
'''
for i in range(100,102):
      print(i)
'''
#passing dictionary using for loop

dict1 = {"apple":4,"banana":2,"grape":6}
for i, j in dict1.items():
      print(f"The price of {i} is {j}")
      

dict1 = {"apple":4,"banana":2,"grape":6}
for i in dict1.values():
      print(i)

dict1 = {"apple":4,"banana":2,"grape":6}
for i in dict1: #dict1.keys()
      print(i)

#Input 2 List and convert to dictionary

L1 = ['apple','banana','grape']
L2 = [4,2,6]
'''
D1 = dict(zip(L1,L2))
print(D1)
'''
D2 = {}
for i in range(len(L1)):
      D2[L1[i]] = L2[i]
print(D2)