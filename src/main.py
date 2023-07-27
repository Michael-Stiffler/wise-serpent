import argparse
from serpent.serpent import Serpent


def main() -> None:
    args = get_args()

    serpent = Serpent()
    serpent.parse_args(args)
    serpent.start_serpent()


def get_args() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-fen', '-f', '--fen', '--f',
                        dest='fen',
                        type=str,
                        help='FEN used to populate the board. Try "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" for the start position.')
    return parser.parse_args()


if __name__ == "__main__":
    main()
