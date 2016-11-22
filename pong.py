import math
import numpy as np

# Markov Decision Process for Pong
# Components: state, actions, rewards, initial state, termination
# state - an array of [ball_x, ball_y, velocity_x, velocity_y, paddle_y]
# actions - a float in {0, +0.04, -0.04}
# rewards - 0 or +1 or -1
# initial state s0 = [0.5, 0.5, 0.03, 0.01, 0.4]

# global constant vairiables
BX = 0      
BY = 1
VX = 2
VY = 3
PY = 4
paddle_height = 0.2
paddle_x = 1
############ below are parameters to tune ######################
Ne = 30             # the min times the agent has to try each action-state pair
R_plus = 100        # an optimistic estimate of the best possible reward in any state 
C = 1               # the constant which dets learning rate alpha = C/(C+N(s,a))
gamma = 0.5         # discount factor


def terminal(s):
    off_paddle = (s[BY]<s[PY]) or (s[BY]>s[PY]+paddle_height)
    if (s[BX] > paddle_x) and off_paddle:    # ball_x > 1 and ball_y < paddle_y or ball_y > paddle_y+paddle_height
        print "terminal!"
        return True
    return False


def discretize_s(s):
    sd = [0 for i in range(5)]
    sd[BX] = int(12*s[BX])
    sd[BY] = int(12*s[BY])
    sd[VX] = int(np.sign(s[VX]))
    if abs(s[VY]) < 0.015:
        sd[VY] = 0
    else:
        sd[VY] = int(np.sign(s[VY]))
    sd[PY] = int(12*s[PY]/(1-paddle_height))
    
    return sd

def discretize_a(a):    # map 0,0.04,-0.04 to 0,1,2
    if a==0:
        return 0
    elif a==0.04:
        return 1
    else:
        return 2

def exploration(u, n):
    if n < Ne:
        return R_plus 
    else:
        return u

def bounce(s):      # s accessed by [ball_x][ball_y][v_x][v_y][paddle_y][action]
    # If ball_y < 0 (the ball is off the top of the screen), assign ball_y = -ball_y and velocity_y = -velocity_y.
    if s[BY] < 0:
        print "bounce down"
        s[BY] = -s[BY]
        s[VY] = -s[VY]
    # If ball_y > 1 (the ball is off the bottom of the screen), let ball_y = 2 - ball_y and velocity_y = -velocity_y.
    if s[BY] > 1:
        print "bounce up"
        s[BY] = 2-s[BY]
        s[VY] = -s[VY]
    # If ball_x < 0 (the ball is off the left edge of the screen), assign ball_x = -ball_x and velocity_x = -velocity_x.
    if s[BX] < 0:
        print "bounce to right"
        s[BX] = -s[BX]
        s[VX] = -s[VX]
    # If ball can bounce on paddle
    if (s[BX] >= paddle_x) and (s[BY]>=s[PY]) and (s[BY]<=s[PY]+paddle_height):
        print "bounce on paddle!"
        s[BX] = 2*paddle_x - s[BX]
        # this loop makes sure |vx| > 0.03
        while True:
            new_vx = np.random.uniform(-0.015,0.015) - s[VX]
            if abs(new_vx) > 0.03: 
                s[VX] = new_vx
                s[VY] = s[VY] + np.random.uniform(-0.03,0.03)
                break
        return 1
    return 0


def Q_learning_agent(cs, cr, Q, N_sa, s, a, r):
    """The Q-learning algorithm
    @param cs: current state
    @param cr: current reward
    @param Q: a table of action values indexed by state and action, initially 0s
    @param N_sa: a table of frequencies for state-action pairs, initially 0s
    @param s, a, r: the previous state, action, and reward, initially null
    """
    #if terminal(s):
        #Q[s0][s1][s2][s3][s4][0] = cr
        #return -1


    # params which start with d means discritized 
    actions = [0,+0.04,-0.04]

    dcs = discretize_s(cs)
    cs0, cs1, cs2, cs3, cs4 = dcs
    Q_cs = Q[cs0][cs1][cs2][cs3][cs4]   # an array of action vals resulted from three actions
    N_sa_cs = N_sa[cs0][cs1][cs2][cs3][cs4]  # an array of frequencies resulted from three actions

    ds = discretize_s(s)
    s0, s1, s2, s3, s4 = ds
    s5 = discretize_a(a)

    alpha = C/(C+N_sa[s0][s1][s2][s3][s4][s5])

    if s != None:
        N_sa[s0][s1][s2][s3][s4][s5] += 1
        max_ca = actions[Q_cs.index(max(Q_cs))] 
        Q[s0][s1][s2][s3][s4][s5] += alpha*N_sa[s0][s1][s2][s3][s4][s5]*(r + gamma*max_ca - Q[s0][s1][s2][s3][s4][s5])
        for si in range(5):
            s[si] = cs[si]
        explorations = [exploration(Q_cs[i], N_sa_cs[i]) for i in range(3)]
        a = actions[explorations.index(max(explorations))]    # argmax a' f(Q[s',a'], N_sa[s',a'])
        #r = cr
    return cr, a


if __name__ == '__main__':
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
    while True:
        # increment ball_x by v_x and ball_y by v_y
        cs[0] += cs[2]
        cs[1] += cs[3]
        cs[4] += a

        # bounce if possible
        if bounce(cs)==1:
            cr += 1

        # do a terminal + reward check
        if terminal(cs):
            cr -= 1
            cs = [0.5, 0.5, 0.03, 0.01, 0.4]
            s = [0.5, 0.5, 0.03, 0.01, 0.4]
            #break

        # do q-learning
        r, a = Q_learning_agent(cs, cr, Q, N_sa, s, a, r)
        

        t += 1
