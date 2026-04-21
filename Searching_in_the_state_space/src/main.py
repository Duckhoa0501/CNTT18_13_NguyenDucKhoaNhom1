#Khi chạy ứng dụng ấn B để xem BFS, ấn D để xem DFS nhé.
import pygame
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dfs_solver import dfs_step
from maps.maze_hard import maze
from src.bfs_solver import bfs_step
from src.core_logic import get_start_goal

# ===== Cấu hình ======
CELL_SIZE = 50

BG      = (30, 30, 40)
WALL    = (70, 70, 90)
FLOOR   = (50, 50, 65)
VISITED = (80, 100, 120)
PATH    = (255, 215, 0)
PLAYER  = (0, 255, 150)
GOAL_C  = (255, 80, 80)

ROWS = len(maze)
COLS = len(maze[0])

start, goal = get_start_goal(maze)

# ====== vẽ map ======
def draw_map(screen, maze, visited):
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(
                c*CELL_SIZE,
                r*CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            if maze[r][c] == 1:
                color = WALL
            else:
                color = FLOOR

            if (r,c) in visited:
                color = VISITED

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (20,20,30), rect, 1)

# ====== Vẽ đường chạy ======
def draw_path(screen, path):
    if len(path) < 2:
        return

    for i in range(len(path)-1):
        r1,c1 = path[i]
        r2,c2 = path[i+1]

        x1 = c1*CELL_SIZE + CELL_SIZE//2
        y1 = r1*CELL_SIZE + CELL_SIZE//2
        x2 = c2*CELL_SIZE + CELL_SIZE//2
        y2 = r2*CELL_SIZE + CELL_SIZE//2

        pygame.draw.line(screen, PATH, (x1,y1), (x2,y2), 5)

# ====== vẽ người di chuyển ======
def draw_player(screen, current):
    if current is None:
        return

    r, c = current
    x = c*CELL_SIZE + CELL_SIZE//2
    y = r*CELL_SIZE + CELL_SIZE//2

    pygame.draw.circle(screen, PLAYER, (x,y), CELL_SIZE//3)

# ====== Mục tiêu xung quanh ======
def draw_goal(screen, goal, t):
    r, c = goal
    x = c*CELL_SIZE + CELL_SIZE//2
    y = r*CELL_SIZE + CELL_SIZE//2

    radius = CELL_SIZE//3 + int(5 * math.sin(t))
    pygame.draw.circle(screen, GOAL_C, (x,y), radius)

# ====== INIT ======
pygame.init()

font = pygame.font.SysFont(None, 36)
screen = pygame.display.set_mode((COLS*CELL_SIZE, ROWS*CELL_SIZE))
pygame.display.set_caption("Maze Game AI")

clock = pygame.time.Clock()

mode = "BFS"
solver = bfs_step(maze)

visited = set()
path = []
current = None
done = False
time = 0

# ====== lặp và điều kiện chạy Dfs và BFS ======
running = True
while running:
    screen.fill(BG)
    time += 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Nhấn B → BFS
            if event.key == pygame.K_b:
                mode = "BFS"
                solver = bfs_step(maze)
                visited = set()
                path = []
                current = None
                done = False

            # Nhấn D → DFS
            if event.key == pygame.K_d:
                mode = "DFS"
                solver = dfs_step(maze)
                visited = set()
                path = []
                current = None
                done = False

    if not done:
        try:
            current, path, visited = next(solver)
        except StopIteration:
            done = True

    draw_map(screen, maze, visited)
    draw_path(screen, path)
    draw_player(screen, current)
    draw_goal(screen, goal, time)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()