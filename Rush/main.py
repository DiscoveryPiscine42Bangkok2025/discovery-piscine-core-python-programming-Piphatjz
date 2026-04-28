import sys
from checkmate import checkmate


def main():
    if len(sys.argv) < 2:
        return

    for arg in sys.argv[1:]:
        try:
            with open(arg, 'r') as f:
                board = f.read()
            if not board.strip():
                print("Error")
            else:
                checkmate(board)
        except Exception:
            print("Error")


if __name__ == "__main__":
    main()