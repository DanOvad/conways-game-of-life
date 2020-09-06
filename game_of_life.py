import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation


arr = np.random.randint(low=0, high=2, size=(20,20))

def count_neighbors_simple(arr):
    ''' This function takes in an array of ones and zeros,
    and returns an array of the same shape with how many
    cardinal neighbors each position has.
    '''
    # Determine the number of neighbors in each direction
        # Yes if my neighbor is greater than me, or equal to me when I'm alive.
    left_neigh = np.roll(arr,1,axis=0) # Yes if my neighbor is alive.
    right_neigh = np.roll(arr,-1,axis=0)
    up_neigh = np.roll(arr,-1,axis=1)
    down_neigh = np.roll(arr,1,axis=1)

    up_left_neigh = np.roll(np.roll(arr, 1, axis=1), 1, axis=0)
    up_right_neigh = np.roll(np.roll(arr, -1, axis=1), 1, axis=0)
    down_left_neigh = np.roll(np.roll(arr, 1, axis=1), -1, axis=0)
    down_right_neigh = np.roll(np.roll(arr, -1, axis=1), -1, axis=0)

    # Sum them up and return the array
    sum_neigh = left_neigh + right_neigh + up_neigh + down_neigh + up_left_neigh + up_right_neigh + down_left_neigh + down_right_neigh
    return sum_neigh


def generate_next_board(arr):
    count_arr = count_neighbors(arrrr)
    return np.logical_or((count_arr==3), np.logical_and(count_arr==2, arr)).astype(int)



def generate_series(arr, n_frames):
    '''Generate a series of boards starting from the starting array arr and evolving forward by n_frames.'''
    # First add in the first element
    frame_list = [arr]

    # Iterate over the number of frames
    for frame in range(n_frames):
        frame_list.append(get_new_state(frame_list[frame]))

    return frame_list

frames = generate_series(arr, 100)

def generate_gif(frame_list, filepath):
    mpl.rc('animation', html='jshtml')
    fig, ax = plt.subplots()
    plt.close()
    #ims = onp.random.uniform(0, 1, size=[5, 28, 28])
    ims = frame_list #MNIST_IMAGES[:5]
    ims = [[ax.imshow(im, animated=True)] for im in ims]
    anim = mpl.animation.ArtistAnimation(fig, ims, interval=100, repeat_delay = 200)
    anim.save(filepath, writer='imagemagick')
    return anim


anim = generate_gif(frames, 'gifs/test3.gif')
