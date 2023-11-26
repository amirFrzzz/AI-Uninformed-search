def read_maze(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        n, m = map(int, lines[0].split(','))
        maze = [list(line.strip()) for line in lines[1:]]
    return n, m, maze


def find_start_and_goal(maze):
    start = tuple()
    goal = tuple()

    for i in range(len(maze)):
        if start and goal:
            break
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                start = (i, j)
            elif maze[i][j] == 'G':
                goal = (i, j)
            if start and goal:
                break

    return start, goal


def is_valid_move(maze, x, y):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != '%'

def has_common_element(queue_start, queue_goal):
    for item_start in queue_start:
        for item_goal in queue_goal:
            if item_start[0] == item_goal[0]:
                return True

    return False


def neighbor(t1, t2):
    if t1[0] == t2[0]:
        return abs(t1[1] - t2[1]) == 1
    elif t1[1] == t2[1]:
        return abs(t1[0] - t2[0]) == 1
    else:
        return False

def common_element_index(q1, q2):
    for index_start, item_start in enumerate(q1):
        for index_goal, item_goal in enumerate(q2):
            if item_start[0] == item_goal[0]:
                return index_start, index_goal


def bidirectional_search(maze):
    start, goal = find_start_and_goal(maze)

    # Initialize the visited sets for both directions
    visited_start = set()
    visited_goal = set()

    # Initialize the queues for both directions
    queue_start = [(start, [])]
    queue_goal = [(goal, [])]

    while queue_start and queue_goal:
        current_start, path_start = queue_start.pop(0)
        current_goal, path_goal = queue_goal.pop(0)
        visited_start.add(current_start)
        visited_goal.add(current_goal)

        moves = [(0, 1, 'r'), (-1, 0, 'u'), (0, -1, 'l'), (1, 0, 'd')]

        for delta_x, delta_y, direct in moves:
            next_start = (current_start[0] + delta_x, current_start[1] + delta_y)
            next_goal = (current_goal[0] - delta_x, current_goal[1] - delta_y)

            if is_valid_move(maze, *next_start) and next_start not in visited_start:
                queue_start.append((next_start, path_start + [direct]))


            if is_valid_move(maze, *next_goal) and next_goal not in visited_goal:
                queue_goal.append((next_goal, path_goal + [direct]))

            if has_common_element(queue_start, queue_goal) :
                x, y= common_element_index(queue_start, queue_goal)
                path_start = queue_start.pop(x)[1]
                path_goal = queue_goal.pop(y)[1]
                return path_start + path_goal[::-1]

        if neighbor(current_start, current_goal):

            # path_start = queue_start.pop(0)[1]
            a = list()
            for i in range(len(queue_start)):
                a.append(queue_start[i][0])
            path_start = queue_start.pop(a.index(current_goal))[1]
            return path_start + path_goal[::-1]

    return None  # No path found


if __name__ == "__main__":
    maze_file = "maze.txt"
    n, m, maze = read_maze(maze_file)
    path = bidirectional_search(maze)

    if path:
        print("Path:", ",".join(path))
    else:
        print("No path found.")