# README

## Objective

The purpose of this project is to play with with Conway's Game of Life, numpy arrays, and animations in matplotlib.

This is also useful context for [Kaggle's Conway's Reverse Game of Life](https://www.kaggle.com/c/conways-reverse-game-of-life-2020/overview/description) competition.

The purpose of the Kaggle competition is the following:
<i>This competition is an experiment to see if machine learning (or optimization, or any method) can predict the game of life in reverse. Is the chaotic start of Life predictable from its orderly ends? We have created many games, evolved them, and provided only the end boards. You are asked to predict the starting board that resulted in each end board.</i>

---
## Conway's Game of Life
In this repo, I am going to explore implementing [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in python and generate GIFs of different starting points.
For more information on the general topic of cellular evolution, there is a [towards data science blogpost](https://towardsdatascience.com/algorithmic-beauty-an-introduction-to-cellular-automata-f53179b3cf8f) by Evan Kozliner that provides some good information.

### Rules
The following is from wikipedia explaining the rules:

The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead, (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours, which are the cells that are <b>horizontally, vertically, or diagonally adjacent</b> [8 potential neighbours]. At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

These rules, which compare the behavior of the automaton to real life, can be condensed into the following:

1. Any live cell with two or three live neighbours survives.
2. Any dead cell with three live neighbours becomes a live cell.
3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed; births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick. Each generation is a pure function of the preceding one. The rules continue to be applied repeatedly to create further generations.

---
## Implementing
For a more robust explanation of implementing Conway's Game of life in python, Jake Vanderplas wrote a blog, aptly titled, [Conway's Game of Life in Python](http://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/). This article contains the stepping function that is used for the Kaggle competition.

### First thoughts
At the start, I knew I would have to split this into two or three functions.
- Count all the neighbors for each cell.
- Produce a list of positions to flip for the next tick.
- Generate the living states on the board for the next tick.

Very quickly I realized that producing an array for flips wasn't needed. Once you have an array showing the count of neighbors for each cell, you can use it in conjunction with the current board to determine dead cells that will be birthed and live cells that will survive. From there, determining and generating the next board became trivial.

### 1. Determining neighbor count
My approach to checking neighbors started by shifting the array along axes and then comparing to the original cell. At first I considered all cases and was doing subtractions and additions. I came up the logic where it worked, but it was long and messy. As I was testing, I realized that I could simplify the logic by considering the arrays as booleans, and considering matrix boolean algebra instead of simply addition and subtraction.

From this I produced the following code:

<pre><code>
def count_neighbors_simple(arr):
''' This function takes in an array of ones and zeros,
and returns an array of the same shape of integers counting the number of neighbors for each position.
'''

    # Determine the number of neighbors in horizontal and vertical directions
        # Yes if my neighbor is greater than me, or equal to me when I'm alive.
    left_neigh = np.roll(arr,1,axis=0) # 1 if my neighbor is alive.
    right_neigh = np.roll(arr,-1,axis=0)
    up_neigh = np.roll(arr,-1,axis=1)
    down_neigh = np.roll(arr,1,axis=1)

    # Determine the number of neighbors in diagonal directions
    up_left_neigh = np.roll(np.roll(arr, 1, axis=1), 1, axis=0)
    up_right_neigh = np.roll(np.roll(arr, -1, axis=1), 1, axis=0)
    down_left_neigh = np.roll(np.roll(arr, 1, axis=1), -1, axis=0)
    down_right_neigh = np.roll(np.roll(arr, -1, axis=1), -1, axis=0)

    # Sum them up and return the array
    sum_neigh = left_neigh + right_neigh + up_neigh + down_neigh + up_left_neigh + up_right_neigh + down_left_neigh + down_right_neigh
    return sum_neigh
    </code></pre>


This can be further condensed with a loop over axes, but at this stage it simply represents how we are counting each neighbor.

If we would like to change the definition of our world to being finite. We would implement a few changes at this stage. Specifically excluding edges from looping around axes

### 2. Logic for generating new board

The key was recognizing that the sum of boolean arrays, represented `OR` while the product of the two boolean arrays represented `AND`. The simplified rules, listed above, lists three rules. Below I will break down how they can be interpreted and implimented.

#### 1. Live cells surviving

`1. Any live cell with two or three live neighbours survives.`

Can be simplified to: `(Number of neighbors == 2 OR 3) AND (alive)`

Can be implemented using: `((count_arr == 2) + (count_arr == 3)) * arr.astype(bool)`

#### 2. Dead cells birthing

`2. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.` <br>

Can be simplified to: `(Number of neighbors == 3) AND (not alive)`<br>

Can be implemented using: `(count_arr == 3) * ~arr.astype(bool)`.

#### 3. All others cells

`3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.`<br>

Can be simplified to, all other cells do not impact the future board.

Once I realized this, it was trivial to realize that all living cells on the new board come from survivors and new births. Therefore, the newboard can be generated using `count_arr` and our current board `arr`.

<pre><code>def generate_next_board(arr):
    # These are the positions to bring to life
    birth = (count_arr == 3) * ~arr.astype(bool)

    # These are the positions to keep alive
    live = ((count_arr == 2) + (count_arr == 3)) * arr.astype(bool)

    # Combine them
    return (birth + live).astype(int)</code></pre>

This can be further simplified using np.logical_and() and np.logical_or() and combined into the same statement:

<pre><code>def generate_next_board(arr):
    count_arr = count_neighbors(arr)
    return np.logical_or((count_arr==3), np.logical_and(count_arr==2, arr)).astype(int)</code></pre>


### Examples:
Some examples of classic seed patterns. These seeds and more about the context of this problem are expanded upon in Jake Vanderplas' blog post [Conway's Game of Life in Python](http://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/). Strongly recommend a glance.

##### Glider
<img src="/gifs/glider20x20-50frames.gif" />

##### Gospel Gun
<img src="/gifs/gospel_gun-250.gif" />

##### Unbounded growth
<img src="/gifs/unbounded-250.gif" />

##### Random State
<img src="/gifs/random-state-250.gif" />

---


## Generating Animations and GIFs
This was the most frustrating part of this project. It broke out into two difficulties:
1. Trying to get Jupyter Notebook to produce an interactive animation.
2. Trying to get matplotlib.animations to produce a GIF to present in the readme.

### Animations in Jupyter
There were just many ways to do it, with a variety of different errors. Either generatively through `FuncAnimation`, or preprocessing each frame with `ArtistAnimation`. Given the data I was working with I could've used `plt.imshow()` or `plt.matshow()`, or another option using `imageio`.

I ended up pregenerating the list of frames and used `ArtistAnimation` and `plt.imshow()`. I also ultimately had to use `plt.rc` and set the `rcParams` to `animation=True` which finally made it work.

### Saving to file (GIFs, MP4s, etc.)
This also proved difficult. I am not familiar with image writers, such as `MovieWriter`, `PillowWriter`, `imagemagick`, or `ffmpeg`, so this was my first time exposed to this. I ended up conda installing imagemagick and checked `which magick` and saving started working using `imagemagic` as the writer.

## Conclusion
Overall this was a great project. It was fun testing and verifying the logic of my code to make sure I was getting the results I was expecting. It was very rewarding when everything made sense, and the best part there isn't a ton of code and dependencies making changes difficult to manage.

### Next Steps
I have a couple thoughts as to the direction I can take this:
1. Finite Space: Try and change the world from wrapping around the edges, to stop at the edges.
2. Generate a universe that expands as live cells grow to the edges. This would be a great exercise to handle the growth of the graph as the number of ticks increase. It would also provide an interesting lesson in learning how to handle sparse matrices to represent data.
3. Pivot towards Kaggle, and attempt working on modeling Conway's Reverse Game of Life. The Kaggle competition did mention that a perfect solution is possible. This would be an interesting experience to work with GANs, and exploring other tools used in this space.
