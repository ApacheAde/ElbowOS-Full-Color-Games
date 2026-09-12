#!/usr/bin/env python3
"""Frogger-style road and river crossing."""

import pygame

W, H = 640, 720
LANE = 48
COLS = 16
CELL = W // COLS


class Hopper:
    def __init__(self):
        self.x = COLS // 2
        self.y = 13
        self.alive = True

    def rect(self):
        return pygame.Rect(self.x * CELL + 6, self.y * LANE + 8, CELL - 12, LANE - 16)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Frog Dash — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    frog = Hopper()
    score = 0
    cars = []
    logs = []
    for lane, speed, n, w in ((11, 3, 3, 2), (10, -4, 3, 2), (9, 5, 2, 3), (8, -3, 3, 2)):
        for i in range(n):
            cars.append({"lane": lane, "x": i * (W // n), "spd": speed, "w": w * CELL})
    for lane, speed, n, w in ((6, 2, 3, 3), (5, -3, 3, 2), (4, 2.5, 2, 4), (3, -2, 3, 3)):
        for i in range(n):
            logs.append({"lane": lane, "x": i * (W // n), "spd": speed, "w": w * CELL})
    homes = [False] * 5
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            if e.type == pygame.KEYDOWN and frog.alive:
                if e.key == pygame.K_LEFT:
                    frog.x = max(0, frog.x - 1)
                if e.key == pygame.K_RIGHT:
                    frog.x = min(COLS - 1, frog.x + 1)
                if e.key == pygame.K_UP:
                    frog.y = max(0, frog.y - 1)
                    score += 1
                if e.key == pygame.K_DOWN:
                    frog.y = min(13, frog.y + 1)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                frog = Hopper()
                homes = [False] * 5
                score = 0
        for c in cars:
            c["x"] = (c["x"] + c["spd"]) % (W + 160) - 80
        for lg in logs:
            lg["x"] = (lg["x"] + lg["spd"]) % (W + 200) - 100
        if frog.alive:
            if 8 <= frog.y <= 11:
                fr = frog.rect()
                hit = any(fr.colliderect(pygame.Rect(c["x"], c["lane"] * LANE + 8, c["w"], LANE - 16)) for c in cars)
                if hit:
                    frog.alive = False
            if 3 <= frog.y <= 6:
                fr = frog.rect()
                riding = None
                for lg in logs:
                    rr = pygame.Rect(lg["x"], lg["lane"] * LANE + 6, lg["w"], LANE - 12)
                    if fr.colliderect(rr):
                        riding = lg
                        break
                if riding:
                    frog.x = int((frog.rect().centerx + riding["spd"]) // CELL)
                    if frog.x < 0 or frog.x >= COLS:
                        frog.alive = False
                else:
                    frog.alive = False
            if frog.y == 1:
                slot = min(4, max(0, frog.x * 5 // COLS))
                if not homes[slot]:
                    homes[slot] = True
                    score += 50
                    frog.x, frog.y = COLS // 2, 13
                    if all(homes):
                        score += 200
                        homes = [False] * 5
                else:
                    frog.alive = False
        screen.fill((20, 20, 28))
        pygame.draw.rect(screen, (36, 160, 64), (0, 12 * LANE, W, LANE * 2))
        pygame.draw.rect(screen, (40, 40, 48), (0, 8 * LANE, W, LANE * 4))
        pygame.draw.rect(screen, (36, 160, 64), (0, 7 * LANE, W, LANE))
        pygame.draw.rect(screen, (28, 92, 180), (0, 3 * LANE, W, LANE * 4))
        pygame.draw.rect(screen, (36, 160, 64), (0, 0, W, LANE * 3))
        for i in range(5):
            hx = 20 + i * 124
            col = (80, 220, 120) if homes[i] else (20, 80, 40)
            pygame.draw.rect(screen, col, (hx, 16, 90, LANE + 10), border_radius=8)
        for c in cars:
            pygame.draw.rect(screen, (220, 48, 48) if c["spd"] > 0 else (48, 120, 255),
                             (c["x"], c["lane"] * LANE + 8, c["w"], LANE - 16), border_radius=6)
        for lg in logs:
            pygame.draw.rect(screen, (140, 84, 36),
                             (lg["x"], lg["lane"] * LANE + 8, lg["w"], LANE - 16), border_radius=8)
        col = (80, 220, 80) if frog.alive else (80, 40, 40)
        pygame.draw.ellipse(screen, col, frog.rect())
        pygame.draw.circle(screen, (20, 40, 20), (frog.rect().centerx - 6, frog.rect().y + 10), 3)
        pygame.draw.circle(screen, (20, 40, 20), (frog.rect().centerx + 6, frog.rect().y + 10), 3)
        screen.blit(font.render(f"FROG DASH   Score {score}    ElbowOS", True, (255, 255, 255)), (12, H - 36))
        if not frog.alive:
            screen.blit(font.render("SPLAT  —  R to retry", True, (255, 220, 80)), (200, H // 2))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
