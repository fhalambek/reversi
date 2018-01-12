import random

weight = [[99, -8,  8,  6,  6,  8, -8, 99],
          [-8,-24, -4, -3, -3, -4,-24, -8],
          [ 8, -4,  7,  4,  4,  7, -4,  8],
          [ 6, -3,  4,  0,  0,  4, -3,  6],
          [ 6, -3,  4,  0,  0,  4, -3,  6],
          [ 8, -4,  7,  4,  4,  7, -4,  8],
          [-8,-24, -4, -3, -3, -4,-24, -8],
          [99, -8,  8,  6,  6,  8, -8, 99]]

def easy(field, possible, color, opp_color):
    
    return(random.choice(possible))

def greedy(field, possible, color, opp_color):
    
    cntmax = 0
    delta_x = [-1, -1,  0,  1,  1,  1,  0, -1]
    delta_y = [ 0,  1,  1,  1,  0, -1, -1, -1]
    bestpos = possible[0]
    
    for position in range(len(possible)):

        counter = 0
        pos_x = possible[position][0]
        pos_y = possible[position][1]
        
        for direction in range(8):

            dir_counter = 0
            legit = True
            current_x = pos_x + delta_x[ direction ]
            current_y = pos_y + delta_y[ direction ]
            
            while(True):
                if(current_x < 0 or current_x > 7 or current_y < 0 or current_y > 7):
                    legit = False
                    break
                
                if(field[ current_x ][ current_y] == color):
                    break

                if(field[ current_x ][ current_y] != color):
                    legit = False
                    break
                    
                if(field[ current_x ][ current_y] == opp_color):
                    dir_counter += 1

                current_x += delta_x[direction]
                current_y += delta_y[direction]

            
            if(legit == True):
                counter += dir_counter

        if(counter > cntmax):
            cntmax = counter
            bestpos = possible[position]
            
    return(bestpos)


def weighted(field, possible, color, opp_color):
    
    maxweight = 0
    bestpos = (possible[0])
    
    for i in range(len(possible)):
        pos_x = possible[i][0]
        pos_y = possible[i][1]
        if(weight[pos_x][pos_y] > maxweight):
            maxweight = weight[pos_x][pos_y]
            bestpos = possible[i]

    return(bestpos)
            

        
