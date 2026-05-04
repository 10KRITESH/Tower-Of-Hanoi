#!/usr/bin/env python3
"""
Tower of Hanoi - ASCII Visualizer
==================================
Coding Challenge: RISC-V High Precision Code Base and Reach (LFX Mentorship)

Demonstrates:
  - RECURSION  : solve() calls itself with a reduced subproblem (n-1 disks)
  - ITERATION  : the main loop iterates over every recorded move to render frames
  - Simple ASCII graphics rendered entirely in the terminal

Author : 10KRITESH
"""

import os
import time
import sys

# ─── Configuration ────────────────────────────────────────────────────────────
NUM_DISKS   = 5          # change this to try more / fewer disks
DELAY       = 0.45       # seconds between frames (set 0 for instant)
ROD_HEIGHT  = NUM_DISKS + 2
ROD_NAMES   = ["A", "B", "C"]
# ──────────────────────────────────────────────────────────────────────────────


# ─── RECURSION ────────────────────────────────────────────────────────────────
def solve(n: int, source: str, target: str, aux: str, moves: list) -> None:
    """
    Classic recursive Tower of Hanoi solver.

    Base case  : n == 0  → nothing to move, return immediately.
    Recursive  :
      1. Move (n-1) disks from source → aux   (using target as buffer)
      2. Move the largest disk from source → target
      3. Move (n-1) disks from aux → target   (using source as buffer)

    Each call reduces the problem size by 1, guaranteeing termination.
    Total moves generated = 2^n - 1.
    """
    if n == 0:
        return                               # ← base case (stops recursion)

    solve(n - 1, source, aux, target, moves) # ← recurse: free the bottom disk
    moves.append((source, target))           # ← record the actual move
    solve(n - 1, aux, target, source, moves) # ← recurse: stack onto target
# ──────────────────────────────────────────────────────────────────────────────


# ─── ASCII Renderer ───────────────────────────────────────────────────────────
def draw(pegs: dict, move_num: int, total: int, last_move: tuple | None) -> None:
    """Render the current peg state as ASCII art."""
    os.system("clear" if os.name == "posix" else "cls")

    disk_width = NUM_DISKS * 2 + 1   # widest disk determines column width
    col_w      = disk_width + 4

    # header
    print("\n  🗼  Tower of Hanoi  —  {} disk{}".format(
        NUM_DISKS, "s" if NUM_DISKS > 1 else ""))
    if last_move:
        print("  Move {:>3} / {}   :   {} → {}".format(
            move_num, total, last_move[0], last_move[1]))
    else:
        print("  Initial state")
    print()

    # build each row top-to-bottom
    for row in range(ROD_HEIGHT - 1, -1, -1):
        line = "  "
        for rod in ROD_NAMES:
            stack = pegs[rod]
            # The disk at this row (0 = bottom of stack)
            disk_idx = row  # row 0 is the base; stack[0] is bottom disk
            if disk_idx < len(stack):
                size = stack[disk_idx]          # disk size (1 = smallest)
                filled = size * 2 - 1
                pad    = (disk_width - filled) // 2
                segment = " " * pad + "█" * filled + " " * pad
            else:
                # empty row — just show the pole
                pole_pos = disk_width // 2
                segment  = " " * pole_pos + "│" + " " * (disk_width - pole_pos - 1)
            line += segment.center(col_w)
        print(line)

    # base line
    print("  " + ("═" * col_w * 3))

    # rod labels
    label_line = "  "
    for rod in ROD_NAMES:
        label_line += rod.center(col_w)
    print(label_line + "\n")
# ──────────────────────────────────────────────────────────────────────────────


def main() -> None:
    # ── Collect all moves via recursion ──────────────────────────────────────
    moves: list[tuple[str, str]] = []
    solve(NUM_DISKS, "A", "C", "B", moves)
    total = len(moves)   # always 2^NUM_DISKS - 1

    # ── Set up initial peg state ──────────────────────────────────────────────
    # Pegs store disks bottom-to-top; disk size = NUM_DISKS (biggest) … 1 (smallest)
    pegs: dict[str, list[int]] = {
        "A": list(range(NUM_DISKS, 0, -1)),  # all disks on A, big→small (bottom→top)
        "B": [],
        "C": [],
    }

    # ── ITERATION: replay moves and render each frame ─────────────────────────
    draw(pegs, 0, total, None)
    time.sleep(DELAY * 2)

    for i, (src, tgt) in enumerate(moves, start=1):   # ← iterates over every move
        disk = pegs[src].pop()          # take top disk from source
        pegs[tgt].append(disk)          # place it on target
        draw(pegs, i, total, (src, tgt))
        time.sleep(DELAY)

    print("  ✅  Solved in {} moves  (2^{} − 1)\n".format(total, NUM_DISKS))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  Interrupted.")
        sys.exit(0)
