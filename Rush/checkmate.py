"""
=============================================================
  Checkmate — King-in-Check Detector
  (42 Bangkok Python Piscine — Rush00)
=============================================================

Approach
--------
1. Parse the board string into a 2-D grid and validate it
   (must be non-empty and square NxN).
2. Locate the King (K) — exactly one must exist.
3. For every enemy piece (P, B, R, Q) on the board, check
   whether it can currently attack the King's square.
4. "A piece can only capture the first possible piece that
   stands on its path." → we walk ray-by-ray and stop at
   the first KNOWN piece character (ignoring unknown chars,
   which are treated as empty squares per the spec).
5. Print "Success" if ANY piece threatens the King, else "Fail".

Function breakdown
------------------
  parse_board(board)                            → list[list[str]] | None
  find_king(grid)                               → (row, col) | None
  is_piece(ch)                                  → bool
  first_piece_in_direction(grid, r, c, dr, dc)  → (row, col) | None
  can_pawn_attack(grid, pr, pc, kr, kc)         → bool
  can_bishop_attack(grid, pr, pc, kr, kc)       → bool
  can_rook_attack(grid, pr, pc, kr, kc)         → bool
  can_queen_attack(grid, pr, pc, kr, kc)        → bool
  is_in_check(grid, king_pos)                   → bool
  checkmate(board)                              → None  (prints result)

Edge cases handled
------------------
  * Empty / whitespace-only input
  * Non-square board (rows ≠ cols, or uneven row widths)
  * Zero kings or multiple kings
  * Piece blocked by another piece before reaching the King
  * Pawn at row 0 (attacks row -1 — safely never matches valid King)
  * Unknown characters treated as empty (spec: "all chars not used
    to refer to pieces are considered empty squares")
  * Queen combining both rook + bishop directions
"""

# ---------------------------------------------------------------------------
# Known piece characters (all others are empty squares per the spec)
# ---------------------------------------------------------------------------
PIECES = {'K', 'P', 'B', 'R', 'Q'}


# ---------------------------------------------------------------------------
# 1. Board parsing & validation
# ---------------------------------------------------------------------------

def parse_board(board: str):
    """
    Convert the raw multi-line string into a 2-D list of characters.

    Returns the grid (list of rows) if valid, or None on error.
    A valid board must be:
      - Non-empty
      - Rectangular (all rows same length)
      - Square (number of rows == row length)
    """
    if not board or not board.strip():
        print("Error: empty input.")
        return None

    # Split on newlines, keep rows that are not completely empty
    rows = [line for line in board.splitlines() if line]

    if len(rows) == 0:
        print("Error: board has no content.")
        return None

    width = len(rows[0])

    # All rows must be the same length (rectangular)
    for row in rows:
        if len(row) != width:
            print("Error: board is not rectangular (row lengths differ).")
            return None

    # Must be square: number of rows == number of columns
    if len(rows) != width:
        print(f"Error: board is not square ({len(rows)}x{width}).")
        return None

    # Build 2-D grid
    grid = [list(row) for row in rows]
    return grid


# ---------------------------------------------------------------------------
# 2. Locate the King
# ---------------------------------------------------------------------------

def find_king(grid: list) -> tuple | None:
    """
    Scan the grid and return (row, col) of the King ('K').
    Prints an error and returns None if not exactly one King exists.
    """
    positions = [
        (r, c)
        for r, row in enumerate(grid)
        for c, cell in enumerate(row)
        if cell == 'K'
    ]

    if len(positions) == 0:
        print("Error: no King found on the board.")
        return None
    if len(positions) > 1:
        print(f"Error: multiple Kings found ({len(positions)} kings).")
        return None

    return positions[0]


# ---------------------------------------------------------------------------
# 3. Helper — is a character a known piece?
# ---------------------------------------------------------------------------

def is_piece(ch: str) -> bool:
    """
    Return True if ch is a recognised piece character.

    Per the spec: 'All characters that are not used to refer to pieces
    are considered as empty squares.' So only K, P, B, R, Q block rays.
    """
    return ch in PIECES


