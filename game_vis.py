import pygame, sys
from pygame.locals import *
import pong
import pickle
import time

# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 200

#Global Variables to be used through our program
WINDOWWIDTH = 12*50
WINDOWHEIGHT = 12*50
LINETHICKNESS = 10
PADDLESIZE = 0.2*WINDOWHEIGHT
BASICFONTSIZE = 20


# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)
RED = (255, 0, 0)


BX = 0
BY = 1
VX = 2
VY = 3
PY = 4

C = 59.0               # the constant which dets learning rate alpha = C/(C+N(s,a))
gamma = 0.8             # discount factor

#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT:
        paddle.bottom = WINDOWHEIGHT
    #Stops paddle moving too high
    elif paddle.top < 0:
        paddle.top = 0
    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)
  
#draws the ball
def drawBall(ball):
    pygame.draw.circle(DISPLAYSURF, RED, ball, LINETHICKNESS/2)

def movePaddle(paddle, newx, newy):
    paddle.x = newx
    paddle.y = newy
    return paddle

def displayInfo(t, max_bounces, game):
    resultSurf = BASICFONT.render('Time = %ss, Max = %s, Game = %s' %(t, max_bounces, game), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (5, 5)
    DISPLAYSURF.blit(resultSurf, resultRect)

#Main function
def main():
    pygame.init()
    global DISPLAYSURF
    global BASICFONT
    BASICFONT = pygame.font.Font('FreeSansBold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) 
    pygame.display.set_caption('Pong')


    # initialize Q & N_sa, access by ((b_x,b_y,v_x,v_y,p_y),action), state is discretized
    Q_sa = {}
    N_sa = {}
    game = 0    #number of games played so far
    max_bounces = 0 # max number of consec paddle bounces so far

# load in model, already trained with 100K games
    with open('Q_sa100000_dict.pkl', 'rb') as f:
        Q_sa = pickle.load(f)
    with open('N_sa100000_dict.pkl', 'rb') as f:
        N_sa = pickle.load(f)

# run 1000 games with trained model and output average bounces per game
    test_games = 1000.0
    bounces_sum = 0.0
    bounces10_sum = 0.0
    t = 0    
    while game < test_games:
        if game%10 == 0:
            print 'game:', game
            print 'avg_bounces of last 10 games:', bounces10_sum/10.0
            bounces10_sum = 0


        current_s = [0.5, 0.5, 0.03, 0.01, 0.4]        # current state 

        #Initiate variable and set starting positions
        ballX = current_s[BX]*WINDOWHEIGHT
        ballY = current_s[BY]*WINDOWHEIGHT
        paddle_y = current_s[PY]*WINDOWHEIGHT

        #Creates Rectangles for ball and paddles.
        paddle = pygame.Rect(WINDOWWIDTH - LINETHICKNESS, paddle_y, LINETHICKNESS, PADDLESIZE)
        ball = (int(ballX), int(ballY))
        drawPaddle(paddle)
        drawBall(ball)
        
        current_bounces = 0   # number of consecutive on paddle bounces
        game_flag = True #game continues?
        while game_flag:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            ballX = current_s[BX]*WINDOWWIDTH
            ballY = current_s[BY]*WINDOWHEIGHT
            new_PY = current_s[PY]*WINDOWHEIGHT

            # update positions
            paddle = movePaddle(paddle, WINDOWWIDTH - LINETHICKNESS, new_PY)
            ball = (int(ballX), int(ballY))

            drawPaddle(paddle)
            drawBall(ball)        
            displayInfo(t, max_bounces, game)
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            DISPLAYSURF.fill(BLACK)
#####################################################################################
            #decide action
            action = pong.pick_action(current_s, Q_sa, N_sa)
            # save key for update Q for current state
            current_sa = (pong.discretize_s(current_s), action)
            #try action on current state, find next state
            next_s, current_r = pong.next_state(current_s, action)


            #next state is terminal state, current_r is -1
            if next_s is None:
                game_flag = False
                bounces_sum += current_bounces
                bounces10_sum += current_bounces
                current_bounces = 0
                game += 1
            
            if current_sa not in N_sa:
                N_sa[current_sa] = 1
                alpha = C / (C + N_sa[current_sa])
                Q_sa[current_sa] = alpha * (current_r + gamma * pong.get_maxQ(next_s, Q_sa)) #update Q for current state

            else:
                N_sa[current_sa] += 1
                alpha = C / (C + N_sa[current_sa])
                Q_sa[current_sa] += alpha * (current_r + gamma * pong.get_maxQ(next_s, Q_sa) - Q_sa[current_sa] )

            # calculate bounces
            if current_r == 1:
                current_bounces += 1
            max_bounces = max(max_bounces, current_bounces)

            t += 1

    print 'avg_bounces of 1000 games:', bounces_sum/test_games



if __name__=='__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

