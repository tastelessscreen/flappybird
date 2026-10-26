import curses
from  curses.textpad import rectangle
import time 
import random



def main(scr):
    curses.curs_set(0)
    scr.timeout(150)


    height,width = scr.getmaxyx()

    MARGIN= 3
    GAP_WIDTH = 7
    INTER_GAP= 20

    pipe=[]
    x =  width//2
    while x < width-MARGIN:
        gap_start = random.randint(MARGIN +1 , height- MARGIN -GAP_WIDTH)
        pipe.append((x, gap_start))
        x +=INTER_GAP
        
    rectangle(scr, MARGIN, MARGIN ,height-MARGIN, width- MARGIN)

    flap_bird='@'

    flap_y, flap_x  = height//2 , width//4

    loop_cntr = 0

    while True:
        if loop_cntr == INTER_GAP:
           gap_start = random.randint(MARGIN +1 , height- MARGIN -GAP_WIDTH)
           pipe.append((pipe[-1][0] + INTER_GAP, gap_start))
           loop_cntr =0


        obstructions = set()

        for x , gap_start in pipe:
          for y in range(MARGIN +1 , height-MARGIN):
            if y not in range (gap_start , gap_start+ GAP_WIDTH ):
                scr.addstr(y , x, '| ')
                obstructions.add((y,x))
        pipe =[(x-1, gap_start) for x, gap_start in pipe if x > MARGIN]
        
                        

       
        scr.addstr(flap_y , flap_x, flap_bird)
        scr.refresh()
        key = scr.getch() 
        if flap_y in [MARGIN, height-MARGIN] or \
            (flap_y, flap_x) in obstructions:
            game_text= 'GAME OVER'
            game_text_y, game_text_x= 1, (width- len(game_text))//2
            scr.addstr(game_text_y, game_text_x , game_text)
            scr.refresh()
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