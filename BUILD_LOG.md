# Build log

How `engine.py` was built, what was tried, and how it was tested.

## Goal

The strongest chess engine that fits in one Python file of at most 4,096 bytes, using only the standard library. It talks UCI over stdin/stdout so any chess GUI or testing tool can drive it.

## Approach

1. Write a readable version first (about 6.5 KB) and get it correct.
2. Check move generation with perft against known node counts.
3. Rewrite it compactly by hand, keeping the same logic, and re-run perft on the compact file.
4. Play test games to check strength, legality and time use.

## Board representation

- A 120-character string: a 10x12 "mailbox" with two padding rows above and below the board and one padding column on each side. Any move that leaves the board lands on a padding square, so there are no bounds checks.
- The board is always seen from the side to move. After each move it is reversed and the case is swapped (`b[::-1].swapcase()`), so uppercase pieces are always "us" moving up the board. One move generator handles both colors.
- A position is a tuple: board, score, castling rights (ours, then theirs), en passant square.

## Move generation

- Pseudo-legal moves from direction tables, with sliding pieces walking until they hit something.
- Pawns: single and double pushes, captures, en passant and all four promotion pieces.
- Castling is generated from the king, toward either rook. It checks that the squares in between are empty and that the king's start, middle and end squares aren't attacked. The same code works for both colors because the rooks sit on the same two squares in the rotated view.
- An attack function looks outward from a square for enemy pawns, knights, sliders and the king. It's used for check detection, castling and legality filtering.

## Evaluation

- Material plus piece-square values, all built from short formulas instead of stored tables, to save bytes:
  - pawns gain value as they advance, more on central files
  - knights and bishops prefer the center
  - rooks get a bonus on the 7th rank and on central files
  - the king stays back and near the corners in the middlegame
- The score is updated incrementally with each move instead of being recomputed.
- When few pieces are left (fewer than 7 knights, bishops, rooks and queens in total), the king switches to a table that rewards centralization. The switch happens when a new position arrives from the GUI.

## Search

- Negamax alpha-beta with iterative deepening.
- Quiescence search over captures and promotions, with stand-pat.
- A transposition table (a dict keyed by the position tuple) storing depth, score, bound type and best move. It's cleared when it grows past 300,000 entries to cap memory.
- Move ordering: transposition-table move first, then the killer move for that ply, then by how much each move changes the static score. That puts captures of valuable pieces and promotions early.
- Null move pruning (reduction 3) when not in check.
- Late move reductions: quiet moves after the first four are searched one ply shallower with a narrow window, then re-searched at full depth if they look good.
- Check extension: one extra ply when the side to move is in check.
- Repetition detection: positions from the game and from the current search path score as draws.
- Mate and stalemate: the search uses pseudo-legal moves and treats a king capture as a loss. A node where every move loses the king is scored as checkmate if in check (preferring faster mates) and as stalemate otherwise. Root moves are filtered for full legality, so the engine never returns an illegal move.

## Time management

- With a clock: budget = min(time/15 + 0.8 * increment, time/3).
- With `movetime`: 85% of the given time.
- With `depth`: no time limit.
- Time is checked at every node. When the budget runs out, the search aborts and the best move from the last finished depth is played.
- A new depth only starts if less than half the budget has been used.

## Squeezing under 4 KB

- One-letter names, one-space indentation, several statements per line.
- Piece-square tables from formulas instead of literal numbers.
- The start position goes through the same FEN parser as any other position, so no separate board string is needed.
- A small helper for board rotation, used in five places.
- The quiescence filter moved into the move generator.

Final size: **3,967 bytes**.

## Problems found and fixed

- **En passant score**: the readable version used the wrong square index for the pawn captured en passant. Caught while reviewing; fixed before the first perft run.
- **FEN parsing for black to move**: the castling rights and en passant square weren't rotated into black's point of view. Fixed, and covered by the perft test with black to move.
- **Stalemate vs. being mated**: an early version confused "all moves lose the king right now" with "all moves lead to being mated later" and could score a lost position as a draw. Fixed by giving an immediate king capture its own sentinel score.
- **Late move reductions skipping moves**: the first version could leave a node with no score when every reduced search failed low. Restructured so every move's result is counted.
- **Numbers next to keywords**: minified code like `0and` is a syntax error in Python 3.13. Added spaces.
- **Silent search failure**: the attack function returned `None` instead of `0` when nothing attacked a square, which crashed the check-extension math. A catch-all `except` hid the crash, so the engine returned its first legal move instantly. Found by testing with the exception surfaced; fixed. The catch-all stays in the final file as a safety net, so a bug can never stop the engine from answering.
- **No legal moves**: `go` in a checkmate or stalemate position used to crash. It now answers `bestmove 0000`.

## Speed

- Replacing `str.isupper()` / `str.isspace()` calls in the move generator with character comparisons made the generator noticeably faster under profiling. Wall-clock gain was small.
- The engine searches roughly 35,000 nodes per second and reaches depth 6 from the start position in about 1-2 seconds.

## Tests

### Perft (legal move counts)

All match the published numbers:

| Position | Depth | Nodes |
|---|---|---|
| Start position | 1-4 | 20, 400, 8,902, 197,281 |
| Kiwipete | 1-3 | 48, 2,039, 97,862 |
| Position 3 (rook and pawn endgame) | 1-4 | 14, 191, 2,812, 43,238 |
| Position 4 | 1-3 | 6, 264, 9,467 |
| Position 4, mirrored, black to move | 1-3 | 6, 264, 9,467 |
| Position 5 | 1-3 | 44, 1,486, 62,379 |
| Position 6 | 1-3 | 46, 2,079, 89,890 |

### UCI checks

- Answers `uci`, `isready`, `position startpos/fen ... moves ...`, `go` with `wtime/btime/winc/binc`, `movetime` and `depth`, and `quit`.
- Finds mate in one (Scholar's mate with Qxf7#, back-rank mate with Rd8#).
- Promotes correctly for both colors.
- Answers `bestmove 0000` in checkmate and stalemate positions.

### Games

Games were run with a small referee script that checks every move for legality and detects mate, stalemate, repetition, the 50-move rule and insufficient material.

- **Against a random mover**: 10 of 10 wins, all by checkmate, at 10-20 seconds per game plus increment.
- **Bullet (2 seconds for the whole game, no increment)**: no time losses. The most it spent on one move was about 7% of its remaining clock. It did stalemate a random mover once at this speed, because shallow searches can miss stalemate.
- **Time use**: across all test games, no move used more than about a fifth of the remaining clock.

### A variant that was tried and dropped

Principal variation search (null-window searches for every move after the first) was tested against the plain version in two self-play matches: 6/12 and 9/18, an even 15/30 total. It added complexity without a measurable gain, so the simpler version was kept.

## Ideas for more strength

- Pawn structure and king safety terms (hard to fit with incremental scoring).
- Better stalemate avoidance in won endgames.
- Handling `go infinite` / `stop` properly, which would need a thread.
