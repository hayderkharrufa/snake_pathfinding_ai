##  Snake Pathfinding AI
AI plays snake game using BFS (Breadth-First Search) algorithm.<br />
Check out this **[YouTube video](https://youtu.be/UIKthUWZ8dw) (in Arabic)** to see how I built this project.

![gameplay](https://user-images.githubusercontent.com/38482276/87240274-cae19380-c420-11ea-8193-bddab2ef379d.gif)

### How to run?

- Install  [Python 3](https://www.python.org).
- Install these modules:
```
pip install pygame
```

- Run play.py file.

### Files / Directories

 - **settings.py** : contains game settings and global variables like width, height, etc..
 - **snake.py** : contains Snake and Square classes.
 - **play.py** : contains code for running the project.

### How it works?

1. The snake will use BFS algorithm to find the shortest path between its head and the apple (let's call it path_1). If path1 is not available, then go to step 4.
2. Create a virtual snake identical to the original snake and make it follow path_1.
3. After the virtual snake reaches the apple, check if the path between the virtual snake's head and its tail is available (let's call it path_2), if so, then make the original snake follow path_1.
4. If path_1 or path_2 are not available, make the original snake follow its tail.

For more details, read the comments in .py files.

### Authors

* **Hayder Kharrufa** - *Initial work* - 

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
