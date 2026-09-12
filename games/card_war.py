#!/usr/bin/env python3
"""War — colourful two-pile card battle."""

import random
import pygame

W, H = 900, 540
RANKS = "23456789TJQKA"
SUITS = "♠♥♦♣"
VAL = {r: i for i, r in enumerate(RANKS, start=2)}


def build():
    deck = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    mid = len(deck) // 2
    return deck[:mid], deck[mid:]


def face(card):
    return card[0].replace("T", "10") + card[1]


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Card War — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24, bold=True)
    big = pygame.font.SysFont("arial", 40, bold=True)
    you, cpu = build()
    last = None
    msg = "Click PLAY to flip"
    wars = 0
    play_btn = pygame.Rect(350, 430, 200, 56)
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and play_btn.collidepoint(e.pos):
                if not you or not cpu:
                    you, cpu = build()
                    msg = "New war"
                    last = None
                    continue
                pile = []
                while you and cpu:
                    a, b = you.pop(0), cpu.pop(0)
                    pile.extend([a, b])
                    last = (a, b)
                    if VAL[a[0]] > VAL[b[0]]:
                        random.shuffle(pile)
                        you.extend(pile)
                        msg = "You take the pile"
                        break
                    if VAL[b[0]] > VAL[a[0]]:
                        random.shuffle(pile)
                        cpu.extend(pile)
                        msg = "CPU takes the pile"
                        break
                    wars += 1
                    msg = "WAR!"
                    for _ in range(3):
                        if you:
                            pile.append(you.pop(0))
                        if cpu:
                            pile.append(cpu.pop(0))
                if not you:
                    msg = "CPU wins the war  (click for rematch)"
                elif not cpu:
                    msg = "You win the war  (click for rematch)"
        screen.fill((48, 28, 92))
        pygame.draw.rect(screen, (255, 196, 48), (16, 16, W - 32, H - 32), 5, border_radius=18)
        screen.blit(big.render("CARD WAR", True, (255, 220, 80)), (40, 30))
        screen.blit(font.render("ElbowOS  •  higher rank wins  •  ties go to war", True, (230, 220, 255)), (40, 84))
        screen.blit(font.render(f"You {len(you)} cards     CPU {len(cpu)} cards     Wars {wars}", True, (255, 255, 255)), (40, 124))
        screen.blit(font.render(msg, True, (255, 240, 180)), (40, 160))

        def paint(card, x, y, title):
            screen.blit(font.render(title, True, (255, 255, 255)), (x, y - 36))
            r = pygame.Rect(x, y, 150, 210)
            pygame.draw.rect(screen, (250, 246, 236), r, border_radius=12)
            if card:
                col = (196, 36, 48) if card[1] in "♥♦" else (20, 20, 20)
                screen.blit(big.render(face(card), True, col), (x + 18, y + 70))
            else:
                pygame.draw.rect(screen, (80, 40, 120), r.inflate(-20, -20), border_radius=8)

        a = last[0] if last else None
        b = last[1] if last else None
        paint(a, 180, 210, "YOU")
        paint(b, 560, 210, "CPU")
        pygame.draw.rect(screen, (36, 140, 80), play_btn, border_radius=10)
        t = big.render("PLAY", True, (255, 255, 255))
        screen.blit(t, t.get_rect(center=play_btn.center))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
