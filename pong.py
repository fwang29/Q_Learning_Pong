import math
import numpy as np
import sys

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
Ne = 10             # the min times the agent has to try each action-state pair
R_plus = 1        # an optimistic estimate of the best possible reward in any state 
C = 59               # the constant which dets learning rate alpha = C/(C+N(s,a))
gamma = 0.8         # discount factor


actions = [0, 0.04, -0.04]
rewards = [0. -1, 1]


def discretize_s(s):
    ball_x = min(int(12*s[BX]),11)
    ball_y = min(int(12*s[BY]), 11)
    velocity_x = int(np.sign(s[VX]))
    if abs(s[VY]) < 0.015:
        velocity_y = 0
    else:
        velocity_y = int(np.sign(s[VY]))
    paddle_y = min(int(12*s[PY]/(1-paddle_height)), 11)
    
    return (ball_x, ball_y, velocity_x, velocity_y, paddle_y)


def pick_action(state, Q, N_sa):
    best_action = None
    max_Q = -sys.maxint
    for action in actions:
        key = (discretize_s(state), action)
        if (key not in Q) or (key not in N_sa) or (N_sa[key] < Ne):
            return action
        if Q[key] > max_Q:
            max_Q = Q[key]
            best_action = action
    return best_action


#try action on current state, return (next state, reward for current state)
def next_state(state, action):
    state[BX] += state[VX]
    state[BY] += state[VY]
    state[PY] += action
# If ball_y < 0 (the ball is off the top of the screen), assign ball_y = -ball_y and velocity_y = -velocity_y.
    if state[BY] < 0:
        # print "bounce down"
        state[BY] = -state[BY]
        state[VY] = -state[VY]
# If ball_y > 1 (the ball is off the bottom of the screen), let ball_y = 2 - ball_y and velocity_y = -velocity_y.
    if state[BY] > 1:
        # print "bounce up"
        state[BY] = 2-state[BY]
        state[VY] = -state[VY]
# If ball_x < 0 (the ball is off the left edge of the screen), assign ball_x = -ball_x and velocity_x = -velocity_x.
    if state[BX] < 0:
        # print "bounce right"
        state[BX] = -state[BX]
        state[VX] = -state[VX]
# If ball bounce on paddle
    if (state[BX] >= paddle_x) and (state[BY]>=state[PY]) and (state[BY]<=state[PY]+paddle_height):
        # print "bounce on paddle!"
        state[BX] = 2*paddle_x - state[BX]
        # this loop makes sure |vx| > 0.03
        while True:
            new_vx = np.random.uniform(-0.015,0.015) - state[VX]
            if abs(new_vx) > 0.03: 
                state[VX] = new_vx
                state[VY] = state[VY] + np.random.uniform(-0.03,0.03)
                break
        return (state, 1)
# If terminal
    if (state[BX] > paddle_x) and ((state[BY]<state[PY]) or (state[BY]>state[PY]+paddle_height)):
        # print "terminal!"
        return (None, -1)
    return (state, 0)


def get_maxQ(state, Q):
    if state is None:
        return -1
    max_Q = -sys.maxint
    for action in actions:
        key = ( discretize_s(state), action )
        if key not in Q:
            max_Q = max(max_Q, 0)
        else:
            max_Q = max(max_Q, Q[key])
    return max_Q














