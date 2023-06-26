# Snake Pathfinding AI

This AI-powered snake game uses the Breadth-First Search (BFS) algorithm to navigate the snake autonomously. Learn how this project was developed by watching this [YouTube video](https://youtu.be/UIKthUWZ8dw) (Arabic).

![Gameplay](https://user-images.githubusercontent.com/38482276/87240274-cae19380-c420-11ea-8193-bddab2ef379d.gif)

## Setup and Execution

1. Download and install [Python 3](https://www.python.org).
2. Install the required modules by executing the following command in your terminal:
```bash
pip install pygame
```
3. Run `play.py` to start the game.

## Code Overview

- `settings.py` : This file houses game configurations and global variables such as width and height.
- `snake.py` : This is where the Snake and Square classes are defined.
- `play.py` : Contains the code required to run the game.

## Functionality

1. The snake uses the BFS algorithm to find the shortest path (path_1) to the apple. If path_1 is not accessible, the process moves to step 4.
2. A virtual snake, identical to the actual one, is created and set to follow path_1.
3. Once the virtual snake reaches the apple, the path between its head and tail (path_2) is checked. If accessible, the actual snake is then directed to follow path_1.
4. If either path_1 or path_2 is inaccessible, the actual snake is commanded to follow its tail.

For more details, please read the comments in the `.py` files.

## Contributors

- **Hayder Kharrufa** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for more details.
