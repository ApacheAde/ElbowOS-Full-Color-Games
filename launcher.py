#!/usr/bin/env python3
"""ElbowOS full-colour game launcher."""

import runpy
from pathlib import Path

import pygame

ROOT = Path(__file__).resolve().parent
GAMES = ROOT / "games"

TITLES = [
    ("Pipe Bros", "Mario-style platformer", "pipe_bros.py", (220, 64, 64)),
    ("Royal Baccarat", "Casino table", "royal_baccarat.py", (32, 140, 72)),
    ("Video Poker", "Jacks or better", "video_poker.py", (36, 96, 200)),
    ("Card War", "Classic card battle", "card_war.py", (128, 64, 196)),
    ("Neon Tetris", "Stack the blocks", "neon_tetris.py", (188, 88, 255)),
    ("Lucky Keno", "Pick 10, draw 20", "lucky_keno.py", (200, 140, 32)),
    ("Frog Dash", "Cross road and river", "frog_dash.py", (48, 180, 88)),
]


def launch(filename):
    pygame.quit()
    path = GAMES / filename
    runpy.run_path(str(path), run_name="__main__")
    raise SystemExit


def main():
    pygame.init()
    screen = pygame.display.set_mode((860, 560))
    pygame.display.set_caption("ElbowOS Full-Colour Games")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 36, bold=True)
    small = pygame.font.SysFont("arial", 16)
    buttons = []
    for i, (name, blurb, file, col) in enumerate(TITLES):
        col_i, row = i % 2, i // 2
        r = pygame.Rect(40 + col_i * 400, 120 + row * 90, 370, 76)
        buttons.append((r, file, name, blurb, col))
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for r, file, *_ in buttons:
                    if r.collidepoint(e.pos):
                        launch(file)
        screen.fill((16, 18, 36))
        screen.blit(big.render("ElbowOS Arcade", True, (255, 210, 70)), (40, 28))
        screen.blit(font.render("Full-colour Python 3 games   •   https://x.com/ElbowOS", True, (210, 210, 230)), (40, 74))
        mouse = pygame.mouse.get_pos()
        for r, file, name, blurb, col in buttons:
            c = tuple(min(255, x + 30) for x in col) if r.collidepoint(mouse) else col
            pygame.draw.rect(screen, c, r, border_radius=12)
            screen.blit(font.render(name, True, (255, 255, 255)), (r.x + 18, r.y + 14))
            screen.blit(small.render(blurb + "   " + file, True, (240, 240, 240)), (r.x + 18, r.y + 44))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
