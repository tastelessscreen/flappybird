import curses
from  curses.textpad import rectangle
import time 
import random



def main(scr):
    curses.curs_set(0)
    scr.nodelay(1)


    HEIGHT, WIDTH= scr.getmaxyx()
    MARGIN= 3
    GAP_WIDTH = 7
    INTER_GAP= 20
    BIRD= "@ "
    PIPE_COLOR = 1
    FLAPPYCOLOR =2


    curses.init_pair(PIPE_COLOR, curses.COLOR_GREEN , curses.COLOR_BLACK)
    curses.init_pair(FLAPPYCOLOR, curses.COLOR_RED , curses.COLOR_BLACK)

    gamedifficulty= 200
    scr.timeout(gamedifficulty)

    

    pipe=[]
    x =  WIDTH//2
    while x < WIDTH - MARGIN:
        gap_start = random.randint(MARGIN +1 , HEIGHT- MARGIN -GAP_WIDTH)
        pipe.append((x, gap_start))
        x +=INTER_GAP
        
    flap_y, flap_x  = HEIGHT//2 , WIDTH//4
    score_text= 'SCORE: {}'
    score= 0

    loop_cntr = 0

    while True:
        scr.erase()
        rectangle(scr, MARGIN, MARGIN ,HEIGHT-MARGIN, WIDTH- MARGIN) 


        game_text = score_text.format(score)
        game_text_y, game_text_x = 1 , (WIDTH  - len(game_text))//2
        scr.addstr(game_text_y , game_text_x , game_text)


   
        if loop_cntr == INTER_GAP:
           gap_start = random.randint(MARGIN +1 , HEIGHT- MARGIN -GAP_WIDTH)
           pipe.append((pipe[-1][0] + INTER_GAP, gap_start))
           loop_cntr =0
           gamedifficulty= max(1, gamedifficulty -5)
           scr.timeout(gamedifficulty)


        obstructions = set()

        for x , gap_start in pipe:
          if flap_x == x:
             score += 1
          for y in range(MARGIN +1 , HEIGHT-MARGIN):
            if y not in range (gap_start , gap_start+ GAP_WIDTH ):
                scr.attron(curses.color_pair(PIPE_COLOR))
                scr.addstr(y , x, '|')
                scr.attroff(curses.color_pair(PIPE_COLOR))
                obstructions.add((y,x))
        pipe =[(x-1, gap_start) for x, gap_start in pipe if x > MARGIN]
        
                        

        scr.attron(curses.color_pair(FLAPPYCOLOR))
        scr.addstr(flap_y , flap_x, BIRD)
        scr.attroff(curses.color_pair(FLAPPYCOLOR))
        scr.refresh()
        
        key = scr.getch()

        
        if flap_y in [MARGIN, HEIGHT - MARGIN] or \
            (flap_y, flap_x) in obstructions:
            if (flap_y , flap_x) in obstructions:
               score -= 1 
            game_text= f'GAME OVER .Score:{score}'
            game_text_y, game_text_x= 1, (WIDTH- len(game_text))//2
            scr.move(1, 0)
            scr.clrtoeol()

            scr.addstr(game_text_y, game_text_x, game_text)
            scr.refresh()
            curses.flushinp()
            scr.timeout(-1)
            scr.getch()
            break



        if key== 27: # esc change it to q
           break
        scr.addstr(flap_y, flap_x, ' ')
        if key== curses.KEY_UP:
           flap_y -= 1
        else:
           flap_y+= 1

        loop_cntr += 1


curses.wrapper(main)