The task is to find paths from the start (yellow node) to the goal (orange node). 

Following search strategies are in `ai.py`:

- BFS
- DFS
- Uniform Cost Search
- A\* Search using Manhattan Distance as the heuristic

Usage
----
First, make sure you have Python 3.\* and the latest pip >= 20.\* (Check the `Notes & FAQ` section below if you're having trouble with this). Then, install the PyGame library: `pip install pygame`. 
Simply run `python main.py` and you will see the grid world window. By pressing `enter` you see how DFS finds a path . Pressing 2, 3, or 4 should respectively run BFS, UCS, A\* in a similar way, which you will implement (since right now it does nothing). 

