"""
main.py — entry point for Rush00 (42 Bangkok Python Piscine)

The checkmate() function is imported from checkmate.py.
This file demonstrates the two examples given in the PDF spec
and is the file submitted alongside checkmate.py.
"""

from checkmate import checkmate


def main():
    # ---------------------------------------------------------------
    # Example 1 from the PDF spec
    # Pawn at (2,2) attacks (1,1) and (1,3) → King at (1,1) is hit
    # Expected output: Success
    # ---------------------------------------------------------------
    board = """\
R...
.K..
..P.
....\
"""
    checkmate(board)


if __name__ == "__main__":
    main()