# ---------------------------------------------------------------------------
# 4. Helper — first PIECE encountered along a direction
# ---------------------------------------------------------------------------

def first_piece_in_direction(grid: list, start_r: int, start_c: int,
                              dr: int, dc: int) -> tuple | None:
    """
    Walk one step at a time from (start_r, start_c) in direction (dr, dc).
    Return (row, col) of the first PIECE (known piece character) found,
    or None if we reach the board edge without hitting any piece.

    Unknown characters are transparent (treated as empty squares).
    """
    size = len(grid)
    r, c = start_r + dr, start_c + dc

    while 0 <= r < size and 0 <= c < size:
        if is_piece(grid[r][c]):
            return (r, c)          # stop at the first real piece
        r += dr
        c += dc

    return None


# ---------------------------------------------------------------------------
# 5. Individual piece attack checkers
# ---------------------------------------------------------------------------

def can_pawn_attack(grid: list, pr: int, pc: int,
                    kr: int, kc: int) -> bool:
    """
    A Pawn attacks the two squares diagonally UPWARD: (pr-1, pc-1) and
    (pr-1, pc+1).  Pawns are single-step pieces — no ray blocking.

    (PDF diagram confirms: Pawn at centre row r attacks row r-1 diagonals.)
    """
    return (kr, kc) in [(pr - 1, pc - 1), (pr - 1, pc + 1)]


def can_bishop_attack(grid: list, pr: int, pc: int,
                      kr: int, kc: int) -> bool:
    """
    A Bishop slides diagonally in four directions.
    It threatens the King only if the King is the FIRST piece on a diagonal.
    """
    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        if first_piece_in_direction(grid, pr, pc, dr, dc) == (kr, kc):
            return True
    return False


def can_rook_attack(grid: list, pr: int, pc: int,
                    kr: int, kc: int) -> bool:
    """
    A Rook slides horizontally and vertically in four directions.
    It threatens the King only if the King is the FIRST piece on an axis.
    """
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if first_piece_in_direction(grid, pr, pc, dr, dc) == (kr, kc):
            return True
    return False


def can_queen_attack(grid: list, pr: int, pc: int,
                     kr: int, kc: int) -> bool:
    """
    A Queen combines Rook + Bishop movement (8 directions total).
    """
    return (can_rook_attack(grid, pr, pc, kr, kc) or
            can_bishop_attack(grid, pr, pc, kr, kc))


# ---------------------------------------------------------------------------
# 6. Check detector — scan every enemy piece
# ---------------------------------------------------------------------------

# Dispatch table: piece character → its attack function
PIECE_ATTACKS = {
    'P': can_pawn_attack,
    'B': can_bishop_attack,
    'R': can_rook_attack,
    'Q': can_queen_attack,
}


def is_in_check(grid: list, king_pos: tuple) -> bool:
    """
    Iterate every cell.  When an enemy piece is found, test whether it
    currently threatens the King.  Return True on the first attacker found.
    """
    kr, kc = king_pos
    size = len(grid)

    for r in range(size):
        for c in range(size):
            attack_fn = PIECE_ATTACKS.get(grid[r][c])
            if attack_fn and attack_fn(grid, r, c, kr, kc):
                return True   # King is in check — stop immediately

    return False


# ---------------------------------------------------------------------------
# 7. Public entry point
# ---------------------------------------------------------------------------

def checkmate(board: str) -> None:
    """
    Main public function.

    Parses and validates the board, locates the King, then prints:
      "Success" — if the King is currently in check
      "Fail"    — if the King is safe
    On invalid input, prints a descriptive error and returns silently.
    """
    grid = parse_board(board)
    if grid is None:
        return                   # error already printed

    king_pos = find_king(grid)
    if king_pos is None:
        return                   # error already printed

    if is_in_check(grid, king_pos):
        print("Success")
    else:
        print("Fail")


# ===========================================================================
# 8. Test cases
# ===========================================================================

