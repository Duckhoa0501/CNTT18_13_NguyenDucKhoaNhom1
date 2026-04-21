import pygame
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dfs_solver import dfs_step
from src.bfs_solver import bfs_step
from src.astar_solver import astar_step
from maps.maze_hard import maze
from src.core_logic import get_start_goal

# ===== CONFIG =====
CELL_SIZE = 50

BG      = (30, 30, 40)
WALL    = (70, 70, 90)
FLOOR   = (50, 50, 65)
PATH    = (255, 215, 0)
GOAL_C  = (255, 80, 80)

ROWS = len(maze)
COLS = len(maze[0])

start, goal = get_start_goal(maze)

# ===== INIT =====
pygame.init()
font = pygame.font.SysFont(None, 30)

screen = pygame.display.set_mode((COLS*CELL_SIZE, ROWS*CELL_SIZE + 80))
pygame.display.set_caption("Maze Firefighter AI")

clock = pygame.time.Clock()

# ===== BUTTON =====
btn_bfs   = pygame.Rect(20, ROWS*CELL_SIZE + 15, 90, 40)
btn_dfs   = pygame.Rect(120, ROWS*CELL_SIZE + 15, 90, 40)
btn_astar = pygame.Rect(220, ROWS*CELL_SIZE + 15, 90, 40)
btn_reset = pygame.Rect(330, ROWS*CELL_SIZE + 15, 110, 40)

def draw_button(text, rect, color, hover):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover, rect, border_radius=10)
        if click:
            return True
    else:
        pygame.draw.rect(screen, color, rect, border_radius=10)

    label = font.render(text, True, (255,255,255))
    screen.blit(label, (rect.x + 10, rect.y + 8))
    return False

# ===== DRAW MAP (FADE) =====
def draw_map():
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if maze[r][c] == 1:
                color = WALL
            else:
                color = FLOOR

            if (r,c) in visited:
                age = step_count - visited[(r,c)]
                fade = max(50, 255 - age * 15)
                color = (fade//3, fade//2, fade)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (20,20,30), rect, 1)

# ===== PATH =====
def draw_path():
    for i in range(len(path)-1):
        r1,c1 = path[i]
        r2,c2 = path[i+1]

        x1 = c1*CELL_SIZE + CELL_SIZE//2
        y1 = r1*CELL_SIZE + CELL_SIZE//2
        x2 = c2*CELL_SIZE + CELL_SIZE//2
        y2 = r2*CELL_SIZE + CELL_SIZE//2

        pygame.draw.line(screen, PATH, (x1,y1), (x2,y2), 5)

# ===== FIRETRUCK =====
def draw_firetruck():
    if current is None:
        return

    r, c = current
    x = c*CELL_SIZE
    y = r*CELL_SIZE

    pygame.draw.rect(screen, (200,0,0), (x+5, y+15, CELL_SIZE-10, CELL_SIZE-25), border_radius=5)
    pygame.draw.rect(screen, (255,80,80), (x+5, y+5, CELL_SIZE//2, CELL_SIZE//2), border_radius=5)

    pygame.draw.circle(screen, (0,0,0), (x+15, y+CELL_SIZE-10), 6)
    pygame.draw.circle(screen, (0,0,0), (x+CELL_SIZE-15, y+CELL_SIZE-10), 6)

    pygame.draw.rect(screen, (255,255,0), (x+CELL_SIZE//2, y+5, 10, 5))

# ===== GOAL =====
def draw_goal(t):
    r, c = goal
    x = c*CELL_SIZE + CELL_SIZE//2
    y = r*CELL_SIZE + CELL_SIZE//2

    radius = CELL_SIZE//3 + int(5 * math.sin(t))
    pygame.draw.circle(screen, GOAL_C, (x,y), radius)

# ===== STATE =====
mode = "BFS"
solver = bfs_step(maze)

visited = {} 
path = []
current = None
done = False
time = 0
step_count = 0

# ===== LOOP =====
running = True
while running:
    screen.fill(BG)
    time += 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ===== BUTTON =====
    if draw_button("BFS", btn_bfs, (70,130,180), (100,160,210)):
        mode = "BFS"
        solver = bfs_step(maze)
        visited, path, current, done = {}, [], None, False
        step_count = 0

    if draw_button("DFS", btn_dfs, (180,100,100), (210,130,130)):
        mode = "DFS"
        solver = dfs_step(maze)
        visited, path, current, done = {}, [], None, False
        step_count = 0

    if draw_button("A*", btn_astar, (120,100,200), (150,130,230)):
        mode = "A*"
        solver = astar_step(maze)
        visited, path, current, done = {}, [], None, False
        step_count = 0

    if draw_button("RESET", btn_reset, (100,100,100), (140,140,140)):
        solver = bfs_step(maze) if mode=="BFS" else dfs_step(maze) if mode=="DFS" else astar_step(maze)
        visited, path, current, done = {}, [], None, False
        step_count = 0

    # ===== SOLVER =====
    if not done:
        try:
            current, path, _ = next(solver)
            step_count += 1

            if current not in visited:
                visited[current] = step_count

        except StopIteration:
            done = True

    # ===== DRAW =====
    draw_map()
    draw_path()
    draw_firetruck()
    draw_goal(time)

    label = font.render(f"Mode: {mode}", True, (255,255,255))
    screen.blit(label, (460, ROWS*CELL_SIZE + 20))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()