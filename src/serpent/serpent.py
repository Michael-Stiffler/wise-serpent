from pprint import pformat
import logging
from .bitboard import Bitboard
from .board import Board
from .fen import Fen
from .move_generator import MoveGenerator
from . visuals import Visuals
import cProfile
import pstats
import sys


class Serpent():

    def __init__(self) -> None:
        # init stuff for game loop here

        logging.basicConfig()
        self.info_logger = logging.getLogger("serpent")
        self.info_logger.setLevel(logging.INFO)
        self.debug_logger = logging.getLogger("serpent")
        self.debug_logger.setLevel(logging.DEBUG)

        self.bitboard = Bitboard()
        self.board = Board()
        self.fen = Fen()
        self.move_generator = MoveGenerator()
        self.visuals = Visuals()

        self.user_color = None

    def start_serpent(self) -> None:
        self.info_logger.info("Starting Serpent")

        serpent_isrunning = True
        need_to_generate_moves = True

        while serpent_isrunning:
            if need_to_generate_moves:
                with cProfile.Profile() as pr:
                    moves = self.move_generator.generate_moves(self.bitboard, self.board)
                    # moves = self.move_generator.verify_moves(self.bitboard, self.board.color_to_move, moves)
                stats = pstats.Stats(pr)
                stats.sort_stats(pstats.SortKey.TIME)
                stats.print_stats()
                need_to_generate_moves = False
                self.visuals.print_board()

            while True:
                color_to_move = "Black" if self.board.color_to_move else "White"
                move = input(color_to_move + " to move. Enter a move: ")
                if move in moves:
                    # set move in self.board object
                    self.visuals.set_board(self.board.piece_board)
                    self.visuals.print_board()
                    break
                else:
                    self.visuals.print_board()
                    print("That move is not possible in this position. Please select another move")

            serpent_isrunning = False

    def parse_args(self, args) -> None:

        self.parse_fen(args)
        self.parse_user_color(args)

    def parse_fen(self, args) -> None:
        # Only parsing fens for now as that is the only argument possible
        base_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        if args.fen:
            self.fen.parse_fen(args.fen)
            self.info_logger.info(f"Using fen: {args.fen}")
        else:
            self.fen.parse_fen(base_fen)
            self.info_logger.info(f"No fen selected, using base fen: {base_fen}")

        parsed_fen = self.fen.get_parsed_fen()
        self.debug_logger.debug(f"Parsed fen is {pformat(parsed_fen)}")
        self.init_helpers_from_fen(parsed_fen)

    def init_helpers_from_fen(self, fen) -> None:
        self.info_logger.info("Setting bitboards, board, and visuals")

        self.bitboard.generate_bitboards_from_fen(fen)
        self.board.generate_board_values_from_fen(fen)
        self.visuals.set_board(self.board.piece_board)

    def parse_user_color(self, args) -> None:
        if args.color:
            if args.color.lower() == "white":
                self.user_color = 0
            elif args.color.lower() == "black":
                self.user_color = 1
            else:
                print("ERROR: Color argument did not specify white or black.")
                print("Exiting Serpent")
                sys.exit()
