# Tower of Hanoi — ASCII Visualizer

A terminal-based Tower of Hanoi solver with live ASCII animation, written in Python 3.  
Built as a coding challenge submission for the **LFX Mentorship — Broadening the RISC-V High Precision Code Base and Reach** program.

---

## Demo

**Initial state** — all disks on peg A:
```
  Tower of Hanoi  --  5 disks
  Initial state

         |              |              |       
         |              |              |       
         #              |              |       
        ###             |              |       
       #####            |              |       
      #######           |              |       
     #########          |              |       
  =============================================
         A              B              C       
```

**Final state** — all disks moved to peg C:
```
  Tower of Hanoi  --  5 disks
  Move  31 / 31   :   A -> C

         |              |              |       
         |              |              |       
         |              |              #       
         |              |             ###      
         |              |            #####     
         |              |           #######    
         |              |          #########   
  =============================================
         A              B              C       

  Solved in 31 moves  (2^5 - 1)
```

---

## Features

- **Recursive solver** — classic divide-and-conquer algorithm
- **Iterative animation** — replays every move frame-by-frame in the terminal
- **Pure stdlib** — no dependencies, just Python 3
- Configurable number of disks and animation speed

---

## Getting Started

**Requirements:** Python 3.10+

```bash
git clone https://github.com/10KRITESH/tower-of-hanoi
cd tower-of-hanoi
python3 tower_of_hanoi.py
```

---

## Configuration

At the top of `tower_of_hanoi.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `NUM_DISKS` | `5` | Number of disks (try 3–8) |
| `DELAY` | `0.45` | Seconds between frames (`0` for instant) |

---

## How It Works

### Recursion — `solve()`

The solver uses the standard recursive approach:

1. Move `n-1` disks from `source` → `aux`
2. Move the bottom disk from `source` → `target`
3. Move `n-1` disks from `aux` → `target`

The base case (`n == 0`) stops the recursion. Total moves generated = **2^n − 1**.

```python
def solve(n, source, target, aux, moves):
    if n == 0:
        return
    solve(n - 1, source, aux, target, moves)
    moves.append((source, target))
    solve(n - 1, aux, target, source, moves)
```

### Iteration — `main()`

After collecting all moves via recursion, the main loop iterates over them one by one, updating peg state and rendering each frame:

```python
for i, (src, tgt) in enumerate(moves, start=1):
    disk = pegs[src].pop()
    pegs[tgt].append(disk)
    draw(pegs, i, total, (src, tgt))
```

---

## Author

**Kritesh Goud** — [@10KRITESH](https://github.com/10KRITESH)