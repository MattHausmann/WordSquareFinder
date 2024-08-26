word_list = "elevens.txt"
words = []

with open(word_list, "r") as f:
    words = [line.replace("\n","") for line in f.readlines()]

length = len(words[0])
letters = 26
A = ord('a')

#straint_freqs[idx * 26 + ltr] = N means "there are N words s.t. word[idx] == chr(ltr+A)
#ltr goes from 0-25, it's the 0-indexed alphabet position of the letter
#for instance, ltr=0 means a, and ltr=5 means f
#for instance, if straint_freqs[4* 26 + 10]=2411, there are 2411 words s.t. word[4] == 'k'
straint_freqs = []
straint_freqs = [0] * length * 26

#find all the straint_freqs
for word in words:
    for idx in range(len(word)):
            ltr = ord(word[idx]) - A
            straint_freqs[idx * 26 + ltr] += 1

#figure out which row is the best one to put our initial row in 
words_guessed_per_row = [0] * 11
best_straint_freqs = [0] * len(straint_freqs)
for row in range(11):
    for word in words:
            words_guessed = len(words)
            best_idx = -1
            best_ltr = -1
            for idx in range(11):
                    if idx != row:
                            ltr = ord(word[idx]) - ord('a')
                            words_for_idx = straint_freqs[row*26+ltr]
                            if words_for_idx <= words_guessed:
                                    words_guessed = words_for_idx
                                    best_idx = idx
                                    best_ltr = ltr
            words_guessed_per_row[row] += words_guessed
            best_straint_freqs[row*26+best_ltr] += 1

sorted_straints = list(range(len(best_straint_freqs)))
best_straint_freqs, sorted_straints = (list(t) for t in zip(*sorted(zip(best_straint_freqs, sorted_straints), reverse=True)))


#for each word in the given row, we want to find the idx with the least common constraint
#then we want to 


sorted_words = []
added_set = set()
straint_index = -1
while len(sorted_words) < len(words):
    straint_index += 1
    straint = sorted_straints[straint_index]
    idx = straint//26
    ltr = straint%26
    for word in words:
        if word not in added_set:
            if word[idx] == chr(ord('a') + ltr):
                    added_set.add(word)
                    sorted_words.append(word)



#now bitsets for every constraint
bitsets = [0]*286
power = 1
all_words_bitset = 0
for word in sorted_words:
    for idx in range(len(word)):
        ltr = ord(word[idx])-A
        bitsets[idx*26+ltr] |= power
    all_words_bitset |= power
    power <<= 1

def find_most_constrained_row_and_bitset(square, list_of_rows):
    power = 1
    most_constrained_bitset = all_words_bitset
    best_row = 10
    for idx in range(len(square)):
         if idx not in list_of_rows:
            current_bitset = all_words_bitset
            for row_num in list_of_rows:
                word = square[row_num]
                ltr = ord(word[idx]) - A
                current_bitset &= bitsets[row_num*26+ltr]
            if current_bitset.bit_count() <= most_constrained_bitset.bit_count():
                most_constrained_bitset = current_bitset
                best_row = idx
    return best_row, most_constrained_bitset

def build_square(square, row_nums, word_idx, word_bit, words_bitset, num_second_words_tried=0):
    if len(row_nums) == len(square):
        return square
    if not row_nums:
        return None
    while word_bit <= words_bitset:
        while word_bit & words_bitset == 0:
            word_bit <<= 1
            word_idx += 1
        square[row_nums[-1]] = sorted_words[word_idx]
        new_row, new_bitset = find_most_constrained_row_and_bitset(square, row_nums)
        if row_nums[-1] == 10:
            print("about to try a new initial word: " + sorted_words[word_idx])
        if len(row_nums) == 2:
            num_second_words_tried += 1
        if new_bitset:
            new_square = square.copy()
            new_row_nums = row_nums.copy()
            new_row_nums.append(new_row)
            new_bit = 1
            new_idx = 0
            while new_bit & new_bitset == 0:
                new_bit <<= 1
                new_idx += 1
            new_square[new_row] = sorted_words[new_idx]
            built_square = build_square(new_square, new_row_nums, new_idx, new_bit, new_bitset, num_second_words_tried)
            if built_square:
                return built_square
        #try the next word
        word_bit <<= 1
        word_idx += 1

build_square([""]*11, [10], 0, 1, all_words_bitset)


