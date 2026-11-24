# tiny-chess-engine

[![make.fun bounty](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01)
![rank](https://make.fun/badge/tiny-chess-01/mikechen04/tiny-chess-engine/rank.svg)
![reward](https://make.fun/badge/tiny-chess-01/mikechen04/tiny-chess-engine/reward.svg)

Entry for the make.fun bounty: [Build the strongest chess engine in 4 KB of Python](https://make.fun/bounty/tiny-chess-01)

A chess engine in a single Python file of 3,967 bytes, written for the "strongest chess engine in 4 KB of Python" challenge.

- Standard library only, no python-chess.
- Speaks UCI over stdin/stdout, so it works with chess GUIs and engine testers.
- Full legal move generation (castling, en passant, all promotions), checked with perft on standard test positions.
- Search: alpha-beta with iterative deepening, quiescence search, transposition table, null move pruning, late move reductions, killer moves and check extensions.
- Time management from `wtime`/`btime`/`winc`/`binc`, `movetime` or `depth`.

## Run

```
python3 engine.py
```

Then send UCI commands, for example:

```
uci
position startpos moves e2e4
go movetime 2000
```
