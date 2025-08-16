rule = {0: 0, 
        1: 1, 
        2: 1, 
        3: 1, 
        4: 0,
        5: 1,
        6: 1,
        7: 0
        }

def neighborhood(latticePos, lattice):
    # Get bit at position (latticePos-1, latticePos, latticePos+1)
    left = 0
    if latticePos > 0:
        left = (lattice >> (latticePos - 1)) & 1
    
    center = (lattice >> latticePos) & 1
    
    right = 0
    if latticePos < lattice.bit_length() - 1:
        right = (lattice >> (latticePos + 1)) & 1
    
    # print(f"Neighborhood at position {latticePos}: left={left}, center={center}, right={right}")
    return (left, center, right)
        
def buildRuleKey(left, center, right):
    rule_key = 0b0
    rule_key |= left << 2
    rule_key |= center << 1
    rule_key |= right << 0
    return rule_key

#apply rules across the lattice
def applyRule(lattice):
    new_lattice = 0
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
for _ in range(4):
    print(f"0{lattice:b}")  
    lattice = applyRule(lattice)
