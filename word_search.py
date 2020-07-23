
WORD_SEARCH_BLOCK = [
    "TCROHLOSTO",
    "EOPBISONIR",
    "ELKALLESUB",
    "KLESROHAES",
    "AILLUSOGAH",
    "RENULLSCSP",
    "AETIBOLIRT",
    "PKKRGIFORI",
    "HANASYLNMT",
    "AOLINGFOIT",
    "EABOKKAIAK",
    "GIBIFSSLSR",
    ]

words_dict = {
    "BONYFISH": 0,
    "GALAGOS": 0,
    "MOLLUSK": 0,
    "SEAHORSE": 0,
    "TRILOBITE": 0,
    "BISON": 0,
    "COLLIE": 0,
    "IBIS": 0,
    "LION": 0,
    "PARAKEET": 0,
    "SKINK": 0,
    }        

def main():
    print("Word Search Block:")
    show_block( WORD_SEARCH_BLOCK )

    # first search line-by-line, will also search if word is backwards...
    row_by_row()

    # now column by column, bit more tricky...
    col_by_col()

    ## Hard part
    # diagonally, Left 2 Right first...
    diag_L_2_R()

    # same as above but right to left...
    diag_R_2_L()
    
    return 1


def diag_R_2_L():
    tmp_block = WORD_SEARCH_BLOCK[:]
    # function is the same as L_2_R but all diff
    # is that line are reversed BEFORE anything is done
    tmp_block = reverse_lines( tmp_block )

    diag_block = horz_2_diag_L2R( tmp_block )

    for word in words_dict:
        tmp_diag_block = diag_block[:]
        
        if words_dict[word] == 1:
            continue

        found = False
        cords = find_str_in_block( tmp_diag_block, word )

        if cords[0] != -1 and cords[1] != -1:
            found = True

        if found:
            word_len = len( word )
            old_line = tmp_diag_block[ cords[1] ]

            new_line = show_word_on_block( old_line, cords[0], word_len )
            tmp_diag_block[ cords[1] ] = new_line            
            words_dict[word] = 1
            
            print("%s word found:" % word)

            # getting dimensions right so the diagonal order lines can
            # be converted back into horizontal ones.
            y = len(tmp_block) -1
            x = len(tmp_block[0] ) -1
            horz_lines = diag_L2R_2_horz( tmp_diag_block, x, y )

            # you may notice that the horz lines are not reversed in this
            # case, that's because in L_2_R you're essentially iterating
            # backwards, but in this case we're going forward, so no need for it.
            
            show_block( horz_lines )
    
    return 1
    

def diag_L_2_R():
    tmp_block = WORD_SEARCH_BLOCK[:]

    diag_block = horz_2_diag_L2R( tmp_block )

    for word in words_dict:
        tmp_diag_block = diag_block[:]
        
        if words_dict[word] == 1:
            continue

        found = False
        cords = find_str_in_block( tmp_diag_block, word )

        if cords[0] != -1 and cords[1] != -1:
            found = True

        if found:
            word_len = len( word )
            old_line = tmp_diag_block[ cords[1] ]

            new_line = show_word_on_block( old_line, cords[0], word_len )
            tmp_diag_block[ cords[1] ] = new_line            
            words_dict[word] = 1
            
            print("%s word found:" % word)

            # getting dimensions right so the diagonal order lines can
            # be converted back into horizontal ones.
            y = len(tmp_block) -1
            x = len(tmp_block[0] ) -1
            horz_lines = diag_L2R_2_horz( tmp_diag_block, x, y )

            # this just reverses all current horizontal lines
            # as they're in wrong order from the original.
            back_2_normal_block = reverse_lines( horz_lines )
            
            show_block( back_2_normal_block )
    
    return 1

def diag_L2R_2_horz( block, x_axis_len, y_axis_len ):
    tmp_block = block[:]

    diag_list = []
    
    # so empty string are ready for use...
    for i in range( y_axis_len+1 ):
        diag_list.append("")

    start = 0
    end = 1

    for line_i in range(x_axis_len+1):
        for x in range(start, end):
            diag_list[x] += tmp_block[line_i][x]

        if x < x_axis_len:
            end += 1
    
    block_len = len( tmp_block )
    y_start = 1
    tmp_y = y_start

    for line_j, line_str in enumerate( tmp_block[line_i+1:] ):
        for char in line_str:
            diag_list[tmp_y] += char
            tmp_y += 1
        
        y_start += 1
        tmp_y = y_start

    return diag_list

