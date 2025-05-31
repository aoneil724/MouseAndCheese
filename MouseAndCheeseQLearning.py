import numpy as np
import random
import csv

# Mouses starting reward values for each position
def Run_mouse():
    results = []
    with open("output.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
        for row in reader: # each row is a list
            results.append(row)
    mouse_memory = np.array(results)

    if mouse_memory.shape != (8, 8):
        mouse_memory = np.zeros([8,8], dtype = float)
    # Starting Parameters
    grid = np.zeros([8,8], dtype=float)
    mouse_start_pos = [0,0]
    # Location of Cats
    cat_location = np.array([[1,1], [1,3], [1,5], [1,6], [1,7], [2,0], [2,5], [3,1], [3,3], [3,4], [3,5], [4,4],[5,4], [6,4], [6,6], [7,6]])
    for x,y in cat_location:
        grid[x,y] = 1

    squares_occupied = []

    Mouse_is_Alive = True
    mouse_pos = mouse_start_pos
    while Mouse_is_Alive == True:
        at_top_wall = False
        at_bottom_wall = False
        at_right_wall = False
        at_left_wall = False
        if mouse_pos[0] == 0:
            at_top_wall = True
        if mouse_pos[0] == 7:
            at_bottom_wall = True
        if mouse_pos[1] == 0:
            at_left_wall = True
        if mouse_pos[1] == 7:
            at_right_wall = True
        if at_top_wall != True:
            top_prob = mouse_memory[mouse_pos[0]-1, mouse_pos[1]]
            exp_prob_top = np.exp(top_prob)
        elif at_top_wall == True:
            exp_prob_top = 0
        if at_bottom_wall != True:
            bot_prob = mouse_memory[mouse_pos[0]+1, mouse_pos[1]]
            exp_prob_bot = np.exp(bot_prob)
        elif at_bottom_wall == True:
            exp_prob_bot = 0
        if at_left_wall != True:
            left_prob = mouse_memory[mouse_pos[0], mouse_pos[1]-1]
            exp_prob_left = np.exp(left_prob)
        elif at_left_wall == True:
            exp_prob_left = 0
        if at_right_wall != True:
            right_prob = mouse_memory[mouse_pos[0], mouse_pos[1]+1]
            exp_prob_right = np.exp(right_prob)
        elif at_right_wall == True:
            exp_prob_right = 0

        top_weight = exp_prob_top / (np.sum([exp_prob_top, exp_prob_bot, exp_prob_left, exp_prob_right]))
        bot_weight = exp_prob_bot / (np.sum([exp_prob_top, exp_prob_bot, exp_prob_left, exp_prob_right]))
        left_weight = exp_prob_left / (np.sum([exp_prob_top, exp_prob_bot, exp_prob_left, exp_prob_right]))
        right_weight = exp_prob_right / (np.sum([exp_prob_top, exp_prob_bot, exp_prob_left, exp_prob_right]))
        options = ['top', 'bot', 'left', 'right']
        randomChoice = random.choices(options, weights = (top_weight, bot_weight, left_weight, right_weight))
        print(randomChoice[0])
        match randomChoice[0]:
            case 'top':
                mouse_pos = [mouse_pos[0]-1, mouse_pos[1]]
            case 'bot':
                mouse_pos = [mouse_pos[0]+1, mouse_pos[1]]
                
            case 'left':
                mouse_pos = [mouse_pos[0], mouse_pos[1]-1]
            case 'right':
                mouse_pos = [mouse_pos[0], mouse_pos[1]+1]
            case _:
                pass
        print(mouse_pos)
        squares_occupied.append(mouse_pos)
        for x,y in cat_location:
            
            if mouse_pos[0] == cat_location[y][0] and mouse_pos[1] == cat_location[y][1]:
                Mouse_is_Alive = False
                print('dead as hell')
                Mouse_Won = False
        if mouse_pos == [7,7]:
            print('He won!')
            Mouse_Won = True
            Mouse_is_Alive = False
            
    unique_squares_occupied = []
    for x in squares_occupied:
        if x not in unique_squares_occupied:
            unique_squares_occupied.append(x)
    for x in unique_squares_occupied:
        print(f'test {x}')
        print(mouse_memory[x[0], x[1]])
        if Mouse_Won == False:
            mouse_memory[x[0], x[1]] += -0.1
        if Mouse_Won == True:
            mouse_memory[x[0], x[1]] += 0.7

    print(mouse_memory)

    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(mouse_memory)
    return Mouse_Won
times_won = 0
times_lost = 0
for x in range(500):
    a = Run_mouse()
    if a == True:
        times_won +=1
    if a == False:
        times_lost +=1
print(f'times won {times_won}')
print(f'times lost {times_lost}')