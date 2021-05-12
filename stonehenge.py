"""module for Stonehenge game and GameState for Stonhenge game."""

from typing import Any, List, Union
from game import Game
from game_state import GameState
from board import Board


class StonehengeGame(Game):
    """A Stonehenge game for 2 players played using a board.

    current_state - Game state controller for the game
    insturctions - instructions for the game
    board_size - the size of the board
    """
    current_state: GameState
    instructions: str
    board_size: int

    def __init__(self, p1_starts: bool) -> None:
        """Initialize a new Stonhenge game self.

        Overridden from Game.
        """
        self.instructions = ("1. Players choose who plays first.\n2. Player " +
                             "claims a cell from the available options.\n" +
                             "Cells form the lines called ley-lines." +
                             "There are three types\nof" + "ley-lines in" +
                             "this game - two types are represented " +
                             "by\ndiagonals and" + "the third type is" +
                             "represented by horizontal\nlines. First type" +
                             "of ley-lines are downward-sloping diagonals." +
                             "The\nsecond type is represented by upward" +
                             "-sloping diagonaals. The third\ntype are" +
                             "all the horizontal lines passing through" +
                             "the cells at \n at each level.\n3." +
                             "The player's goal is to capture at least" +
                             "half of the ley-lines.\nA ley-line, once" +
                             "claimed, cannot be taken by the other pla" +
                             "yer.\n4. The first player to capure at" +
                             "least a half of all" +
                             "ley-lines wins !")
        self.board_size = int(input('Please enter the size of the board : '))
        self.current_state = StonehengeState(p1_starts, self.board_size)
        self.p1_starts = p1_starts

    def __str__(self) -> str:
        """Return the string representation of self.

        Overridden from Game.
        """
        return 'Stonehenge game with {} board size'.format(self.board_size)

    def __eq__(self, other: Any) -> bool:
        """Return whether self is equivalent to other.

        Overridden from Game.
        """
        return type(self) == type(other) and self.board_size == other.board_size

    def __repr__(self) -> Any:
        """Return representation of an object.

        Overridden from Game.
        """
        return 'StonehengeGame({})'.format(self.p1_starts)

    def get_instructions(self) -> str:
        """Return instructions for Stonhenge game.

        Overriden from Game.
        """
        return self.instructions

    def is_over(self, state: GameState) -> bool:
        """Return whether the game is over.

        Overriden from Game.
        """
        return state.board.game_over()

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.

        Overriden from Game.
        """
        return self.current_state.board.total_winner(player)

    def str_to_move(self, string: str) -> Union[int, str]:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.

        Precondition : string should consist of one capital letter from
        English Alphabet.

        Overriden from Game.
        """
        if not string.strip().isalpha():
            return -1
        return string.strip().upper()

class StonehengeState(GameState):
    """Game state for Stonhenge game.

    is_p1_turn - indicates whether it is player1's turn
    size - the size of the board
    board - current board for the game

    >>> s = StonehengeState(True, 1)
    >>> s.size == 1
    True
    >>> s.p1_turn
    True
    >>> s.get_possible_moves()
    ['A', 'B', 'C']
    """
    size: int
    board: Board

    def __init__(self, is_p1_turn: bool, size: int) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        Extended from GameState.

        >>> s = StonehengeState(True, 5)
        >>> s.size
        5
        >>> s.p1_turn
        True
        """
        GameState.__init__(self, is_p1_turn)
        self.size = size
        self.board = Board(size)

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.

        Overriden from GameState.
        >>> s = StonehengeState(True, 0)
        >>> str(s).count('@')
        5
        """
        return str(self.board)

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).

        Overriden from GameState.

        >>> s = StonehengeState(True, 1)
        >>> s.__repr__().count('Current player')
        1
        """
        cur_player = 'p1' if self.p1_turn else 'p2'
        return 'Current player is : {}.\n'.format(cur_player) + str(self)

    def get_possible_moves(self) -> List[str]:
        """
        Return all possible moves that can be applied to this state.

        Overriden from GameState.

        >>> s = StonehengeState(True, 1)
        >>> s.get_possible_moves()
        ['A', 'B', 'C']
        """
        return self.board.possible_variations()

    def make_move(self, move: Any) -> 'GameState':
        """
        Return the GameState that results from applying move to this GameState.

        Overriden from GameState.

        >>> s = StonehengeState(True, 0)
        >>> s2 = s.make_move('A')
        >>> str(s2).count('1')
        4
        """
        new_state = StonehengeState(self.p1_turn, self.size)
        new_state.board = self.board.produce_copy()

        if new_state.p1_turn:
            new_state.board.occupy_node(move, 'p1')
        else:
            new_state.board.occupy_node(move, 'p2')

        new_state.p1_turn = not self.p1_turn
        return new_state

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        Overriden from GameState.

        >>> s = StonehengeState(True, 1)
        >>> s.rough_outcome()
        1
        """
        cur_player = 'p1' if self.p1_turn else 'p2'
        other_player = 'p2' if cur_player == 'p1' else 'p1'
        if self.board.game_over():
            return -1
        moves = self.get_possible_moves()
        children = [self.make_move(move) for move in moves]
        grand_children, last_index = {}, 0
        for child in children:
            if child.board.is_total_winner(cur_player):
                return 1
            new_outcomes = []
            new_moves = child.get_possible_moves()
            if not child.board.game_over() and new_moves != []:
                new_children = [child.make_move(nm) for nm in new_moves]
                self.shape_new_outcomes(new_children, other_player,
                                        new_outcomes)
            grand_children[last_index] = new_outcomes
            last_index += 1
        if all([other_player in grand_children[x] for x in grand_children]):
            return -1
        if any([other_player not in grand_children[y] for y in grand_children]):
            return 0
        return 0

    def shape_new_outcomes(self, new_children: List['GameState'],
                           other_player: str, new_outcomes:
                           List[Union[int, str]]) -> None:
        """Modify new_outcomes list to contain information about other
        player winning or loosing at different stages.
        """
        for nc in new_children:
            if nc.board.is_total_winner(other_player):
                new_outcomes.append(other_player)
            else:
                new_outcomes.append(0)
