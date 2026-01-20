# Multiple Dict merge
D1={'name':'Advaith',
    'age':12,
}
D2={'class':'VII','location':'Chennai'}
D3= D1 | D2 # Merge into new Dict
print(D3)
#D1 |= D2  # Merge Dict in place using |=
D1.update(D2) # Merge Dict in place using update() method
print(D1)
D1['age'] += 1 # Keys are immutable, values are mutable
print(D1)