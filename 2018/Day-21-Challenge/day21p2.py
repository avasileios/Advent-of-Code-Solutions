def solve():
    # Constants extracted from your specific input
    seed = 16298264
    multiplier = 65899
    
    seen = set()
    last_unique = 0
    reg_1 = 0 

    while True:
        # Instruction 6: bori 1 65536 4
        # Note: reg_1 is reused from the previous loop iteration
        reg_4 = reg_1 | 65536
        reg_1 = seed
        
        while True:
            # Instructions 8-13: The core bitwise hashing logic
            reg_1 += (reg_4 & 255)
            reg_1 &= 16777215
            reg_1 *= multiplier
            reg_1 &= 16777215
            
            # Instructions 14-27: This replaces the slow 'division' loop
            if 256 > reg_4:
                # Instruction 28: eqrr 1 0 5
                if reg_1 in seen:
                    return last_unique
                
                if not seen:
                    print(f"Part 1 (Earliest): {reg_1}")
                
                seen.add(reg_1)
                last_unique = reg_1
                break
            
            # Fast-forwarding the inner loop that slowly divides reg_4 by 256
            reg_4 //= 256

if __name__ == "__main__":
    final_val = solve()
    print(f"Part 2 (Latest): {final_val}")