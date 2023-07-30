class Board():
    def __init__(self) -> None:
        self.piece_board = []
        self.color_to_move = None
        self.white_castle_kingside = False
        self.black_castle_kingside = False
        self.white_castle_queenside = False
        self.black_castle_queenside = False
        self.en_passant_target_square = None

    def generate_board_values_from_fen(self, fen) -> None:
        self.piece_board = fen["piece_board"]
        self.color_to_move = fen["color_to_move"]
        self.white_castle_kingside = fen["white_castle_kingside"]
        self.black_castle_kingside = fen["black_castle_kingside"]
        self.white_castle_queenside = fen["white_castle_queenside"]
        self.black_castle_queenside = fen["black_castle_queenside"]
        self.en_passant_target_square = fen["en_passant_target_square"]
