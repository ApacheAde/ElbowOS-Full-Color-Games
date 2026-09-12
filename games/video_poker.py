#!/usr/bin/env python3
"""Jacks-or-better video poker, full colour."""

import random
from collections import Counter
import pygame

W, H = 960, 540
RANKS = "A23456789TJQK"
SUITS = "♠♥♦♣"
RANK_VAL = {r: i for i, r in enumerate(RANKS, start=1)}


def fresh_deck():
    d = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(d)
    return d


def score_hand(cards):
    ranks = [c[0] for c in cards]
    suits = [c[1] for c in cards]
    vals = sorted(RANK_VAL[r] for r in ranks)
    flush = len(set(suits)) == 1
    wheel = vals == [1, 2, 3, 4, 13]
    straight = wheel or (vals == list(range(vals[0], vals[0] + 5)))
    counts = Counter(ranks)
    freq = sorted(counts.values(), reverse=True)
    if straight and flush and set(ranks) >= set("TJQKA"):
        return "ROYAL FLUSH", 800
    if straight and flush:
        return "STRAIGHT FLUSH", 50
    if freq[0] == 4:
        return "FOUR OF A KIND", 25
    if freq == [3, 2]:
        return "FULL HOUSE", 9
    if flush:
        return "FLUSH", 6
    if straight:
        return "STRAIGHT", 4
    if freq[0] == 3:
        return "THREE OF A KIND", 3
    if freq == [2, 2, 1]:
        return "TWO PAIR", 2
    pairs = [r for r, n in counts.items() if n == 2]
    if any(p in "AJQK" for p in pairs):
        return "JACKS OR BETTER", 1
    return "NOTHING", 0


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Video Poker — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 34, bold=True)
    credits = 100
    bet = 5
    deck = fresh_deck()
    hand = [deck.pop() for _ in range(5)]
    held = [False] * 5
    phase = "deal"
    msg = "DEAL then hold cards and DRAW"
    card_rects = [pygame.Rect(70 + i * 170, 200, 140, 190) for i in range(5)]
    deal_btn = pygame.Rect(360, 430, 240, 56)
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_EQUALS, pygame.K_PLUS):
                    bet = min(25, bet + 1)
                if e.key == pygame.K_MINUS:
                    bet = max(1, bet - 1)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if phase == "draw":
                    for i, r in enumerate(card_rects):
                        if r.collidepoint(e.pos):
                            held[i] = not held[i]
                if deal_btn.collidepoint(e.pos):
                    if phase == "deal" and credits >= bet:
                        credits -= bet
                        deck = fresh_deck()
                        hand = [deck.pop() for _ in range(5)]
                        held = [False] * 5
                        phase = "draw"
                        msg = "Click cards to HOLD, then DRAW"
                    elif phase == "draw":
                        for i in range(5):
                            if not held[i]:
                                hand[i] = deck.pop()
                        name, mult = score_hand(hand)
                        win = bet * mult
                        credits += win
                        msg = f"{name}   +${win}" if win else f"{name}"
                        phase = "deal"
                        if credits < 1:
                            credits = 100
                            msg += "   (reloaded 100)"
        screen.fill((18, 78, 42))
        pygame.draw.rect(screen, (212, 168, 48), (20, 20, W - 40, H - 40), 6, border_radius=16)
        screen.blit(big.render("JACKS-OR-BETTER  VIDEO POKER", True, (255, 220, 80)), (40, 36))
        screen.blit(font.render(f"Credits ${credits}    Bet ${bet}   [+/-]    ElbowOS", True, (255, 255, 255)), (40, 86))
        screen.blit(font.render(msg, True, (255, 240, 200)), (40, 122))
        for i, card in enumerate(hand):
            r = card_rects[i]
            pygame.draw.rect(screen, (250, 246, 236), r, border_radius=12)
            col = (196, 36, 48) if card[1] in "♥♦" else (20, 20, 20)
            label = card[0].replace("T", "10") + " " + card[1]
            screen.blit(big.render(label, True, col), (r.x + 16, r.y + 30))
            if held[i]:
                pygame.draw.rect(screen, (255, 210, 40), r, 6, border_radius=12)
                screen.blit(font.render("HOLD", True, (180, 40, 20)), (r.x + 40, r.y + 150))
            else:
                pygame.draw.rect(screen, (40, 40, 40), r, 2, border_radius=12)
        pygame.draw.rect(screen, (36, 96, 200), deal_btn, border_radius=10)
        lab = "DRAW" if phase == "draw" else "DEAL"
        t = big.render(lab, True, (255, 255, 255))
        screen.blit(t, t.get_rect(center=deal_btn.center))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
