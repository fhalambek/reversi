import random


def easy(field, possible, color):
    return(random.choice(possible))

def greedy(field, possible, color, opp_color):

    cntmax = 0
    delta_x = [-1, -1,  0,  1,  1,  1,  0, -1]
    delta_y = [ 0,  1,  1,  1,  0, -1, -1, -1]
    
    for position in range(possible.size()):

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
