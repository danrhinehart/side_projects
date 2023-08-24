#PART 0: ENSURE YOU DOWNLOAD THE SOWPODS.TXT FILE AND SAVE IT IN SAME DIRECTORY AS THIS FILE. 

#PART 1: DEFINING THE WORD SCORING FUNCTION WHICH IS CALLED IN OTHER FUNCTIONS
#note: this requires sowpods.txt to run

def score_word(word):
    """Calculates the score of a scrabble word and returns it."""
    final_score=0
    temp_word=word.lower()
    scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10, "*":0}
    for i in temp_word:
        final_score = final_score + scores[i]
    return final_score

#PART 2: DEFINES THE SCRABBLE FUNCTION WHICH TAKES IN LETTERS, CREATES POSSIBLE WORDS, SCORES EACH ON AND RETURNS SORTED LIST OF HIGHEST SCORING WORDS
#note: this requires the function (score_word) and sowpods.txt noted above.

def run_scrabble(input_word):
    """Calculates all possible words for a given scrabble rack and returns their list, score and total count."""
    #STEP0: CREATING INITIAL VARIABLES AND LISTS
    import time
    start_time = time.time()
    scrabble_word_list = []
    possible_word_list = []
    alpha_compare_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t",
                          "u","v","w","x","y","z","?","*"]
    scrabble_word = input_word.lower()
    scrabble_word_up = input_word.upper()
    error_mssg = ""
    scrabble_word_len = len(scrabble_word)
    wildcard_initial_counter = 0
    
    #STEP1: IMPORTING LIST OF ALL SCRABBLE WORDS. USES SOWPODS.TXT
    with open("sowpods.txt","r") as infile:
        raw_input = infile.readlines()
        data = [datum.strip('\n') for datum in raw_input]
    
    #STEP2: ERROR GENERATION
    #error for too few or too many characters
    if scrabble_word_len < 2 or scrabble_word_len > 7:
        error_mssg = "The characters you entered are too few or too many. Please enter between 2 and 7"
        return error_mssg
    for y in scrabble_word:
        #error for char not allowed
        if y not in alpha_compare_list:
            error_mssg = "You entered an integer or character which is not allowed"
            return error_mssg
        #error for too many wildcards
        if y == "?" or y =="*":
            wildcard_initial_counter = wildcard_initial_counter+1
            if wildcard_initial_counter >2:
                error_mssg = "You have too many wildcards. Please enter no more than 2"
                return error_mssg
    
    #STEP 3a: TRIM POSSIBLE WORD LIST TO ONLY SUBSET OF MAX LENGTH
    for z in data:
        if len(z) <= scrabble_word_len:
            scrabble_word_list.append(z)
    
    #STEP 3b: TRIM POSSIBLE WORD LIST TO ONLY THOSE POSSIBLE BASED ON RACK + WILDCARDS
    for x in scrabble_word_list:
        temp_counter=0
        for w in x:
            if w in scrabble_word_up:
                temp_counter=temp_counter+1
        #doing filtering to include all possible words based on wildcards; doesnt account for duplicates
        if (temp_counter+wildcard_initial_counter) >= len(x):
            possible_word_list.append(x)
        temp_counter=0
    
    #STEP 4: CREATE DICTIONARY FOR THE LIST WORD, RACK LETTERS AND COMPARE; ADD TO SUCCESS FAIL LISTS
    final_success_list =[]
    final_failure_list =[]
    rack_dict = {}
    list_dict = {}
    
    #create rack dictionary which remains constant
    for i in scrabble_word_up:
        if i not in rack_dict:
            rack_dict[i]=1
        else:
            rack_dict[i]=rack_dict[i]+1

    #iterating through word list to make dictionary and determine is valid word (dups / wildcards)
    for x in possible_word_list:
        #setting default values for use in every word
        temp_wildcard_counter = wildcard_initial_counter
        dup_delta = 0
        duplicate_risk = False
        wildcard_risk = False
        valid_word = True
        
        #create list word dictionary
        for i in x:
            if i not in list_dict:
                list_dict[i]=1
            else:
                list_dict[i]=list_dict[i]+1
        
        #compare dictionaries (listword vs rackword) to see where there is a wildcard and duplicate risk
        
        for y in list_dict:
            #handle case where letter not included due to wildcard or duplicate risk
            if y not in rack_dict:
                wildcard_risk = True
                #decrementing available wildcards to consume
                temp_wildcard_counter=temp_wildcard_counter-1
                if temp_wildcard_counter <0:
                    valid_word = False
            elif list_dict[y] > rack_dict[y]:
                duplicate_risk = True
                dup_delta = list_dict[y] - rack_dict[y]
                temp_wildcard_counter = temp_wildcard_counter - dup_delta
                if temp_wildcard_counter < 0:
                    valid_word = False
              
        #appending the word to the failure or success list based on outcome        
        if valid_word is True:
            final_success_list.append(x)
        else:
            final_failure_list.append(x)
        #clear list dictionary for next iteration
        list_dict={}
    final_success_word_count = len(final_success_list)
    
    #STEP5: SEND WORD TO SCORE FUNCTION (in above section of code) FOR FINAL SCORE & APPEND TO TUPLE
    import copy
    overall_success_list=[]
    
    for i in final_success_list:
        temp_final_success_list=[]
        temp_scoring_word_list=[]
        temp_scoring_word=""
        temp_incoming_score=0
        temp_rack_dict=copy.deepcopy(rack_dict)
        #doing the loop per letter to make sure we dont send duplicate letters for scoring
        for k in i:
            if k in scrabble_word_up:
                #decrement dict letter value
                temp_rack_dict[k]=temp_rack_dict[k]-1 
                if temp_rack_dict[k] >= 0:
                    temp_scoring_word_list.append(k)
            else:
                temp_scoring_word_list.append("*")        
        temp_scoring_word = "".join(temp_scoring_word_list)
        #sending scoring word to function
        temp_incoming_score = score_word(temp_scoring_word)
        temp_final_success_list.append(temp_incoming_score)
        temp_final_success_list.append(i)
        overall_success_list.append(tuple(temp_final_success_list))
    
    #STEP6: Sort final list
    
    import operator
    overall_success_list = sorted(overall_success_list, key = lambda y: (-y[0], y[1]))
    
    #STEP 7: CONFIRM Time and return final data object
    
    end_time=time.time()
    overall_time = end_time - start_time
    return (overall_success_list,final_success_word_count)


