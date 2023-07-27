class Board():
    def __init__(self) -> None:
        self.piece_board = []
        self.color_to_move = None
        self.white_castle_kingside = False
        self.black_castle_kingside = False
        self.white_castle_queenside = False
        self.black_castle_queenside = False
        self.en_passant_target_square = None

    def generate_board_values_from_fen(self, parsed_fen):
        self.piece_board = parsed_fen["piece_board"]
        self.color_to_move = parsed_fen["color_to_move"]
        self.white_castle_kingside = parsed_fen["white_castle_kingside"]
        self.black_castle_kingside = parsed_fen["black_castle_kingside"]
        self.white_castle_queenside = parsed_fen["white_castle_queenside"]
        self.black_castle_queenside = parsed_fen["black_castle_queenside"]
        self.en_passant_target_square = parsed_fen["en_passant_target_square"]
