# List  - Methods
task = ["set","code","sleep"]
task.append("repeat")
print(task)

a=[1,2,3]
b=[4,5]
a.extend(b)
print(a)
a.insert(1,1.5)
print(a)
a.remove(1.5)
print(a)
c=a.pop(2)
print(a)
print(c)
d=a.index(4,0,3)
print(d)

students = [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
# Sort by age (the third element, index 2)
students.sort(key=lambda st:st[0],reverse=True)
students_sorted=sorted(students,key=lambda st: (st[1],st[2]))
print(students)
print(students_sorted)

#append(item): Adds an item to the end of the list.
#extend(iterable): Appends elements from an iterable to the list.
#insert(index, item): Inserts an item at a specific index.
#remove(item): Removes the first occurrence of an item by value.
#pop([index]): Removes and returns an item at a given index (or the last item if no index is specified).
#clear(): Removes all elements from the list.
#index(item, [start, end]): Returns the index of the first occurrence of an item.
#count(item): Returns the number of times an item appears in the list.
#sort(*, key=None, reverse=False): Sorts the list in place.
#reverse(): Reverses the list in place.
#copy(): Returns a shallow copy of the list. 