import numpy as np


class Bitboard():
    def __init__(self) -> None:
        self.UNSIGNED_LONG_1 = np.ulonglong()

        self.white_pawns = np.uint64(0)
        self.black_pawns = np.uint64(0)
        self.white_knights = np.uint64(0)
        self.black_knights = np.uint64(0)
        self.white_bishops = np.uint64(0)
        self.black_bishops = np.uint64(0)
        self.white_rooks = np.uint64(0)
        self.black_rooks = np.uint64(0)
        self.white_queens = np.uint64(0)
        self.black_queens = np.uint64(0)
        self.white_king = np.uint64(0)
        self.black_king = np.uint64(0)
        self.full_board = np.uint64(0)
        self.white_board = np.uint64(0)
        self.black_board = np.uint64(0)

    def generate_bitboards_from_fen(self, fen) -> None:
        self.white_pawns = fen["white_pawns"]
        self.black_pawns = fen["black_pawns"]
        self.white_knights = fen["white_knights"]
        self.black_knights = fen["black_knights"]
        self.white_bishops = fen["white_bishops"]
        self.black_bishops = fen["black_bishops"]
        self.white_rooks = fen["white_rooks"]
        self.black_rooks = fen["black_rooks"]
        self.white_queens = fen["white_queens"]
        self.black_queens = fen["black_queens"]
        self.white_king = fen["white_king"]
        self.black_king = fen["black_king"]
        self.full_board = fen["full_board"]
        self.white_board = fen["white_board"]
        self.black_board = fen["black_board"]
