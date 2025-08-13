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
    left = 0
    center = 0
    right = 0
    for pos in range(pos, 3):
        if pos > 0:
            left = lattice & pos-1
        center = lattice & pos
        right = 0
        if pos < lattice.bit_length():
            right = lattice & pos+1
    return (left, center, right)
        
def buildRuleKey(left, center, right):
    rule_key = 0b0
    rule_key |= left << 2
    rule_key |= center << 1
    rule_key |= right << 0
    return rule_key

#apply rules across the lattice
def applyRule(lattice):
    new_lattice = 0b0
    for pos in range(lattice.bit_length()):
        left, right, center = neighborhood(pos, lattice)
        rule_key = buildRuleKey(left, center, right)
        new_bit = rule[rule_key]
        new_lattice |= new_bit << pos
    
    # Add padding: shift left by 1 to append 0, then add space for prepending
    new_lattice = new_lattice << 1  # Append 0 bit on the right
    # Prepending 0 bit on the left is automatic since we're not setting that bit
    
    return new_lattice


lattice = 0b010
for _ in range(10):
    print(f"{lattice:b}")  
    lattice = applyRule(lattice)