def horz_2_diag_L2R( block ):
    y_axis_len = len(block) -1 # both already in list format (-1 len)
    x_axis_len = len(block[0]) -1
    diag_list = []

    y_start = 0
    x_start = x_axis_len
    x_end = x_axis_len

    ## This is the main outter loop:
    # Basically y only adds by 1 in each X loop, then gets
    # reset back to 0 again after it. 
    while True:
        if x_start < 0:
            x_start = 0
            y_start += 1
            
        tmp_y = y_start
        tmp_str = ""

        for x_i_start in range(x_start, x_end+1):
            if tmp_y >= y_axis_len:
                tmp_str += block[tmp_y][x_i_start]
                break
            
            tmp_str += block[tmp_y][x_i_start]

            if tmp_y < y_axis_len:
                tmp_y += 1
    
        diag_list.append( tmp_str )

        x_start -= 1
        
        if x_start < 0 and y_start == y_axis_len:
            break

    return diag_list



def col_by_col():
    tmp_block = WORD_SEARCH_BLOCK[:]
    # convert columns into rows so search is easier...
    inv_block = inv_col_row( tmp_block )

    for word in words_dict:
        tmp_block = WORD_SEARCH_BLOCK[:]
        inv_block = inv_col_row( tmp_block )
        
        # if already found then just skip...
        if words_dict[word] == 1:
            continue

        found = False
        cords = find_str_in_block( inv_block, word )
        if cords[0] != -1 and cords[1] != -1:
            found = True
        
        word_len = len( word )
        old_line = inv_block[ cords[1] ]
        new_line = show_word_on_block( old_line, cords[0], word_len )
        inv_block[ cords[1] ] = new_line 

        if found:
            words_dict[word] = 1
            
            print("%s word found:" % word)
            # convert the sideways matrix back to normal, but this time
            # with all words found...
            back_2_normal = inv_col_row( inv_block )
            show_block( back_2_normal )

            continue


    return 1

# converts columns into rows and vice versa
def inv_col_row( block ):
    inv_block = []

    y_axis = len(block)
    x_axis = len(block[0])

    tmp_str = ""
    for x in range(x_axis):
        for y in range(y_axis):
            tmp_str += block[y][x]

        inv_block.append(tmp_str)
        tmp_str = ""

    return inv_block

def row_by_row():
    for word in words_dict:
        # resets block being used to lower chars.
        # needs to take slice of whole list since just assigning with '='
        # only give the pointer, it does NOT copy data of original. 
        tmp_block = WORD_SEARCH_BLOCK[:]

        found = False
        cords = find_str_in_block( tmp_block, word )
        if cords[0] != -1 and cords[1] != -1:
            found = True
        
        word_len = len( word )
        old_line = tmp_block[ cords[1] ]
        new_line = show_word_on_block( old_line, cords[0], word_len )
        tmp_block[ cords[1] ] = new_line 

        if found:
            words_dict[word] = 1
            
            print("%s word found:" % word)
            show_block( tmp_block )

            continue

    return 1

# iterates through each line to find string,
# then returns co-ordinates of starting point in list form.
def find_str_in_block( block, word ):
    x_axis = -1
    y_axis = -1
    
    for y, line in enumerate(block):
        index = line.find( word )
        index_reverse = line.find( word[::-1] )

        if index != -1 or index_reverse != -1:
            x_axis = index if index != -1 else index_reverse
            y_axis = y

            break

    return [x_axis, y_axis]

# function to lower chars in line str, starting from
# index given and ending in index + length of word.
#   start = index
#   end = index + len(word)
def show_word_on_block(line_str, index, word_len):
    ast_pad = '*' * word_len
    # uncomment line below and replace "ast_pad"
    # if you want word to be in lower case instead.
    # used '*' since it's hard to distinguish between lower and upper
    # case chars when showing user result.
    #lower_word = line_str[index:word_len+index].lower()
    
    new_line = line_str[:index] + ast_pad + line_str[word_len+index:]

    return new_line

# display block passed through so user can see words found, etc.
def show_block( block ):
    for line in block:
        for char in line:
            print(char, end=" ")
        print()
    print("\n" + "#"*20 + "\n")
    
def reverse_lines( block ):
    reversed_block = []

    for line in block:
        reversed_block.append( line[::-1] )

    return reversed_block

if __name__ == "__main__":

    main()

