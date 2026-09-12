#!/usr/bin/env python3
"""Pick-10 colourful keno board."""

import random
import pygame

W, H = 900, 620


def payout(hits, wager):
    table = {0: 0, 1: 0, 2: 0, 3: 1, 4: 2, 5: 5, 6: 15, 7: 50, 8: 200, 9: 1000, 10: 5000}
    return wager * table.get(hits, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Lucky Keno — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20, bold=True)
    big = pygame.font.SysFont("arial", 32, bold=True)
    picked = set()
    drawn = set()
    credits = 100
    wager = 2
    msg = "Pick up to 10 numbers, then DRAW"
    cells = []
    for n in range(1, 81):
        c, r = (n - 1) % 10, (n - 1) // 10
        cells.append((n, pygame.Rect(40 + c * 64, 120 + r * 48, 56, 40)))
    draw_btn = pygame.Rect(700, 120, 160, 50)
    clear_btn = pygame.Rect(700, 184, 160, 50)
    plus_btn = pygame.Rect(700, 248, 70, 50)
    minus_btn = pygame.Rect(790, 248, 70, 50)
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if draw_btn.collidepoint(e.pos) and picked and credits >= wager:
                    credits -= wager
                    drawn = set(random.sample(range(1, 81), 20))
                    hits = len(picked & drawn)
                    win = payout(hits, wager)
                    credits += win
                    msg = f"{hits} hits   +${win}"
                    if credits < wager:
                        credits += 50
                        msg += "   (+50 house chip)"
                elif clear_btn.collidepoint(e.pos):
                    picked.clear()
                    drawn.clear()
                    msg = "Board cleared"
                elif plus_btn.collidepoint(e.pos):
                    wager = min(20, wager + 1)
                elif minus_btn.collidepoint(e.pos):
                    wager = max(1, wager - 1)
                else:
                    for n, rect in cells:
                        if rect.collidepoint(e.pos):
                            if n in picked:
                                picked.remove(n)
                            elif len(picked) < 10:
                                picked.add(n)
        screen.fill((18, 24, 64))
        screen.blit(big.render("LUCKY KENO", True, (255, 210, 70)), (40, 24))
        screen.blit(font.render(f"Credits ${credits}   Wager ${wager}   Picked {len(picked)}/10    ElbowOS", True, (230, 230, 255)), (40, 70))
        screen.blit(font.render(msg, True, (180, 255, 200)), (40, 96))
        for n, rect in cells:
            if n in picked and n in drawn:
                col = (48, 200, 96)
            elif n in drawn:
                col = (200, 48, 80)
            elif n in picked:
                col = (48, 96, 220)
            else:
                col = (40, 48, 96)
            pygame.draw.rect(screen, col, rect, border_radius=8)
            t = font.render(str(n), True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=rect.center))
        for btn, lab, col in (
            (draw_btn, "DRAW 20", (36, 140, 80)),
            (clear_btn, "CLEAR", (140, 60, 60)),
            (plus_btn, "+", (36, 80, 160)),
            (minus_btn, "-", (36, 80, 160)),
        ):
            pygame.draw.rect(screen, col, btn, border_radius=8)
            t = font.render(lab, True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=btn.center))
        screen.blit(font.render("Blue=yours  Red=drawn  Green=hit", True, (200, 200, 230)), (700, 320))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