def run_tests():
    """Run all test cases, printing expected vs actual result."""
    sep = "-" * 50

    # ------------------------------------------------------------------
    # Test 1 — EXACT example from the PDF (Example1)
    # Board:   R...     Rook at (0,0), King at (1,1), Pawn at (2,2)
    #          .K..     Pawn (2,2) attacks (1,1) and (1,3) → hits King!
    #          ..P.     Expected: Success
    #          ....
    # ------------------------------------------------------------------
    test1 = (
        "R...\n"
        ".K..\n"
        "..P.\n"
        "...."
    )
    print(sep)
    print("Test 1 — PDF Example1: Pawn attacks King diagonally upward")
    print("Expected: Success")
    print("Got:     ", end="")
    checkmate(test1)

    # ------------------------------------------------------------------
    # Test 2 — PDF Example2: 2×2 board, King only → no enemy pieces
    # Board:   ..     King at (1,1), no enemies
    #          .K     Expected: Fail
    # ------------------------------------------------------------------
    test2 = (
        "..\n"
        ".K"
    )
    print(sep)
    print("Test 2 — PDF Example2: King alone on 2x2 board (no enemies)")
    print("Expected: Fail")
    print("Got:     ", end="")
    checkmate(test2)

    # ------------------------------------------------------------------
    # Test 3 — Rook on same row, clear path
    # Board:   ....
    #          R..K    Rook (1,0) → King (1,3), nothing in between
    #          ....    Expected: Success
    #          ....
    # ------------------------------------------------------------------
    test3 = (
        "....\n"
        "R..K\n"
        "....\n"
        "...."
    )
    print(sep)
    print("Test 3 — Rook attacking King horizontally (clear path)")
    print("Expected: Success")
    print("Got:     ", end="")
    checkmate(test3)

    # ------------------------------------------------------------------
    # Test 4 — Rook blocked by another piece
    # Board:   ....
    #          R.BK    Rook hits B first, cannot reach King
    #          ....    Expected: Fail
    #          ....
    # ------------------------------------------------------------------
    test4 = (
        "....\n"
        "R.BK\n"
        "....\n"
        "...."
    )
    print(sep)
    print("Test 4 — Rook blocked by Bishop (path obstruction)")
    print("Expected: Fail")
    print("Got:     ", end="")
    checkmate(test4)

    # ------------------------------------------------------------------
    # Test 5 — Bishop on TRUE diagonal, clear path
    # Board:   ...K    King (0,3)
    #          ....    Bishop (3,0) → (2,1)→(1,2)→(0,3)=King ✓
    #          ....    Expected: Success
    #          B...
    # ------------------------------------------------------------------
    test5 = (
        "...K\n"
        "....\n"
        "....\n"
        "B..."
    )
    print(sep)
    print("Test 5 — Bishop attacking King diagonally (clear path)")
    print("Expected: Success")
    print("Got:     ", end="")
    checkmate(test5)

    # ------------------------------------------------------------------
    # Test 6 — Bishop NOT on King's diagonal
    # Board:   ....
    #          ...K    King (1,3), Bishop (3,0)
    #          ....    NOT on same diagonal → diagonal from (3,0) goes
    #          B...    to (2,1),(1,2),(0,3) NOT (1,3)
    #                  Expected: Fail
    # ------------------------------------------------------------------
    test6 = (
        "....\n"
        "...K\n"
        "....\n"
        "B..."
    )
    print(sep)
    print("Test 6 — Bishop NOT on King's true diagonal")
    print("Expected: Fail")
    print("Got:     ", end="")
    checkmate(test6)

    # ------------------------------------------------------------------
    # Test 7 — Queen attacks vertically
    # Board:   .K.    King (0,1), Queen (2,1), same column
    #          ...    Expected: Success
    #          .Q.
    # ------------------------------------------------------------------
    test7 = (
        ".K.\n"
        "...\n"
        ".Q."
    )
    print(sep)
    print("Test 7 — Queen attacking King vertically")
    print("Expected: Success")
    print("Got:     ", end="")
    checkmate(test7)

    # ------------------------------------------------------------------
    # Test 8 — Queen attacks diagonally
    # Board:   Q...    Queen (0,0), King (2,2) — diagonal ✓
    #          ....    Expected: Success
    #          ..K.
    #          ....
    # ------------------------------------------------------------------
    test8 = (
        "Q...\n"
        "....\n"
        "..K.\n"
        "...."
    )
    print(sep)
    print("Test 8 — Queen attacking King diagonally")
    print("Expected: Success")
    print("Got:     ", end="")
    checkmate(test8)

    # ------------------------------------------------------------------
    # Test 9 — Pawn BELOW King (Pawn attacks upward only → no threat)
    # Board:   ....
    #          ..K.    King (1,2), Pawn (0,1)
    #          .P..    Pawn at (2,1) attacks (1,0) and (1,2) → hits King!
    #          ....    Wait — this IS a hit. Let me use Pawn below King.
    #
    # Correction: Pawn at (0,1) attacks (-1,0) and (-1,2) — off board.
    # Use Pawn at (3,1), King at (1,2) — Pawn attacks (2,0) and (2,2),
    # NOT the king. Expected: Fail
    # Board:   ....
    #          ..K.
    #          ....
    #          .P..
    # ------------------------------------------------------------------
    test9 = (
        "....\n"
        "..K.\n"
        "....\n"
        ".P.."
    )
    print(sep)
    print("Test 9 — Pawn too far below King (cannot reach)")
    print("Expected: Fail")
    print("Got:     ", end="")
    checkmate(test9)

    # ------------------------------------------------------------------
    # Test 10 — Pawn one row below King, adjacent column → attacks King
    # Board:   ....
    #          ..K.    King (1,2)
    #          .P..    Pawn (2,1) attacks (1,0) and (1,2) → King at (1,2)!
    #          ....    Expected: Success
    # ------------------------------------------------------------------
    test10 = (
        "....\n"
        "..K.\n"
        ".P..\n"
        "...."
    )
    print(sep)
    print("Test 10 — Pawn one step below King, on diagonal (attacks)")
    print("Expected: Success")
    print("Got:     ", end="")
    checkmate(test10)

    # ------------------------------------------------------------------
    # Test 11 — No enemy pieces at all
    # ------------------------------------------------------------------
    test11 = (
        "....\n"
        ".K..\n"
        "....\n"
        "...."
    )
    print(sep)
    print("Test 11 — King alone, no enemies")
    print("Expected: Fail")
    print("Got:     ", end="")
    checkmate(test11)

    # ------------------------------------------------------------------
    # Test 12 — Unknown characters treated as empty (not blocking!)
    # Board:   R x x K    x = unknown chars (treated as empty)
    # Rook at (0,0) should still reach King at (0,3)
    # Expected: Success
    # ------------------------------------------------------------------
    test12 = (
        "RxxK\n"
        "xxxx\n"
        "xxxx\n"
        "xxxx"
    )
    print(sep)
    print("Test 12 — Unknown chars are transparent (not blocking rays)")
    print("Expected: Success")
    print("Got:     ", end="")
    checkmate(test12)

    # ------------------------------------------------------------------
    # Invalid input tests
    # ------------------------------------------------------------------
    print(sep)
    print("Test 13 — Non-square board")
    print("Expected: Error message")
    print("Got:     ", end="")
    checkmate("KR\nP")

    print(sep)
    print("Test 14 — Empty string")
    print("Expected: Error message")
    print("Got:     ", end="")
    checkmate("")

    print(sep)
    print("Test 15 — No King on board")
    print("Expected: Error message")
    print("Got:     ", end="")
    checkmate("R..\n...\n...")

    print(sep)
    print("Test 16 — Multiple Kings")
    print("Expected: Error message")
    print("Got:     ", end="")
    checkmate("K.K\n...\n...")

    print(sep)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_tests()
