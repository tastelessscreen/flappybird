import curses
from  curses.textpad import rectangle
import time 
import random


MARGIN= 3
GAP_WIDTH = 7
INTER_GAP= 20
BIRD= "@ "
HEART="<3"
PIPE_COLOR = 1
FLAPPYCOLOR =2
LIVES = 3
FRAMES = 25  
GRAVITY = 0.18         
FLAP_VELOCITY = -1.1    
MAX_FALL_SPEED = 1.2    
START_DELAY = 100       
MIN_DELAY = 50       
 
HEART_COLOR = 3
 
FLAP = (curses.KEY_UP, ord(" "))
QUIT = (ord("q"), ord("Q"), 27)  # q or Esc
PAUSE = (ord("p"), ord("P"))






def draw_centered(scr, y,text, attr=0):
   
   _, WIDTH =scr.getmaxyx()
   x = max(0, (WIDTH -len(text))//2)
   scr.addstr(y, x , text ,attr)



def menu(scr, title, lines, accept_keys):
    
    HEIGHT, _ = scr.getmaxyx()
    scr.timeout(-1)        
    scr.erase()
    top = max(0, HEIGHT // 2 - (len(lines) + 2) // 2)
    draw_centered(scr, top, title, curses.A_BOLD)
    for i, line in enumerate(lines):
        draw_centered(scr, top + 2 + i, line)
    scr.refresh()
    curses.flushinp()      
    while True:
        key = scr.getch()
        if key in accept_keys:
            return True
        if key in QUIT:
            return False



def pause_screen(scr):
    HEIGHT, _ = scr.getmaxyx()
    draw_centered(scr, HEIGHT // 2, "  PAUSED - press P to resume, Q to quit  ",  curses.A_REVERSE)
    scr.refresh()
    scr.timeout(-1)
    while True:
        key = scr.getch()
        if key in PAUSE:
            return True
        if key in QUIT:
            return False



def  play_game(scr):
      
      HEIGHT, WIDTH = scr.getmaxyx()
 
      delay = START_DELAY
      scr.timeout(delay)
 
    
      pipes = []
      x = WIDTH // 2
      while x < WIDTH - MARGIN:
        gap_start = random.randint(MARGIN + 1, HEIGHT - MARGIN - GAP_WIDTH)
        pipes.append((x, gap_start))
        x += INTER_GAP
 
      flap_x = WIDTH // 4
      flap_y = float(HEIGHT // 2)  
      velocity = 0.0
 
      score = 0
      lives = LIVES
      invincible = 0
 
      while True:
       
        scr.erase()
        rectangle(scr, MARGIN, MARGIN, HEIGHT - MARGIN, WIDTH - MARGIN)
 
        draw_centered(scr, 1, f"SCORE: {score}")
 
        scr.addstr(1, MARGIN, "LIVES: ")
        scr.attron(curses.color_pair(HEART_COLOR))
        scr.addstr(" ".join([HEART] * lives))
        scr.attroff(curses.color_pair(HEART_COLOR))
 
        scr.addstr(1, WIDTH - MARGIN - 9, "P = pause")
 
        scr.attron(curses.color_pair(PIPE_COLOR))
        for px, gap_start in pipes:
            if MARGIN < px < WIDTH - MARGIN:
                for y in range(MARGIN + 1, HEIGHT - MARGIN):
                    if not (gap_start <= y < gap_start + GAP_WIDTH):
                        scr.addstr(y, px, "|")
        scr.attroff(curses.color_pair(PIPE_COLOR))
 
        bird_y = int(round(flap_y))
      
        if invincible == 0 or (invincible // 2) % 2 == 0:
            scr.attron(curses.color_pair(FLAPPYCOLOR))
            scr.addstr(bird_y, flap_x, BIRD)
            scr.attroff(curses.color_pair(FLAPPYCOLOR))
        scr.refresh()
 
        
        key = scr.getch()
 
        if key in QUIT:
            return None
        if key in PAUSE:
            if not pause_screen(scr):
                return None
            scr.timeout(delay)
            curses.flushinp()
            continue
        if key in FLAP:
            velocity = FLAP_VELOCITY
 
        velocity = min(velocity + GRAVITY, MAX_FALL_SPEED)
        flap_y += velocity
        bird_y = int(round(flap_y))
 
        if invincible > 0:
            invincible -= 1
 
    
        pipes = [(px - 1, g) for px, g in pipes if px - 1 > MARGIN]
        if not pipes or pipes[-1][0] <= WIDTH - MARGIN - 1 - INTER_GAP:
            gap_start = random.randint(MARGIN + 1, HEIGHT - MARGIN - GAP_WIDTH)
            pipes.append((WIDTH - MARGIN - 1, gap_start))
            delay = max(MIN_DELAY, delay - 2)  
 
   
        hit = False
 
        
        if bird_y <= MARGIN or bird_y >= HEIGHT - MARGIN:
            if invincible > 0:
               
                bird_y = min(max(bird_y, MARGIN + 1), HEIGHT - MARGIN - 1)
                flap_y = float(bird_y)
                velocity = 0.0
            else:
                hit = True
                flap_y = float(HEIGHT // 2)   
                velocity = 0.0
 
      
        for px, gap_start in pipes:
            if px == flap_x:
                if gap_start <= bird_y < gap_start + GAP_WIDTH:
                    score += 1                 # flew through the gap
                else:
                    if invincible == 0:
                      hit = True
                    flap_y = float(gap_start + GAP_WIDTH // 2)
                    velocity = 0.0
 
        
        if hit:
            lives -= 1
            invincible = FRAMES
            if lives <= 0:
                return score
 

def main(scr):
    curses.curs_set(0)
    scr.nodelay(1)


    curses.init_pair(PIPE_COLOR, curses.COLOR_GREEN , curses.COLOR_GREEN)
    curses.init_pair(FLAPPYCOLOR, curses.COLOR_RED , curses.COLOR_BLACK)
    curses.init_pair(HEART_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)


    if not menu(scr, "F L A P P Y" ,
                ["UP / SPACE = flap     P = pause",
                 "",
                 "Press SPACE to play",
                 "Press Q to quit"],
                (ord(" "),)):
        return
    

   
    while True:
       score =play_game(scr)
       if score is None:
          break
       again = menu(scr, "GAME OVER",
                   [f"Score: {score}",
                     "",
                    "Press R to restart",
                    "Press Q to quit"],
                (ord("r"), ord("R")))
       if not again :
          break


       
curses.wrapper(main)