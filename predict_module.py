import numpy as np
import math


def get_nu_square(mat_u,window):
    sum = 0
    for i in range(0, window):
        test = mat_u[mat_u.shape[0]-1,i]
        sum=sum+test*test
    return sum;

def det_vector(mat_u, nu_square,window):
    a_vec = np.zeros((window,))

    for i in range(0, window):
        a_vec=a_vec+(mat_u.transpose()[i]*mat_u[mat_u.shape[1]-1,i])/(1-nu_square)
    return a_vec

def predict(timeline, a_vec, horizon,window):
    for h in range(0, horizon):
        ans =  predict_next(timeline,a_vec,window)
        timeline[len(timeline.items())+1]=ans

def predict_next(timeline,a_vec,window):
    sum=0
    for i in range(0, window-1):
        comp = a_vec[i]
        sum = sum + timeline[len(timeline.items())-i] * comp


    return sum;

     