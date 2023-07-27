from .bitboard import Bitboard
from .board import Board
import numpy as np

SQUARES = [
    A8, B8, C8, D8, E8, F8, G8, H8,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A1, B1, C1, D1, E1, F1, G1, H1,
] = range(64)

SQUARES_TO_COORDS = [
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
]


class MoveGenerator():
    def __init__(self) -> None:
        self.WHITE = 0
        self.BLACK = 1
        self.UNSIGNED_LONG_1 = np.ulonglong(1)
        self.not_h_file = np.ulonglong(9187201950435737471)
        self.not_a_file = np.ulonglong(18374403900871474942)

    def generate_moves(self, bitboard, move_color) -> list:

        moves = []

        pawn_moves = []
        if move_color:
            pawn_moves = self.generate_black_pawn_moves(bitboard)
        else:
            pawn_moves = self.generate_white_pawn_moves(bitboard)
        moves.extend(pawn_moves)

        # bishop_moves = self.generate_bishop_moves(bitboard, move_color)
        # moves.extend(bishop_moves)

        # knight_moves = self.generate_knight_moves(bitboard, move_color)
        # moves.extend(knight_moves)

        # rook_moves = self.generate_rook_moves(bitboard, move_color)
        # moves.extend(rook_moves)

        # queen_moves = self.generate_queen_moves(bitboard, move_color)
        # moves.extend(queen_moves)

        # king_moves = self.generate_king_moves(bitboard, move_color)
        # moves.extend(king_moves)

        return moves

    def generate_white_pawn_moves(self, bitboard: Bitboard) -> list:

        moves = []
        white_pawns = bitboard.white_pawns

        for square in range(64):
            if self.is_piece_on_square(white_pawns, square):
                # Check if pawn can move up one
                move_one_square = square - 8
                if move_one_square > A8 and not self.is_piece_on_square(bitboard.full_board, move_one_square):
                    # check if pawn is promoting
                    if square >= A7 and square <= H7:
                        moves.append(SQUARES_TO_COORDS[move_one_square] + "=Q")
                        moves.append(SQUARES_TO_COORDS[move_one_square] + "=N")
                        moves.append(SQUARES_TO_COORDS[move_one_square] + "=B")
                        moves.append(SQUARES_TO_COORDS[move_one_square] + "=R")
                    else:
                        moves.append(SQUARES_TO_COORDS[move_one_square])
                        # Check if pawn can move up two
                        move_two_squares = move_one_square - 8
                        if (square >= A2 and square <= H2) and not self.is_piece_on_square(bitboard.full_board, move_two_squares):
                            moves.append(SQUARES_TO_COORDS[move_two_squares])

                board = np.uint64(0)
                board = self.set_bit(board, square)
                if ((board >> np.uint64(7)) & self.not_a_file):
                    target_square = self.get_least_sig_bit_index(board >> np.uint64(7))
                    if self.is_piece_on_square(bitboard.black_board, target_square):
                        moves.append(SQUARES_TO_COORDS[square][:-1] + "x" + SQUARES_TO_COORDS[target_square])
                if ((board >> np.uint64(9)) & self.not_h_file):
                    target_square = self.get_least_sig_bit_index(board >> np.uint64(9))
                    if self.is_piece_on_square(bitboard.black_board, target_square):
                        moves.append(SQUARES_TO_COORDS[square][:-1] + "x" + SQUARES_TO_COORDS[target_square])
        return moves

    def generate_black_pawn_moves(self, bitboard: Bitboard) -> list:
        moves = []
        black_pawns = bitboard.black_pawns

        attack_squares = np.uint64(0)
        board = np.uint64(0)
        for square in range(64):
            if self.is_piece_on_square(black_pawns, square):
                # Check if pawn can move up one
                move_one_square = square + 8
                if move_one_square < H1 and not self.is_piece_on_square(bitboard.full_board, move_one_square):
                    # check if pawn is promoting
                    if square >= A2 and square <= H2:
                        moves.append(SQUARES_TO_COORDS[move_one_square] + "=Q")
                        moves.append(SQUARES_TO_COORDS[move_one_square] + "=N")
                        moves.append(SQUARES_TO_COORDS[move_one_square] + "=B")
                        moves.append(SQUARES_TO_COORDS[move_one_square] + "=R")
                    else:
                        moves.append(SQUARES_TO_COORDS[move_one_square])
                        # Check if pawn can move up two
                        move_two_squares = move_one_square + 8
                        if (square >= A7 and square <= H7) and not self.is_piece_on_square(bitboard.full_board, move_two_squares):
                            moves.append(SQUARES_TO_COORDS[move_two_squares])

                board = np.uint64(0)
                board = self.set_bit(board, square)
                if ((board << np.uint64(7)) & self.not_h_file):
                    target_square = self.get_least_sig_bit_index(board << np.uint64(7))
                    if self.is_piece_on_square(bitboard.white_board, target_square):
                        moves.append(SQUARES_TO_COORDS[square][:-1] + "x" + SQUARES_TO_COORDS[target_square])
                if ((board << np.uint64(9)) & self.not_a_file):
                    target_square = self.get_least_sig_bit_index(board << np.uint64(9))
                    if self.is_piece_on_square(bitboard.white_board, target_square):
                        moves.append(SQUARES_TO_COORDS[square][:-1] + "x" + SQUARES_TO_COORDS[target_square])

        return moves

    def generate_bishop_moves(self, bitboard: Bitboard, color_to_move):
        bishops = bitboard.black_bishops if color_to_move else bitboard.white_bishops

    def generate_knight_moves(self, bitboard: Bitboard, color_to_move):
        knights = bitboard.black_knights if color_to_move else bitboard.white_knights

    def generate_rook_moves(self, bitboard: Bitboard, color_to_move):
        rooks = bitboard.black_rooks if color_to_move else bitboard.white_rooks

    def generate_queen_moves(self, bitboard: Bitboard, color_to_move):
        queens = bitboard.black_queens if color_to_move else bitboard.white_queens

    def generate_king_moves(self, bitboard: Bitboard, color_to_move):
        king = bitboard.black_king if color_to_move else bitboard.white_king

    def is_piece_on_square(self, bitboard: np.uint64, square: int) -> bool:
        return bool(np.ulonglong(bitboard) & (self.UNSIGNED_LONG_1 << np.ulonglong(square)))

    def set_bit(self, bitboard: np.uint64, square: int):
        return np.ulonglong(bitboard) | (self.UNSIGNED_LONG_1 << np.ulonglong(square))

    def get_least_sig_bit_index(self, board):
        if board:
            return (int(board) & int(-board)).bit_length()-1
        else:
            return -1
