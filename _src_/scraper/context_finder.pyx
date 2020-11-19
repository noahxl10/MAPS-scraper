def context_finder(str pagetext, int set_index):
    cdef int desired_sentences, num, index, period_count, top_index, bottom_index

    desired_sentences = 2

    num = desired_sentences + 1

    index = set_index
    period_count = 0

    while period_count != num:
        
        if pagetext[index] == '.':
                period_count+=1
        index +=1
        if index >= len(pagetext):
            period_count = num
    top_index = index   

    


    period_count = 0
    index = set_index
    while period_count != num:
    
        if pagetext[index] == '.':
                period_count+=1
        index -=1
        if index <= 0:
            period_count = num

    bottom_index = index



    context_string = pagetext[bottom_index:top_index]
    return context_string
