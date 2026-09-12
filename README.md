# ElbowOS Full-Colour Python 3 Games

A pack of **distinct**, standalone **Python 3 + pygame** games. Every title uses a full-colour window (not a text-only terminal). Featured project: **[x.com/ElbowOS](https://x.com/ElbowOS)**.

This is **not** a Nintendo emulator and does not load ROM files. `pipe_bros.py` is an original side-scrolling platformer in the classic plumber-jumps-on-critters style.

## Games

| File | Genre | How to play |
|---|---|---|
| `games/pipe_bros.py` | Mario-style platformer | Arrows / A D move, Space / W / Up jump. Stomp critters, grab coins, reach the flag. |
| `games/royal_baccarat.py` | Casino | Click Player / Banker / Tie, then Deal. |
| `games/video_poker.py` | Casino cards | Bet, deal, click cards to hold, draw. |
| `games/card_war.py` | Card game | Click PLAY. Higher rank wins the pile. |
| `games/neon_tetris.py` | Puzzle | Arrows move / rotate, Down soft drop, Space hard drop. |
| `games/lucky_keno.py` | Casino | Pick up to 10 numbers, click DRAW. |
| `games/frog_dash.py` | Arcade | Arrows hop the frog across traffic and river. |

## Run

```bash
python3 -m pip install -r requirements.txt
python3 launcher.py
```

Or run one game directly:

```bash
python3 games/pipe_bros.py
```

Needs Python 3.10+ and a desktop display (pygame / SDL).

## Links

- GitHub: https://github.com/ApacheAde/ElbowOS-Full-Color-Games
- ElbowOS on X: https://x.com/ElbowOS

MIT licensed. Original art and rules — no copyrighted sprites or ROMs.
