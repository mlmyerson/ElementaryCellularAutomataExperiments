rule = {0: 0, 
        1: 1, 
        2: 1, 
        3: 1, 
        4: 0,
        5: 1,
        6: 1,
        7: 0
        }

def neighborhood(pos, lattice):
    out = 0
    for pos in range(pos, 3):
        left = False
        if pos > -1:
            left = bool(lattice & pos-1) != 0
        center = bool(lattice & pos) != 0
        right = False
        if pos < lattice.bit_length() - 1:
            right = bool(lattice & pos+1) != 0
    return (left, center, right)
        
lattice = 0b010
# latticeInt = int(lattice, 2)

for pos in range(lattice.bit_length()):
    left, right, center = neighborhood(pos, lattice)
    # is_one = bool(lattice & pos) != 0
    # if (is_one):


print(rule)