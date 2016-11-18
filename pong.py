import math
import numpy as np

# Markov Decision Process for Pong
# Components: state, actions, rewards, initial state, termination
# state - an array of [ball_x, ball_y, velocity_x, velocity_y, paddle_y]
# actions - a float in {0, +0.04, -0.04}
# rewards - 0 or +1 or -1
# initial state s0 = [0.5, 0.5, 0.03, 0.01, 0.4]

# global vairiables
paddle_height = 0.2
Ne = 20             # the min times the agent has to try each action-state pair
R_plus = 100        # an optimistic estimate of the best possible reward in any state 

def terminal(s):
    if s[0] > 1:    # ball_x > 1
        return True
    return False

def discretize_s(s):
    sd = [0 for i in range(5)]
    sd[0] = math.floor(s[0])
    sd[1] = math.floor(s[1])
    sd[2] = np.sign(s[2])
    if abs(s[3]) < 0.015:
        sd[3] = 0
    else:
        sd[3] = np.sign(s[3])
    sd[4] = math.floor(12*s[4]/(1-paddle_height))
    
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

def Q_learning_agent(cs, cr, Q, N_sa, s, a, r):
    """The Q-learning algorithm
    @param cs: current state
    @param cr: current reward
    @param Q: a table of action values indexed by state and action, initially 0s
    @param N_sa: a table of frequencies for state-action pairs, initially 0s
    @param s, a, r: the previous state, action, and reward, initially null
    """
    alpha = 1
    gamma = 1
    actions = [0,+0.04,-0.04]
    dcs = discretize_s(cs)
    cs0, cs1, cs2, cs4 = dcs
    Q_cs = Q[cs0][cs1][cs2][cs3][cs4]   # an array of action vals resulted from three actions
    N_sa_cs = N_sa[cs0][cs1][cs2][cs3][cs4]  # an array of frequencies resulted from three actions
    ds = discretize_s(s)
    s0, s1, s2, s3, s4 = ds
    s5 = discretize_a(a)

    if terminal(s):
        Q[s0][s1][s2][s3][s4][0] = cr
    if s != None:
        N_sa[s0][s1][s2][s3][s4][s5] += 1
        max_ca = actions[Q_cs.indexof(max(Q_cs))] 
        Q[s0][s1][s2][s3][s4][s5] += alpha*N_sa[s0][s1][s2][s3][s4][s5]*(r + gamma*max_ca - Q[s0][s1][s2][s3][s4][s5])
        s = cs
        explorations = [exploration(Q_cs[i], N_sa_cs[i]) for i in range(3)]
        a = actions[explorations.indexof(max(explorations))]    # argmax a' f(Q[s',a'], N_sa[s',a'])
        r = cr
    return a


if __name__ == '__main__':
    # initialize Q,N_sa values to 0, access by [ball_x][ball_y][v_x][v_y][paddle_y][action], indexes are discretized
    Q = [[[[[[0 for x5 in xrange(3)]for x4 in xrange(12)]for x3 in xrange(3)]for x2 in xrange(2)]for x1 in xrange(12)]for x0 in xrange(12)]
    
    N_sa = [[[[[[0 for x5 in xrange(3)]for x4 in xrange(12)]for x3 in xrange(3)]for x2 in xrange(2)]for x1 in xrange(12)]for x0 in xrange(12)] 

   s,a,r,cs,cr = None, None, None, None, None



