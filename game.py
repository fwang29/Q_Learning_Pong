import pygame, sys
from pygame.locals import *
import pong

# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 50

#Global Variables to be used through our program
WINDOWWIDTH = 12*50
WINDOWHEIGHT = 12*50
LINETHICKNESS = 10
PADDLESIZE = 0.2*WINDOWHEIGHT

# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)
  
#draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

def moveBall(ball, newx, newy):
    ball.x = newx
    ball.y = newy
    return ball

def movePaddle(paddle, newx, newy):
    paddle.x = newx
    paddle.y = newy
    return paddle

#Main function
def main():
    # initialize Q,N_sa values to 0, access by [ball_x][ball_y][v_x][v_y][paddle_y][action], indexes are discretized
    Q = [[[[[[0 for x5 in xrange(3)]for x4 in xrange(12)]for x3 in xrange(3)]for x2 in xrange(2)]for x1 in xrange(12)]for x0 in xrange(12)]
    
    N_sa = [[[[[[0 for x5 in xrange(3)]for x4 in xrange(12)]for x3 in xrange(3)]for x2 in xrange(2)]for x1 in xrange(12)]for x0 in xrange(12)] 

    s = [0.5, 0.5, 0.03, 0.01, 0.4]        # initial state 
    a = 0
    r = 0

    cs = [0.5, 0.5, 0.03, 0.01, 0.4]        # initial state 
    cr = 0

    # simulate the env at each time step
    t = 0


    pygame.init()
    global DISPLAYSURF

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) 
    pygame.display.set_caption('Pong')

    #Initiate variable and set starting positions
    #any future changes made within rectangles
    ballX = s[0]*WINDOWHEIGHT - LINETHICKNESS/2
    ballY = s[1]*WINDOWHEIGHT - LINETHICKNESS/2
    playerOnePosition = s[4]*WINDOWHEIGHT - LINETHICKNESS/2

    #Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(WINDOWWIDTH - LINETHICKNESS, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    drawPaddle(paddle1)
    drawBall(ball)

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        ballX = s[0]*WINDOWHEIGHT - LINETHICKNESS/2
        ballY = s[1]*WINDOWHEIGHT - LINETHICKNESS/2
        playerOnePosition = s[4]*WINDOWHEIGHT - LINETHICKNESS/2
 
        drawPaddle(paddle1)
        drawBall(ball)        

        paddle1 = movePaddle(paddle1, WINDOWWIDTH - LINETHICKNESS, playerOnePosition)
        ball = moveBall(ball, ballX, ballY)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        DISPLAYSURF.fill(BLACK)

        cs[0] += cs[2]
        cs[1] += cs[3]
        cs[4] += a

        # bounce if possible
        if pong.bounce(cs)==1:
            cr += 1

        # do a terminal + reward check
        if pong.terminal(cs):
            cr -= 1
            cs = [0.5, 0.5, 0.03, 0.01, 0.4]
            s = [0.5, 0.5, 0.03, 0.01, 0.4]
            #break

        # do q-learning
        r, a = pong.Q_learning_agent(cs, cr, Q, N_sa, s, a, r)

        print cr, r
        print cs, s
        print a
        t += 1



if __name__=='__main__':
    main()

'''
        irint 
        cs[0] += cs[2]
        cs[1] += cs[3]

        # bounce if possible
        if pong.bounce(cs)==1:
            cr += 1

        # do a terminal + reward check
        if pong.terminal(cs):
            cr -= 1
            cs = [0.5, 0.5, 0.03, 0.01, 0.4]
            s = [0.5, 0.5, 0.03, 0.01, 0.4]
            #break

        # do q-learning
        if pong.Q_learning_agent(cs, cr, Q, N_sa, s, a, r):
            break
        print s

        t += 1
'''