# * * * * * * TEST CASE: RUN THESE NEXT THREE LINES OF CODE TO CONFIRM THE ABOVE TWO FUNCTIONS WORD AS INTENDED (word_score, run_scrabble) * * * * * * * * * * *
#scrabble_rack_input=input("Enter Your Scrabble Letters. Use ? or * for wildcards: ")
#scrabble_scored_list = run_scrabble(scrabble_rack_input)
#print(scrabble_scored_list)
# * * * * * * END OF TEST CASE * * * * * * * * * * * * * * * * * * * * * ** * * * * * * * * * ** * * * * * * * * * ** * * * * * * * * * ** * * * * * * * * * * *


#PART 3: FUNCTION WHICH TAKES THE PRE-CREATED LIST OF WORDS AND LIMITS THEM TO A DISCRETE LENGTH (e.g. you only have 3 spaces to use for your word)
#note: this requires (score_word), (run_scrabble) and sowpods.txt to run

def char_limit_scrabble(input_list,char_max):
    """Takes the tuple of all possible word, along with their score and only keeps ones which maybe the char max"""
    #STEP1: gets list of all possible scrabble words
    max_char = char_max
    temp_list1 = input_list[0]
    temp_allowed_words = []
    final_allowed_words = []
    #final_adjusted_list = ()
    for i in temp_list1:
        temp_score = i[0]
        temp_word = i[1]
        if len(temp_word) <= max_char:
            temp_allowed_words.append(temp_score)
            temp_allowed_words.append(temp_word)
            final_allowed_words.append(temp_allowed_words)
            temp_allowed_words = []
            
    #STEP2: getting final count of allowed words
    final_allowed_words_count = len(final_allowed_words)
    final_adjusted_list=(final_allowed_words,final_allowed_words_count)
    
    #STEP3: returning final adjusted value
    return final_adjusted_list


# * * * * * * TEST CASE: RUN THESE NEXT EIGHT LINES OF CODE TO CONFIRM THE ABOVE FUNCTION WORKS AS INTENDED (char_limit_scrabble) * * * * * * * * * * *
#promting user for scrabble rack
#scrabble_rack_input=input("Enter Your Scrabble Letters: ")
#scrabble_scored_list = run_scrabble(scrabble_rack_input)
#prompting user for max characters to allow
#char_limit_input = input("Enter The Max Letter Count: ")
#char_limit = int(char_limit_input)
#temp_output = char_limit_scrabble(scrabble_scored_list,char_limit)
#print(temp_output)
# * * * * * * END OF TEST CASE * * * * * * * * * * * * * * * * * * * * * ** * * * * * * * * * ** * * * * * * * * * ** * * * * * * * * * ** * * * * * * 


#PART 4: THIS IS A FUNCTION WHICH DETERMINES IF A WORD EXISTS AND IF TRUE, RETURNS THE SCORE.
#note - this requires the (score_word) function above and sowpods.txt to run. 

def is_scrabble_word(search_word):
    var_search_word = search_word.upper()
    len_search_word = len(search_word)
    temp_word_population = []
    is_word_allowed = False
    search_word_score = 0
    final_search_output = []
    
    #STEP1: IMPORTING LIST OF ALL SCRABBLE WORDS
    with open("sowpods.txt","r") as infile:
        raw_input = infile.readlines()
        data = [datum.strip('\n') for datum in raw_input]
    
    #STEP2: doing first optimization to remove words that are longer than search word
    for i in data:
        if len(i) == len_search_word:
            temp_word_population.append(i)
    
    #STEP3: doing formal pass to find if the word exists
    for i in temp_word_population:
        if i == var_search_word:
            is_word_allowed = True
    
    #STEP4: getting word score if True        
    if is_word_allowed == True:
        search_word_score = score_word(search_word)
    
    #STEP5: Adding to list to return output
    final_search_output.append(var_search_word)
    final_search_output.append(is_word_allowed)
    final_search_output.append(search_word_score)
    
    return final_search_output


# * * * * * * TEST CASE: RUN THESE NEXT THREE LINES OF CODE TO DETERMINE IF THE FUNCTION WORKS AS INTENDED (is_scrabble_word) * * * * * * * * * * *
user_search_word = input("Enter The Word To Search: ")
temp_output = is_scrabble_word(user_search_word)
print(temp_output)
# * * * * * * END OF TEST CASE * * * * * * * * * * * * * * * * * * * * * ** * * * * * * * * * ** * * * * * * * * * ** * * * * * * * * * ** * * * * * * 