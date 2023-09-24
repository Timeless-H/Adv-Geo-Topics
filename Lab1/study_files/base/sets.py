'''a set is a collection of items where no single item shows up twice.
unlike lists, sets dont have any particular order to it. the most important
thing here is if a particular value is or not in the set'''
s = set()
s.add(1)
s.add(3)
s.add(5)
s.add(3)
print(s)  # {1,3,5}  the unique values
