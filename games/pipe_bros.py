#!/usr/bin/env python3
"""Original Mario-style side-scroller. Not an emulator and not Nintendo IP."""

import pygame

W, H = 960, 540
TILE = 40
GRAV = 0.55
JUMP = -11.4
SPEED = 4.2
SKY = (92, 178, 255)
HILL = (46, 168, 72)
DIRT = (168, 92, 42)
BRICK = (214, 92, 48)
GOLD = (255, 208, 48)
FLAG = (48, 214, 96)
PLAYER = (236, 48, 48)
OVERALL = (48, 96, 220)
CRITTER = (168, 92, 36)

LEVEL = [
    "....................................................................................",
    "....................................................................................",
    "....................................................................................",
    "................C........C..............C.....C................C....................",
    "........................................................................F...........",
    "............BB.BBB..................BBBBB...........BB.................####.........",
    ".......................................................................####.........",
    "....C...........E........C....E..............E...........C....E........####.........",
    "##################..############..###############..###############################",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
]


class Actor:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.vx = 0
        self.vy = 0
        self.on_ground = False


def parse_level():
    solids, coins, enemies, flag = [], [], [], None
    rows = len(LEVEL)
    for j, row in enumerate(LEVEL):
        for i, ch in enumerate(row):
            x, y = i * TILE, (j + (H // TILE - rows)) * TILE
            if ch in "#D":
                solids.append(pygame.Rect(x, y, TILE, TILE))
            elif ch == "B":
                solids.append(pygame.Rect(x, y, TILE, TILE))
            elif ch == "C":
                coins.append(pygame.Rect(x + 12, y + 12, 16, 16))
            elif ch == "E":
                enemies.append(Actor(x + 4, y + 8, 32, TILE - 8))
                enemies[-1].vx = -1.6
            elif ch == "F":
                flag = pygame.Rect(x + 12, y - TILE * 3, 16, TILE * 4)
    return solids, coins, enemies, flag


def collide_axis(actor, solids, axis):
    for s in solids:
        if actor.rect.colliderect(s):
            if axis == "x":
                if actor.vx > 0:
                    actor.rect.right = s.left
                elif actor.vx < 0:
                    actor.rect.left = s.right
                actor.vx = 0
            else:
                if actor.vy > 0:
                    actor.rect.bottom = s.top
                    actor.on_ground = True
                elif actor.vy < 0:
                    actor.rect.top = s.bottom
                actor.vy = 0


def draw_world(surf, cam, solids, coins, enemies, flag, player, score, lives, won, dead):
    surf.fill(SKY)
    for i in range(8):
        pygame.draw.ellipse(surf, HILL, (i * 220 - cam % 220 - 80, 340, 260, 180))
    pygame.draw.rect(surf, (120, 210, 255), (0, 0, W, 90))
    for s in solids:
        r = s.move(-cam, 0)
        if r.right < 0 or r.left > W:
            continue
        color = DIRT if s.y > H - TILE * 2 else BRICK
        pygame.draw.rect(surf, color, r)
        pygame.draw.rect(surf, (40, 20, 10), r, 2)
        if color == BRICK:
            pygame.draw.line(surf, (255, 180, 120), (r.x, r.y + 18), (r.right, r.y + 18), 2)
    for c in coins:
        r = c.move(-cam, 0)
        pygame.draw.circle(surf, GOLD, r.center, 9)
        pygame.draw.circle(surf, (255, 255, 200), r.center, 9, 2)
    if flag:
        r = flag.move(-cam, 0)
        pygame.draw.rect(surf, (240, 240, 240), (r.x + 6, r.y, 4, r.h))
        pygame.draw.polygon(surf, FLAG, [(r.x + 10, r.y), (r.x + 42, r.y + 14), (r.x + 10, r.y + 28)])
    for e in enemies:
        r = e.rect.move(-cam, 0)
        pygame.draw.ellipse(surf, CRITTER, r)
        pygame.draw.circle(surf, (20, 10, 0), (r.x + 10, r.y + 10), 3)
        pygame.draw.circle(surf, (20, 10, 0), (r.x + 22, r.y + 10), 3)
    pr = player.rect.move(-cam, 0)
    pygame.draw.rect(surf, PLAYER, pr, border_radius=6)
    pygame.draw.rect(surf, OVERALL, (pr.x, pr.y + 16, pr.w, pr.h - 16), border_radius=4)
    pygame.draw.rect(surf, (255, 220, 180), (pr.x + 8, pr.y + 4, 16, 12))
    font = pygame.font.SysFont("arial", 22, bold=True)
    surf.blit(font.render(f"COINS {score}   LIVES {lives}", True, (20, 20, 40)), (16, 12))
    surf.blit(font.render("PIPE BROS   ElbowOS", True, (20, 40, 80)), (W - 280, 12))
    big = pygame.font.SysFont("arial", 42, bold=True)
    if won:
        msg = big.render("FLAG! STAGE CLEAR", True, (255, 255, 255))
        surf.blit(msg, msg.get_rect(center=(W // 2, H // 2)))
    elif dead:
        msg = big.render("TRY AGAIN  (R)", True, (255, 240, 240))
        surf.blit(msg, msg.get_rect(center=(W // 2, H // 2)))


def reset():
    solids, coins, enemies, flag = parse_level()
    player = Actor(80, 200, 28, 36)
    return solids, coins, enemies, flag, player, 0, False, False


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pipe Bros — ElbowOS")
    clock = pygame.time.Clock()
    solids, coins, enemies, flag, player, score, won, dead = reset()
    lives = 3
    cam = 0
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                solids, coins, enemies, flag, player, score, won, dead = reset()
                lives = 3
        keys = pygame.key.get_pressed()
        if not won and not dead:
            player.vx = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.vx = -SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.vx = SPEED
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and player.on_ground:
                player.vy = JUMP
                player.on_ground = False
            player.vy += GRAV
            player.rect.x += int(player.vx)
            collide_axis(player, solids, "x")
            player.on_ground = False
            player.rect.y += int(player.vy)
            collide_axis(player, solids, "y")
            for coin in coins[:]:
                if player.rect.colliderect(coin):
                    coins.remove(coin)
                    score += 1
            for enemy in enemies[:]:
                enemy.rect.x += int(enemy.vx)
                hit_wall = False
                for s in solids:
                    if enemy.rect.colliderect(s):
                        hit_wall = True
                        break
                if hit_wall:
                    enemy.vx *= -1
                    enemy.rect.x += int(enemy.vx * 2)
                if player.rect.colliderect(enemy.rect):
                    if player.vy > 0 and player.rect.bottom - enemy.rect.top < 18:
                        enemies.remove(enemy)
                        player.vy = JUMP * 0.55
                        score += 2
                    else:
                        lives -= 1
                        if lives <= 0:
                            dead = True
                        else:
                            player.rect.topleft = (80, 200)
                            player.vx = player.vy = 0
                            cam = 0
            if flag and player.rect.colliderect(flag):
                won = True
            if player.rect.top > H + 80:
                lives -= 1
                if lives <= 0:
                    dead = True
                else:
                    player.rect.topleft = (80, 200)
                    player.vx = player.vy = 0
                    cam = 0
        cam = max(0, player.rect.centerx - W // 3)
        draw_world(screen, cam, solids, coins, enemies, flag, player, score, lives, won, dead)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
