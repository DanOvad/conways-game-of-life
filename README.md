# README

## Objective

The purpose of this project is to familiarize myself with Conway's Game of Life, working exclusively in numpy arrays, and generating animations through matplotlib.

This is also useful context for [Kaggle's Conway's Reverse Game of Life](https://www.kaggle.com/c/conways-reverse-game-of-life-2020/overview/description) competition.

The purpose of the Kaggle competition is the following:
<i>This competition is an experiment to see if machine learning (or optimization, or any method) can predict the game of life in reverse. Is the chaotic start of Life predictable from its orderly ends? We have created many games, evolved them, and provided only the end boards. You are asked to predict the starting board that resulted in each end board.</i>

---
## Conway's Game of Life
In this repo, I am going to explore implementing [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in python and generate GIFs of different starting points.

### Context

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

Some other better implementations of [Conways Game of life in Python](http://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/). This article contains the stepping function that is used for the Kaggle competition.

### First thoughts
At the start, I knew I would have to split this into two or three functions.
- Count all the neighbors for each node
- Produce a list of positions to flip or keep as is.
- Generate the living states for the next board.

Very quickly I realized that producing an array for flips wasn't needed. Once you have an array showing the count of neighbors for each position, you can use it in conjunction with current board to determine dead cells that will be birthed and live cells that will survive. From there, determining and generating the next board became trivial.

### 1. Determining neighbor count

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

<pre><code>def get_new_state(arr):
    # These are the positions to bring to life
    birth = (count_arr == 3) * ~arr.astype(bool)

    # These are the positions to keep alive
    live = ((count_arr == 2) + (count_arr == 3)) * arr.astype(bool)

    # Combine them
    return (birth + live).astype(int)</code></pre>


![]('./gifs/random-game-1.gif')


---
## Generating Animations and GIFs
This was the most frustrating part of this project. Was reliably generating animations in jupyter notebook, and reliably generating GIFs or MP4s to file.

### Animations
So many ways to do it: `FuncAnimation`, `ArtistAnimation`, using `plt.imshow()` or `plt.matshow()`, or imageio.

### Saving to file (GIFs, MP4s, etc.)

Trying to write to a GIF was very difficult and required exploring different types of writers. From MovieWriter, to PillowWriter, to imagemagick, and ffmpeg.


## Conclusion
