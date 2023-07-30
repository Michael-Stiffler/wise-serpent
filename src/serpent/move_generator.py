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


class MoveInfo():
    def __init__(self, source: int, target: int, is_capture: bool, promotion: str, piece: str, en_passant_square: int, is_castle: bool) -> None:
        self.source = source
        self.target = target
        self.is_capture = is_capture
        self.promotion = promotion
        self.piece = piece
        self.en_passant_square = en_passant_square
        self.is_castle = is_castle


class MoveGenerator():
    def __init__(self) -> None:
        self.WHITE = 0
        self.BLACK = 1
        self.UNSIGNED_LONG_1 = np.ulonglong(1)
        self.not_h_file = np.ulonglong(9187201950435737471)
        self.not_a_file = np.ulonglong(18374403900871474942)
        self.not_hg_file = np.ulonglong(4557430888798830399)
        self.not_ab_file = np.ulonglong(18229723555195321596)

    def verify_moves(self, bitboard: Bitboard, color_to_move: int, moves: list) -> list:
        verified_moves = []

        for move in moves:
            if self.is_friendly_king_in_check_after_move(move, bitboard, color_to_move):
                moves.remove(move)
            pass
            # check if move is legal
            # check if YOUR king is in check
            # check if move results in check
            # check if other pieces can get to the same square

        return verified_moves

    def generate_moves(self, bitboard: Bitboard, board: Board) -> list:

        moves = []
        pawn_moves = []
        move_color = board.color_to_move

        if move_color:
            pawn_moves = self.generate_black_pawn_moves(bitboard, board)
        else:
            pawn_moves = self.generate_white_pawn_moves(bitboard, board)
        moves.extend(pawn_moves)

        bishop_moves = self.generate_bishop_moves(bitboard, move_color, is_queen=False)
        moves.extend(bishop_moves)

        knight_moves = self.generate_knight_moves(bitboard, move_color)
        moves.extend(knight_moves)

        rook_moves = self.generate_rook_moves(bitboard, move_color, is_queen=False)
        moves.extend(rook_moves)

        queen_moves = self.generate_queen_moves(bitboard, move_color)
        moves.extend(queen_moves)

        king_moves = self.generate_king_moves(bitboard, board, move_color)
        moves.extend(king_moves)

        return moves

    # TODO: parameterize this somehow
    def generate_white_pawn_moves(self, bitboard: Bitboard, board: Board) -> list:

        moves = []
        white_pawns = bitboard.white_pawns

        for square in range(64):
            if self.is_piece_on_square(white_pawns, square):
                # Check if pawn can move up one
                move_one_square = square - 8
                if move_one_square > A8 and not self.is_piece_on_square(bitboard.full_board, move_one_square):
                    # check if pawn is promoting
                    if square >= A7 and square <= H7:
                        moves.append(MoveInfo(target=move_one_square, source=square, is_capture=False, promotion="Q", piece="P", en_passant_square=None, is_castle=False))
                        moves.append(MoveInfo(target=move_one_square, source=square, is_capture=False, promotion="N", piece="P", en_passant_square=None, is_castle=False))
                        moves.append(MoveInfo(target=move_one_square, source=square, is_capture=False, promotion="B", piece="P", en_passant_square=None, is_castle=False))
                        moves.append(MoveInfo(target=move_one_square, source=square, is_capture=False, promotion="R", piece="P", en_passant_square=None, is_castle=False))
                    else:
                        moves.append(MoveInfo(target=move_one_square, source=square, is_capture=False, promotion=None, piece="P", en_passant_square=None, is_castle=False))
                        # Check if pawn can move up two
                        move_two_squares = move_one_square - 8
                        if (square >= A2 and square <= H2) and not self.is_piece_on_square(bitboard.full_board, move_two_squares):
                            moves.append(MoveInfo(target=move_two_squares, source=square, is_capture=False, promotion=None, piece="P", en_passant_square=move_one_square, is_castle=False))

                board = np.uint64(0)
                board = self.set_bit(board, square)
                if ((board >> np.uint64(7)) & self.not_a_file):
                    target_square = self.get_least_sig_bit_index(board >> np.uint64(7))
                    if self.is_piece_on_square(bitboard.black_board, target_square):
                        moves.append(MoveInfo(target=target_square, source=square, is_capture=True, promotion=None, piece="P", en_passant_square=None, is_castle=False))
                    elif target_square == board.en_passant_target_square:
                        moves.append(MoveInfo(target=target_square, source=square, is_capture=True, promotion=None, piece="P", en_passant_square=None, is_castle=False))
                if ((board >> np.uint64(9)) & self.not_h_file):
                    target_square = self.get_least_sig_bit_index(board >> np.uint64(9))
                    if self.is_piece_on_square(bitboard.black_board, target_square):
                        moves.append(MoveInfo(target=target_square, source=square, is_capture=True, promotion=None, piece="P", en_passant_square=None, is_castle=False))
                    elif target_square == board.en_passant_target_square:
                        moves.append(MoveInfo(target=target_square, source=square, is_capture=True, promotion=None, piece="P", en_passant_square=None, is_castle=False))
        return moves

    # TODO: parameterize this somehow
    def generate_black_pawn_moves(self, bitboard: Bitboard, board: Board) -> list:

        moves = []
        black_pawns = bitboard.black_pawns

        for square in range(64):
            if self.is_piece_on_square(black_pawns, square):
                # Check if pawn can move up one
                move_one_square = square + 8
                if move_one_square < H1 and not self.is_piece_on_square(bitboard.full_board, move_one_square):
                    # check if pawn is promoting
                    if square >= A2 and square <= H2:
                        moves.append(MoveInfo(target=move_one_square, source=square, is_capture=False, promotion="Q", piece="P", en_passant_square=None, is_castle=False))
                        moves.append(MoveInfo(target=move_one_square, source=square, is_capture=False, promotion="N", piece="P", en_passant_square=None, is_castle=False))
                        moves.append(MoveInfo(target=move_one_square, source=square, is_capture=False, promotion="B", piece="P", en_passant_square=None, is_castle=False))
                        moves.append(MoveInfo(target=move_one_square, source=square, is_capture=False, promotion="R", piece="P", en_passant_square=None, is_castle=False))
                    else:
                        moves.append(MoveInfo(target=move_one_square, source=square, is_capture=False, promotion=None, piece="P", en_passant_square=None, is_castle=False))
                        # Check if pawn can move up two
                        move_two_squares = move_one_square + 8
                        if (square >= A7 and square <= H7) and not self.is_piece_on_square(bitboard.full_board, move_two_squares):
                            moves.append(MoveInfo(target=move_two_squares, source=square, is_capture=False, promotion=None, piece="P", en_passant_square=move_one_square, is_castle=False))

                board = np.uint64(0)
                board = self.set_bit(board, square)
                if ((board << np.uint64(7)) & self.not_h_file):
                    target_square = self.get_least_sig_bit_index(board << np.uint64(7))
                    if self.is_piece_on_square(bitboard.white_board, target_square):
                        moves.append(MoveInfo(target=target_square, source=square, is_capture=True, promotion=None, piece="P", en_passant_square=None, is_castle=False))
                    elif target_square == board.en_passant_target_square:
                        moves.append(MoveInfo(target=target_square, source=square, is_capture=True, promotion=None, piece="P", en_passant_square=None, is_castle=False))
                if ((board << np.uint64(9)) & self.not_a_file):
                    target_square = self.get_least_sig_bit_index(board << np.uint64(9))
                    if self.is_piece_on_square(bitboard.white_board, target_square):
                        moves.append(MoveInfo(target=target_square, source=square, is_capture=True, promotion=None, piece="P", en_passant_square=None, is_castle=False))
                    elif target_square == board.en_passant_target_square:
                        moves.append(MoveInfo(target=target_square, source=square, is_capture=True, promotion=None, piece="P", en_passant_square=None, is_castle=False))
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

                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=17, file=self.not_h_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N", source_square=square))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=15, file=self.not_a_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N", source_square=square))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=10, file=self.not_hg_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N", source_square=square))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=6, file=self.not_ab_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N", source_square=square))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=17, file=self.not_a_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N", source_square=square))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=15, file=self.not_h_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N", source_square=square))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=10, file=self.not_ab_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N", source_square=square))
                moves.append(self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=6, file=self.not_hg_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter="N", source_square=square))

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
                    move = self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=shift_amount, file=self.not_a_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter=piece_letter, source_square=square)
                    if move:
                        moves.append(move)
                        if move.is_capture:
                            break
                        shift_amount += 1

                    else:
                        break

                shift_amount = 1
                # Check left horizontal
                while True:
                    move = self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=shift_amount, file=self.not_h_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter=piece_letter, source_square=square)
                    if move:
                        moves.append(move)
                        if move.is_capture:
                            break
                        shift_amount += 1
                    else:
                        break

                shift_amount = 8
                # Check up
                while True:
                    move = self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=shift_amount, file=self.not_h_file, left_shift=False, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter=piece_letter, source_square=square)
                    if move:
                        moves.append(move)
                        if move.is_capture:
                            break
                        shift_amount += 8
                    else:
                        break

                shift_amount = 8
                # Check down
                while True:
                    move = self.calculate_rook_knight_king_bitboard_moves(board=board, shift_amount=shift_amount, file=self.not_a_file, left_shift=True, opponent_pieces=opponent_pieces, full_board=bitboard.full_board, piece_letter=piece_letter, source_square=square)
                    if move:
                        moves.append(move)
                        if move.is_capture:
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
                moves.append(MoveInfo(target=target_square, source=square, is_capture=True, promotion=None, piece=piece_letter.upper(), en_passant_square=None, is_castle=False))
                break
            elif not self.is_piece_on_square(full_board, target_square):
                if subtract:
                    new_square = new_square - diagonal
                else:
                    new_square = new_square + diagonal
                moves.append(MoveInfo(target=target_square, source=square, is_capture=False, promotion=None, piece=piece_letter.upper(), en_passant_square=None, is_castle=False))
            else:
                break

        return moves

    def calculate_rook_knight_king_bitboard_moves(self, board: np.uint64, shift_amount: int, file: np.uint64, left_shift: bool, opponent_pieces: np.uint64, full_board: np.uint64, piece_letter: str, source_square: int) -> MoveInfo:
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
            return MoveInfo(target=target_square, source=source_square, is_capture=True, promotion=None, piece=piece_letter.upper(), en_passant_square=None, is_castle=False)
        elif not self.is_piece_on_square(full_board, target_square):
            return MoveInfo(target=target_square, source=source_square, is_capture=False, promotion=None, piece=piece_letter.upper(), en_passant_square=None, is_castle=False)
        else:
            return None

    def generate_queen_moves(self, bitboard: Bitboard, color_to_move: bool) -> list:
        moves = []

        moves.extend(self.generate_rook_moves(bitboard=bitboard, color_to_move=color_to_move, is_queen=True))
        moves.extend(self.generate_bishop_moves(bitboard=bitboard, color_to_move=color_to_move, is_queen=True))

        return moves

    def generate_king_moves(self, bitboard: Bitboard, board_obj: Board, color_to_move: bool) -> list:
        moves = []
        king = bitboard.black_king if color_to_move else bitboard.white_king
        opponent_pieces = bitboard.white_board if color_to_move else bitboard.black_board

        # TODO: There is only one king, no need to check all 64 squares
        for square in range(64):
            if self.is_piece_on_square(king, square):
                board = np.uint64(0)
                board = self.set_bit(board, square)

                if color_to_move:
                    if board_obj.black_castle_kingside and not self.is_piece_on_square(bitboard.full_board, F8) and not self.is_piece_on_square(bitboard.full_board, G8):
                        moves.append(MoveInfo(target=F8, source=square, is_capture=False, promotion=None, piece="K", en_passant_square=None, is_castle=True))
                        moves.append(MoveInfo(target=G8, source=square, is_capture=False, promotion=None, piece="K", en_passant_square=None, is_castle=True))

                    if board_obj.black_castle_queenside and not self.is_piece_on_square(bitboard.full_board, D8) and not self.is_piece_on_square(bitboard.full_board, C8):
                        moves.append(MoveInfo(target=D8, source=square, is_capture=False, promotion=None, piece="K", en_passant_square=None, is_castle=True))
                        moves.append(MoveInfo(target=C8, source=square, is_capture=False, promotion=None, piece="K", en_passant_square=None, is_castle=True))
                else:
                    if board_obj.white_castle_kingside and not self.is_piece_on_square(bitboard.full_board, F1) and not self.is_piece_on_square(bitboard.full_board, G1):
                        moves.append(MoveInfo(target=F1, source=square, is_capture=False, promotion=None, piece="K", en_passant_square=None, is_castle=True))
                        moves.append(MoveInfo(target=G1, source=square, is_capture=False, promotion=None, piece="K", en_passant_square=None, is_castle=True))

                    if board_obj.white_castle_queenside and not self.is_piece_on_square(bitboard.full_board, D1) and not self.is_piece_on_square(bitboard.full_board, C1):
                        moves.append(MoveInfo(target=D1, source=square, is_capture=False, promotion=None, piece="K", en_passant_square=None, is_castle=True))
                        moves.append(MoveInfo(target=C1, source=square, is_capture=False, promotion=None, piece="K", en_passant_square=None, is_castle=True))
                # up
                if square > H8:
                    moves.append(self.calculate_rook_knight_king_bitboard_moves(
                        board=board,
                        shift_amount=8,
                        file=np.uint64(0),
                        left_shift=False,
                        opponent_pieces=opponent_pieces,
                        full_board=bitboard.full_board,
                        piece_letter="K",
                        source_square=square
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
                        piece_letter="K",
                        source_square=square
                    ))

                # west
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=1,
                    file=self.not_h_file,
                    left_shift=False,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K",
                    source_square=square
                ))

                # northwest
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=9,
                    file=self.not_h_file,
                    left_shift=False,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K",
                    source_square=square
                ))

                # northeast
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=7,
                    file=self.not_a_file,
                    left_shift=False,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K",
                    source_square=square
                ))

                # east
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=1,
                    file=self.not_a_file,
                    left_shift=True,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K",
                    source_square=square
                ))

                # southeast
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=9,
                    file=self.not_a_file,
                    left_shift=True,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K",
                    source_square=square
                ))

                # southwest
                moves.append(self.calculate_rook_knight_king_bitboard_moves(
                    board=board,
                    shift_amount=7,
                    file=self.not_h_file,
                    left_shift=True,
                    opponent_pieces=opponent_pieces,
                    full_board=bitboard.full_board,
                    piece_letter="K",
                    source_square=square
                ))

        return [move for move in moves if move is not None]

    def is_friendly_king_in_check_after_move(self, bitboard: Bitboard, move: str, color_to_move: int) -> bool:
        pseduo_move_bitboards = self.make_pseduo_move(bitboard, move, color_to_move)

    def make_pseduo_move(self, bitboard: Bitboard, move: str, color_to_move: int) -> Bitboard:

        board = np.uint64(0)
        if "=" in move:
            square = SQUARES_TO_COORDS.index(move[:2])
            board = self.set_bit(board, square)
        elif "+" in move:
            square = SQUARES_TO_COORDS.index(move[-3:-1])
            board = self.set_bit(board, square)
        else:
            square = SQUARES_TO_COORDS.index(move[-2])
            board = self.set_bit(board, square)

        if color_to_move:
            white_pawns = bitboard.white_pawns ^ board if self.is_piece_on_square(bitboard.white_pawns, square) else bitboard.white_pawns
            white_bishops = bitboard.white_bishops ^ board if self.is_piece_on_square(bitboard.white_bishops, square) else bitboard.white_bishops
            white_knights = bitboard.white_knights ^ board if self.is_piece_on_square(bitboard.white_knights, square) else bitboard.white_knights
            white_rooks = bitboard.white_rooks ^ board if self.is_piece_on_square(bitboard.white_rooks, square) else bitboard.white_rooks
            white_queens = bitboard.white_queens ^ board if self.is_piece_on_square(bitboard.white_queens, square) else bitboard.white_queens
            white_king = bitboard.white_king

            if "=Q" in move:
                black_queens = bitboard.black_queens ^ board

            if "B" == move[0]:
                black_bishops = bitboard.black_bishops ^ board
            else:
                black_bishops = bitboard.black_bishops

            if "R" == move[0]:
                black_rooks = bitboard.black_rooks ^ board
            else:
                black_rooks = bitboard.black_rooks

            if "Q" == move[0]:
                black_queens = bitboard.black_queens ^ board
            else:
                black_queens = bitboard.black_queens

            if "K" == move[0]:
                black_king = bitboard.black_king ^ board
            else:
                black_king = bitboard.black_king

            if "N" == move[0]:
                black_knights = bitboard.black_knights ^ board
            else:
                black_knights = bitboard.black_knights

            black_board = black_pawns | black_knights | black_bishops | black_queens | black_rooks | black_king
            white_board = white_pawns | white_knights | white_bishops | white_queens | white_rooks | white_king

        else:
            black_pawns = bitboard.black_pawns ^ board if self.is_piece_on_square(bitboard.black_pawns, square) else bitboard.black_pawns
            black_bishops = bitboard.black_bishops ^ board if self.is_piece_on_square(bitboard.black_bishops, square) else bitboard.black_bishops
            black_knights = bitboard.black_knights ^ board if self.is_piece_on_square(bitboard.black_knights, square) else bitboard.black_knights
            black_rooks = bitboard.black_rooks ^ board if self.is_piece_on_square(bitboard.black_rooks, square) else bitboard.black_rooks
            black_queens = bitboard.black_queens ^ board if self.is_piece_on_square(bitboard.black_queens, square) else bitboard.black_queens
            black_board = black_pawns | black_knights | black_bishops | black_queens | black_rooks | black_king
            white_board = white_pawns | white_knights | white_bishops | white_queens | white_rooks | white_king

        full_board = white_pawns | white_knights | white_bishops | white_queens | white_rooks | white_king | black_pawns | black_knights | black_bishops | black_queens | black_rooks | black_king

        new_bitboards = Bitboard()
        new_bitboards.generate_bitboards_from_bitboards(
            white_pawns="a"
        )

    def is_piece_on_square(self, bitboard: np.uint64, square: int) -> bool:
        return bool(np.ulonglong(bitboard) & (self.UNSIGNED_LONG_1 << np.ulonglong(square)))

    def set_bit(self, bitboard: np.uint64, square: int) -> np.uint64:
        return np.ulonglong(bitboard) | (self.UNSIGNED_LONG_1 << np.ulonglong(square))

    def get_least_sig_bit_index(self, board: np.uint64) -> int:
        if board:
            return (int(board) & int(-board)).bit_length()-1
        else:
            return -1
