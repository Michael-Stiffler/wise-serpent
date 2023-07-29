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
        self.not_hg_file = np.ulonglong(4557430888798830399)
        self.not_ab_file = np.ulonglong(18229723555195321596)

    def generate_moves(self, bitboard, move_color) -> list:

        moves = []

        pawn_moves = []
        if move_color:
            pawn_moves = self.generate_black_pawn_moves(bitboard)
        else:
            pawn_moves = self.generate_white_pawn_moves(bitboard)
        moves.extend(pawn_moves)

        bishop_moves = self.generate_bishop_moves(bitboard, move_color, is_queen=False)
        moves.extend(bishop_moves)

        knight_moves = self.generate_knight_moves(bitboard, move_color)
        moves.extend(knight_moves)

        rook_moves = self.generate_rook_moves(bitboard, move_color, is_queen=False)
        moves.extend(rook_moves)

        queen_moves = self.generate_queen_moves(bitboard, move_color)
        moves.extend(queen_moves)

        king_moves = self.generate_king_moves(bitboard, move_color)
        moves.extend(king_moves)

        return moves

    # TODO: parameterize this somehow
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

    # TODO: parameterize this somehow
    def generate_black_pawn_moves(self, bitboard: Bitboard) -> list:

        moves = []
        black_pawns = bitboard.black_pawns

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

    def generate_bishop_moves(self, bitboard: Bitboard, color_to_move: bool, is_queen: bool) -> list:
        moves = []
        piece_letter = ""
        # Queen can use the same exact algorithm
        if is_queen:
            bishops = bitboard.black_queens if color_to_move else bitboard.white_queens
            piece_letter = "Q"
        else:
            bishops = bitboard.black_bishops if color_to_move else bitboard.white_bishops
            piece_letter = "B"

        opponent_pieces = bitboard.white_board if color_to_move else bitboard.black_board

        bishop_diagonal_ne_sw = 7
        bishop_diagonal_nw_se = 9

        for square in range(64):
            if self.is_piece_on_square(bishops, square):

                # Check southeast diagonal until we hit the edge of the board or a friendly piece
                moves.extend(self.calculate_bishop_bitboard_moves(
                    square=square,
                    diagonal=bishop_diagonal_nw_se,
                    file=self.not_a_file,
                    left_shift=True,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter=piece_letter,
                    subtract=False
                ))

                # Check northwest diagonal until we hit the edge of the board or a friendly piece
                moves.extend(self.calculate_bishop_bitboard_moves(
                    square=square,
                    diagonal=bishop_diagonal_nw_se,
                    file=self.not_h_file,
                    left_shift=False,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter=piece_letter,
                    subtract=True
                ))

                # Check southwest diagonal until we hit the edge of the board or a friendly piece
                moves.extend(self.calculate_bishop_bitboard_moves(
                    square=square,
                    diagonal=bishop_diagonal_ne_sw,
                    file=self.not_h_file,
                    left_shift=True,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter=piece_letter,
                    subtract=False
                ))

                # Check northeast diagonal until we hit the edge of the board or a friendly piece
                moves.extend(self.calculate_bishop_bitboard_moves(
                    square=square,
                    diagonal=bishop_diagonal_ne_sw,
                    file=self.not_a_file,
                    left_shift=False,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter=piece_letter,
                    subtract=True
                ))

        return moves

    def generate_knight_moves(self, bitboard: Bitboard, color_to_move: int) -> list:
        moves = []
        knights = bitboard.black_knights if color_to_move else bitboard.white_knights
        opponent_pieces = bitboard.white_board if color_to_move else bitboard.black_board

        for square in range(64):
            if self.is_piece_on_square(knights, square):
                board = np.uint64(0)
                board = self.set_bit(board, square)

                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=17, file=self.not_h_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N"))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=15, file=self.not_a_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N"))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=10, file=self.not_hg_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N"))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=6, file=self.not_ab_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N"))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=17, file=self.not_a_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N"))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=15, file=self.not_h_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N"))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=10, file=self.not_ab_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N"))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=6, file=self.not_hg_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N"))

        return [move for move in moves if move is not None]

    def generate_rook_moves(self, bitboard: Bitboard, color_to_move: bool, is_queen: bool) -> list:
        moves = []
        piece_letter = ""
        # Queen can use the same exact algorithm
        if is_queen:
            rooks = bitboard.black_queens if color_to_move else bitboard.white_queens
            piece_letter = "Q"
        else:
            rooks = bitboard.black_rooks if color_to_move else bitboard.white_rooks
            piece_letter = "R"

        opponent_pieces = bitboard.white_board if color_to_move else bitboard.black_board

        for square in range(64):
            if self.is_piece_on_square(rooks, square):
                board = np.uint64(0)
                board = self.set_bit(board, square)

                shift_amount = 1

                # Check right horizontal
                while True:
                    move = self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=shift_amount, file=self.not_a_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter=piece_letter)
                    if move:
                        moves.append(move)
                        if "x" in move:
                            break
                        shift_amount += 1

                    else:
                        break

                shift_amount = 1
                # Check left horizontal
                while True:
                    move = self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=shift_amount, file=self.not_h_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter=piece_letter)
                    if move:
                        moves.append(move)
                        if "x" in move:
                            break
                        shift_amount += 1
                    else:
                        break

                shift_amount = 8
                # Check up
                while True:
                    move = self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=shift_amount, file=self.not_h_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter=piece_letter)
                    if move:
                        moves.append(move)
                        if "x" in move:
                            break
                        shift_amount += 8
                    else:
                        break

                shift_amount = 8
                # Check down
                while True:
                    move = self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=shift_amount, file=self.not_a_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter=piece_letter)
                    if move:
                        moves.append(move)
                        if "x" in move:
                            break
                        shift_amount += 8
                    else:
                        break

        return [move for move in moves if move is not None]

    def calculate_bishop_bitboard_moves(self, square: int, file: int, left_shift: bool, diagonal: int, opponent_pieces: np.uint64, full_board: np.uint64, piece_letter: str, subtract: bool) -> list:
        moves = []

        new_square = square
        while True:
            target_square = 0
            board = np.uint64(0)
            board = self.set_bit(board, new_square)

            if left_shift:
                if ((board << np.uint64(diagonal)) & file):
                    target_square = self.get_least_sig_bit_index(board << np.uint64(diagonal))
            else:
                if ((board >> np.uint64(diagonal)) & file):
                    target_square = self.get_least_sig_bit_index(board >> np.uint64(diagonal))

            if target_square == 0:
                break

            if self.is_piece_on_square(opponent_pieces, target_square):
                moves.append(piece_letter + "x" + SQUARES_TO_COORDS[target_square])
                break
            elif not self.is_piece_on_square(full_board, target_square):
                if subtract:
                    new_square = new_square - diagonal
                else:
                    new_square = new_square + diagonal
                moves.append(piece_letter + SQUARES_TO_COORDS[new_square])
            else:
                break

        return moves

    def calculate_rook_knight_king_bitboard_moves(self, board: np.uint64, shift_amount: int, file: np.uint64, left_shift: bool, opponent_pieces: np.uint64, full_board: np.uint64, piece_letter: str) -> str:
        target_square = 0

        if left_shift:
            if file == 0 or ((board << np.uint64(shift_amount)) & file):
                target_square = self.get_least_sig_bit_index(board << np.uint64(shift_amount))
        else:
            if file == 0 or ((board >> np.uint64(shift_amount)) & file):
                target_square = self.get_least_sig_bit_index(board >> np.uint64(shift_amount))

        if target_square == 0:
            return None

        if self.is_piece_on_square(opponent_pieces, target_square):
            return (piece_letter + "x" + SQUARES_TO_COORDS[target_square])
        elif not self.is_piece_on_square(full_board, target_square):
            return (piece_letter + SQUARES_TO_COORDS[target_square])
        else:
            return None

    def generate_queen_moves(self, bitboard: Bitboard, color_to_move: bool) -> list:
        moves = []

        moves.extend(self.generate_rook_moves(bitboard=bitboard, color_to_move=color_to_move, is_queen=True))
        moves.extend(self.generate_bishop_moves(bitboard=bitboard, color_to_move=color_to_move, is_queen=True))

        return moves

    def generate_king_moves(self, bitboard: Bitboard, color_to_move: bool) -> list:
        moves = []
        king = bitboard.black_king if color_to_move else bitboard.white_king
        opponent_pieces = bitboard.white_board if color_to_move else bitboard.black_board

        # TODO: There is only one king, no need to check all 64 squares
        for square in range(64):
            if self.is_piece_on_square(king, square):
                board = np.uint64(0)
                board = self.set_bit(board, square)

                # up
                if square > H8:
                    moves.append(self.calculate_rook_knight_king_bitboard_moves(
                        board=board,
                        shift_amount=8,
                        file=np.uint64(0),
                        left_shift=False,
                        opponent_pieces=opponent_pieces,
                        full_board=bitboard.full_board,
                        piece_letter="K"
                    ))

                # down
                if square < A1:
                    moves.append(self.calculate_rook_knight_king_bitboard_moves(
                        board=board,
                        shift_amount=8,
                        file=np.uint64(0),
                        left_shift=True,
                        opponent_pieces=opponent_pieces,
                        full_board=bitboard.full_board,
                        piece_letter="K"
                    ))

                # west
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=1,
                    file=self.not_h_file,
                    left_shift=False,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K"
                ))

                # northwest
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=9,
                    file=self.not_h_file,
                    left_shift=False,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K"
                ))

                # northeast
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=7,
                    file=self.not_a_file,
                    left_shift=False,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K"
                ))

                # east
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=1,
                    file=self.not_a_file,
                    left_shift=True,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K"
                ))

                # southeast
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=9,
                    file=self.not_a_file,
                    left_shift=True,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K"
                ))

                # southwest
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=7,
                    file=self.not_h_file,
                    left_shift=True,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K"
                ))

        return [move for move in moves if move is not None]

    def is_piece_on_square(self, bitboard: np.uint64, square: int) -> bool:
        return bool(np.ulonglong(bitboard) & (self.UNSIGNED_LONG_1 << np.ulonglong(square)))

    def set_bit(self, bitboard: np.uint64, square: int) -> np.uint64:
        return np.ulonglong(bitboard) | (self.UNSIGNED_LONG_1 << np.ulonglong(square))

    def get_least_sig_bit_index(self, board: np.uint64) -> int:
        if board:
            return (int(board) & int(-board)).bit_length()-1
        else:
            return -1
