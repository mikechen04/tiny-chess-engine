# tiny-chess-engine

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
