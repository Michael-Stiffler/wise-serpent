from .piece import Piece


class Visuals():
    def __init__(self) -> None:
        self.board = []
        self.unicode_dict = {
            Piece.WHITE_PAWN: "♟︎",
            Piece.WHITE_KNIGHT: "♞",
            Piece.WHITE_BISHOP: "♝",
            Piece.WHITE_ROOK: "♜",
            Piece.WHITE_QUEEN: "♛",
            Piece.WHITE_KING: "♚",
            Piece.BLACK_PAWN: "♙",
            Piece.BLACK_KNIGHT: "♘",
            Piece.BLACK_BISHOP: "♗",
            Piece.BLACK_ROOK: "♖",
            Piece.BLACK_QUEEN: "♕",
            Piece.BLACK_KING: "♔"
        }

    def set_board(self, board) -> None:
        self.board = board

    def print_board(self) -> None:

        print("\n")

        for rank in range(8):
            for file in range(8):
                square = rank * 8 + file
                if not file:
                    print("  " + str(8 - rank) + " ", end="")

                print(" " + self.unicode_dict[self.board[square]] if self.board[square] is not None else " -", end="")

            print("")

        print("\n     a b c d e f g h\n\n")
