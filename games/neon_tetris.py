#!/usr/bin/env python3
"""Neon tetromino stacker."""

import random
import pygame

COLS, ROWS = 10, 20
CELL = 26
OX, OY = 80, 20
W, H = 720, 560
SHAPES = {
    "I": [[(0, 1), (1, 1), (2, 1), (3, 1)], [(2, 0), (2, 1), (2, 2), (2, 3)]],
    "O": [[(1, 0), (2, 0), (1, 1), (2, 1)]],
    "T": [[(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (2, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (1, 2)], [(1, 0), (0, 1), (1, 1), (1, 2)]],
    "S": [[(1, 0), (2, 0), (0, 1), (1, 1)], [(1, 0), (1, 1), (2, 1), (2, 2)]],
    "Z": [[(0, 0), (1, 0), (1, 1), (2, 1)], [(2, 0), (1, 1), (2, 1), (1, 2)]],
    "J": [[(0, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (2, 0), (1, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (2, 2)], [(1, 0), (1, 1), (0, 2), (1, 2)]],
    "L": [[(2, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (1, 2), (2, 2)],
          [(0, 1), (1, 1), (2, 1), (0, 2)], [(0, 0), (1, 0), (1, 1), (1, 2)]],
}
COLORS = {
    "I": (48, 220, 255), "O": (255, 220, 48), "T": (188, 88, 255),
    "S": (48, 220, 96), "Z": (255, 72, 72), "J": (64, 96, 255), "L": (255, 148, 48),
}


def rot(name, r):
    opts = SHAPES[name]
    return opts[r % len(opts)]


def valid(board, name, r, x, y):
    for dx, dy in rot(name, r):
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= COLS or ny >= ROWS:
            return False
        if ny >= 0 and board[ny][nx]:
            return False
    return True


def stamp(board, name, r, x, y):
    for dx, dy in rot(name, r):
        nx, ny = x + dx, y + dy
        if 0 <= ny < ROWS:
            board[ny][nx] = COLORS[name]


def clear_rows(board):
    keep = [row for row in board if any(c is None for c in row)]
    cleared = ROWS - len(keep)
    while len(keep) < ROWS:
        keep.insert(0, [None] * COLS)
    return keep, cleared


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Tetris — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    board = [[None] * COLS for _ in range(ROWS)]
    bag = list(SHAPES)
    random.shuffle(bag)
    cur = bag.pop()
    rot_i, x, y = 0, 3, -1
    score = lines = 0
    fall = 0
    speed = 36
    over = False
    running = True
    while running:
        fall += 1
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            if over and e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                board = [[None] * COLS for _ in range(ROWS)]
                score = lines = 0
                over = False
                cur = random.choice(list(SHAPES))
                rot_i, x, y = 0, 3, -1
            if e.type == pygame.KEYDOWN and not over:
                if e.key == pygame.K_LEFT and valid(board, cur, rot_i, x - 1, y):
                    x -= 1
                if e.key == pygame.K_RIGHT and valid(board, cur, rot_i, x + 1, y):
                    x += 1
                if e.key == pygame.K_UP and valid(board, cur, rot_i + 1, x, y):
                    rot_i += 1
                if e.key == pygame.K_DOWN and valid(board, cur, rot_i, x, y + 1):
                    y += 1
                    score += 1
                if e.key == pygame.K_SPACE:
                    while valid(board, cur, rot_i, x, y + 1):
                        y += 1
                        score += 2
                    fall = speed
        if not over and fall >= max(8, speed - lines):
            fall = 0
            if valid(board, cur, rot_i, x, y + 1):
                y += 1
            else:
                stamp(board, cur, rot_i, x, y)
                board, n = clear_rows(board)
                lines += n
                score += (0, 100, 300, 500, 800)[n]
                if not bag:
                    bag = list(SHAPES)
                    random.shuffle(bag)
                cur = bag.pop()
                rot_i, x, y = 0, 3, -1
                if not valid(board, cur, rot_i, x, y):
                    over = True
        screen.fill((12, 10, 28))
        pygame.draw.rect(screen, (40, 30, 80), (OX - 6, OY - 6, COLS * CELL + 12, ROWS * CELL + 12), border_radius=8)
        for r in range(ROWS):
            for c in range(COLS):
                col = board[r][c] or (22, 18, 40)
                pygame.draw.rect(screen, col, (OX + c * CELL, OY + r * CELL, CELL - 2, CELL - 2), border_radius=3)
        if not over:
            for dx, dy in rot(cur, rot_i):
                nx, ny = x + dx, y + dy
                if ny >= 0:
                    pygame.draw.rect(screen, COLORS[cur], (OX + nx * CELL, OY + ny * CELL, CELL - 2, CELL - 2), border_radius=3)
        screen.blit(font.render("NEON TETRIS", True, (180, 140, 255)), (380, 30))
        screen.blit(font.render(f"Score {score}", True, (255, 255, 255)), (380, 80))
        screen.blit(font.render(f"Lines {lines}", True, (255, 255, 255)), (380, 114))
        screen.blit(font.render("Arrows + Space", True, (200, 200, 230)), (380, 160))
        screen.blit(font.render("ElbowOS", True, (255, 200, 80)), (380, 200))
        if over:
            screen.blit(font.render("GAME OVER  R=retry", True, (255, 80, 120)), (380, 260))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
