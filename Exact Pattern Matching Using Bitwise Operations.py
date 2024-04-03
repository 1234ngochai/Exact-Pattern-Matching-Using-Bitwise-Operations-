#Author: Ngoc Hai Nguyen
#ID : 32212046

from bitarray import bitarray
import sys

def precompute_delta_table_bitarray(pat):
    """
    Optimizes the exact pattern matching process using simple bitwise operations.

    In a naive pattern matching approach, for each position j (ranging from 0 to n,
    where n is the length of the text), a delta value for txt[j] is computed.
    This computation requires m comparisons for each position in txt, where m
    is the length of the pattern, since each character must be compared individually.

    This function precomputes a delta table to optimize the computation of these values.
    Given that delta represents the bitwise comparison of a character against the pattern,
    we can precompute delta for each character within the ASCII range [33, 126]. This
    range is specified by the problem's constraints.

    By doing so, we reduce the complexity from O(mn) to O(m*p), where p represents the
    number of characters in the specified ASCII range. Since p is a constant, the complexity
    effectively reduces to O(m), achieving linear time. This significantly improves the
    computational efficiency of the algorithm.

    The delta table stores a bitarray for each ASCII character within the [33, 126] range.
    Each bitarray's length corresponds to the length of the pattern 'pat'. Each bit
    in a bitarray indicates whether the corresponding character in 'pat' matches (0)
    or mismatches (1) the ASCII character the bitarray represents. The bitarrays are
    reversed to align with the pattern matching's reverse search direction.

    Parameters:
    - pat (str): The pattern for which to precompute delta values. It should
      consist of ASCII characters within the range [33, 126].

    Returns:
    - A list of bitarrays, each corresponding to an ASCII character in the range
      [33, 126]. Each bitarray represents the delta values calculated based on
      character mismatches between the ASCII character and the pattern 'pat'.
    """
    # Define the start of the ASCII range
    ascii_start = 33
    # Define the end of the ASCII range.
    ascii_end = 126
    # length of the pattern
    m = len(pat)
    #initialise the table for each of the characters in the range
    delta_table = [None] * (ascii_end - ascii_start + 1)

    # Fill the delta table with bitarrays representing the delta for each character
    for ascii_val in range(ascii_start, ascii_end + 1):
        # Convert the ASCII value to its corresponding character.
        char = chr(ascii_val)
        #init a bitarray with all 0
        delta = bitarray('0' * m)
        # Compare this character against each character in the pattern.
        for i, pat_char in enumerate(pat):
            # If the character does not match the pattern character at position i,
            # set the corresponding bit in the delta bitarray to 1.
            delta[i] = char != pat_char
        # Reverse the bitarray to match the pattern direction
        delta_table[ascii_val - ascii_start] = delta[::-1]

    return delta_table


def initialize_bit_vector_at_position_m(txt, pat, m):
    # Initialize the bit vector with all bits set to 1
    bit_vector = bitarray('1' * m)
    
    # Check the match for the substring of the text ending at position m
    for i in range(1, m + 1):
        # slicing the patter smaller and smaller
        pattern_slice = pat[:i]
        # The corresponding slice of text ending at position m
        text_slice = txt[m-i:m]
        
        # If the slices match, set the bit at the corresponding position to 0
        if pattern_slice == text_slice:
            bit_vector[m - i] = 0
    
    return bit_vector


def find_pattern(txt, pat, delta_table):
    m, n = len(pat), len(txt)
    # end if the input is weird
    if m == 0 or n < m:
        return []

    # Initialize the bit vector for the position starting from m, where we start the comparision first
    bit_vector = initialize_bit_vector_at_position_m(txt, pat, m)
    matches = []
    
    # Check for a match at the initial position m
    if bit_vector[0] == 0:
        matches.append(0)  # Match found at the beginning of the text

    # Iterate over the text starting from the index m
    for j in range(m, n):
        print(f"Before update for txt[{j}] = '{txt[j]}': {bit_vector.to01()}")
        
        # Left-shift the bit vector by slicing and adding 0 :v
        bit_vector = bit_vector[1:] + bitarray('0')
        print(f"After shift for txt[{j}] = '{txt[j]}': {bit_vector.to01()}")
        
        # Get the Delta vector for the current character and perform bitwise OR
        current_char_delta = delta_table[ord(txt[j]) - 33] # the offset where start at 33
        bit_vector = bit_vector | current_char_delta
        print(f"Delta vector for '{txt[j]}'     : {current_char_delta.to01()}")
        print(f"After OR with Delta for txt[{j}]: {bit_vector.to01()}")

        # If the leftmost bit of the bit vector is 0, we have a match
        if bit_vector[0] == 0:
            match_position = j - m + 1
            print(f"Match found at position: {match_position}\n")
            matches.append(match_position)
        else:
            print()

    return matches

# Example usage:
# txt = "xaadadadaxdad"
# pat = "dadax"

# txt = "aaaabaaacaaaaa"
# pat = "abcd"
# pat = "aaa"

def main(text_filename, pattern_filename):
    # Read the text from the text file
    with open(text_filename, 'r') as file:
        txt = file.read().strip()
    
    # Read the pattern from the pattern file
    with open(pattern_filename, 'r') as file:
        pat = file.read().strip()
    
    # Compute the Delta table
    delta_table = precompute_delta_table_bitarray(pat)
    
    # Find pattern matches in the text
    matches = find_pattern(txt, pat, delta_table)
    
    # Output match positions to output_q2.txt
    with open('output_q2.txt', 'w') as file:
        for position in sorted(matches):
            file.write(str(position + 1) + '\n')  # Convert to 1-based indexing

if __name__ == "__main__":
    text_filename = sys.argv[1]
    pattern_filename = sys.argv[2]
    main(text_filename, pattern_filename)
