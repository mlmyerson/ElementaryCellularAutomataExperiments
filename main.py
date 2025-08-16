rules = {
    0: "0",
    1: "1",
    2: "1",
    3: "1",
    4: "0",
    5: "1",
    6: "1",
    7: "0"
}

def apply_rules(input_string):
    left = int(input_string[0], 2)
    center = int(input_string[1], 2)
    right = int(input_string[2], 2)
    rule_key = (left << 2) | (center << 1) | right
    return rules[rule_key]

def iterate_lattice(lattice):
    new_lattice = []
    new_lattice.append("0")
    
    for i in range(len(lattice)):
        left = lattice[i - 1] if i > 0 else '0'
        center = lattice[i]
        right = lattice[i + 1] if i < len(lattice) - 1 else '0'
        neighborhood = left + center + right
        new_lattice.append(apply_rules(neighborhood))
    
    return ''.join(new_lattice)

lattice = "010"
picFile = open("picture.txt", "w")
numFile = open("numbers.txt", "w")
for _ in range(50):
    picFile.write(lattice + "\n")
    # print(lattice)
    numFile.write(str(int(lattice, 2)) + "\n")
    # print(int (lattice, 2)) 
    lattice = iterate_lattice(lattice)

picFile.close()
numFile.close()