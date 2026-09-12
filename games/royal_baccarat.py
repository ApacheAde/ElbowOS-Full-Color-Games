#!/usr/bin/env python3
"""Colourful baccarat table. Player vs Banker with standard third-card rules."""

import random
import pygame

W, H = 960, 540
FELT = (12, 92, 48)
GOLD = (232, 188, 64)
WHITE = (250, 246, 236)
RED = (196, 36, 48)
BLUE = (36, 72, 180)
RANKS = "A23456789TJQK"
SUITS = "♠♥♦♣"


def card_value(rank):
    if rank in "TJQK":
        return 0
    if rank == "A":
        return 1
    return int(rank)


def hand_total(cards):
    return sum(card_value(c[0]) for c in cards) % 10


def draw_card(deck):
    return deck.pop()


def need_player_third(pt):
    return pt <= 5


def need_banker_third(bt, pt, p3):
    if p3 is None:
        return bt <= 5
    v = card_value(p3[0])
    if bt <= 2:
        return True
    if bt == 3:
        return v != 8
    if bt == 4:
        return v in (2, 3, 4, 5, 6, 7)
    if bt == 5:
        return v in (4, 5, 6, 7)
    if bt == 6:
        return v in (6, 7)
    return False


def draw_card_face(surf, font, card, x, y):
    r = pygame.Rect(x, y, 78, 108)
    pygame.draw.rect(surf, WHITE, r, border_radius=8)
    pygame.draw.rect(surf, (20, 20, 20), r, 2, border_radius=8)
    color = RED if card[1] in "♥♦" else (20, 20, 20)
    label = card[0].replace("T", "10") + card[1]
    surf.blit(font.render(label, True, color), (x + 8, y + 8))
    surf.blit(font.render(card[1], True, color), (x + 28, y + 44))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Royal Baccarat — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 36, bold=True)
    bankroll = 200
    bet_kind = "player"
    bet_amt = 10
    result = "Pick a side, then DEAL"
    player, banker = [], []
    buttons = {
        "player": pygame.Rect(80, 430, 160, 54),
        "banker": pygame.Rect(260, 430, 160, 54),
        "tie": pygame.Rect(440, 430, 120, 54),
        "deal": pygame.Rect(600, 430, 140, 54),
        "plus": pygame.Rect(780, 430, 54, 54),
        "minus": pygame.Rect(850, 430, 54, 54),
    }
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pos = e.pos
                if buttons["player"].collidepoint(pos):
                    bet_kind = "player"
                elif buttons["banker"].collidepoint(pos):
                    bet_kind = "banker"
                elif buttons["tie"].collidepoint(pos):
                    bet_kind = "tie"
                elif buttons["plus"].collidepoint(pos):
                    bet_amt = min(100, bet_amt + 5)
                elif buttons["minus"].collidepoint(pos):
                    bet_amt = max(5, bet_amt - 5)
                elif buttons["deal"].collidepoint(pos) and bankroll >= bet_amt:
                    deck = [(r, s) for r in RANKS for s in SUITS]
                    random.shuffle(deck)
                    player = [draw_card(deck), draw_card(deck)]
                    banker = [draw_card(deck), draw_card(deck)]
                    pt, bt = hand_total(player), hand_total(banker)
                    p3 = None
                    if pt <= 7 and bt <= 7:
                        if need_player_third(pt):
                            p3 = draw_card(deck)
                            player.append(p3)
                            pt = hand_total(player)
                        if need_banker_third(bt, pt, p3):
                            banker.append(draw_card(deck))
                    pt, bt = hand_total(player), hand_total(banker)
                    if pt > bt:
                        winner = "player"
                    elif bt > pt:
                        winner = "banker"
                    else:
                        winner = "tie"
                    if bet_kind == winner:
                        payout = bet_amt * (8 if winner == "tie" else (0.95 if winner == "banker" else 1))
                        bankroll += int(round(payout))
                        result = f"{winner.upper()} wins  +{int(round(payout))}"
                    else:
                        bankroll -= bet_amt
                        result = f"{winner.upper()} wins  -{bet_amt}"
                    if bankroll < 5:
                        result += "   (reload: click DEAL with $0 for +200)"
                elif buttons["deal"].collidepoint(pos) and bankroll < 5:
                    bankroll = 200
                    result = "House floated you another 200"
        screen.fill(FELT)
        pygame.draw.ellipse(screen, (8, 64, 32), (40, 40, W - 80, 360), 8)
        screen.blit(big.render("ROYAL BACCARAT", True, GOLD), (40, 16))
        screen.blit(font.render("ElbowOS casino  •  https://x.com/ElbowOS", True, WHITE), (40, 58))
        screen.blit(font.render(f"Bankroll  ${bankroll}    Bet  ${bet_amt} on {bet_kind.upper()}", True, GOLD), (40, 92))
        screen.blit(font.render(result, True, WHITE), (40, 122))
        screen.blit(font.render("PLAYER", True, BLUE), (140, 170))
        screen.blit(font.render("BANKER", True, RED), (560, 170))
        if player:
            screen.blit(font.render(str(hand_total(player)), True, WHITE), (140, 200))
            for i, c in enumerate(player):
                draw_card_face(screen, font, c, 140 + i * 90, 230)
        if banker:
            screen.blit(font.render(str(hand_total(banker)), True, WHITE), (560, 200))
            for i, c in enumerate(banker):
                draw_card_face(screen, font, c, 560 + i * 90, 230)
        for name, rect in buttons.items():
            col = GOLD if name == bet_kind else (28, 120, 64)
            if name in ("deal", "plus", "minus"):
                col = (28, 80, 160)
            pygame.draw.rect(screen, col, rect, border_radius=10)
            label = {"player": "PLAYER", "banker": "BANKER", "tie": "TIE 8:1", "deal": "DEAL", "plus": "+", "minus": "-"}[name]
            lab = font.render(label, True, WHITE)
            screen.blit(lab, lab.get_rect(center=rect.center))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
