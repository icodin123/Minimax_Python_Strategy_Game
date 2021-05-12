"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any, List, Union
from random import randint


class Tree:
    """A special tree used for minimax strategy.

    value - value of a node
    children - children of node
    highest_score - the highest score achiveable from game state by using it as
    a value and its child states as elements in list children
    mov - move by which value game state was achieved

    >>> t = Tree(1)
    >>> t.value
    1
    """
    def __init__(self, value: Any,
                 children: List['Tree'] = None, mov: object = 'Root') -> None:
        """Initialize a new Tree self.

        >>> t = Tree(1)
        >>> t.value
        1
        """
        self.value = value
        self.children = children if children is not None else []
        self.highest_score = None
        self.mov = mov

    def __eq__(self, other: 'Tree') -> bool:
        """Return whether self is equivalent to other.

        >>> t1 = Tree(1)
        >>> t2 = Tree(2)
        >>> t1 == t2
        False
        """
        return (type(self) == type(other) and self.value == other.value
                and self.children == other.children)

    def __str__(self) -> str:
        """Return the string representation of an object.
        >>> t = Tree(1)
        >>> str(t)
        'Tree(1, [])'
        """
        return 'Tree({}, {})'.format(self.value, self.children)

    def __repr__(self) -> str:
        """Return representation of an object.

        >>> t = Tree(1)
        >>> t.__repr__()
        'Root'
        """
        return str(self.mov)

    def add(self, child: 'Tree') -> None:
        """Add child to the children of self.

        >>> t = Tree(1)
        >>> t.add(Tree(2))
        >>> t.children
        [Root]
        """
        self.children.append(child)


class Stack:
    """"A stack.

    >>> s = Stack()
    >>> s.add(5)
    >>> s.remove()
    5
    """
    def __init__(self) -> None:
        """Initialize a new Stack self.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.remove()
        5
        """
        self._content = []

    def __eq__(self, other: 'Stack') -> bool:
        """Return whether self is equivalent to other.

        >>> s1 = Stack()
        >>> s1.add(5)
        >>> s2 = Stack()
        >>> s1 == s2
        False
        """
        return (type(self) == type(other) and
                self._content == other.get_content())

    def __str__(self) -> str:
        """Return the string representation of self.

        >>> s = Stack()
        >>> s.add(5)
        >>> str(s)
        '[5]'
        """
        return str(self._content)

    def __repr__(self) -> str:
        """Return a representation of self.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.__repr__()
        '[5]'
        """
        return self.__str__()

    def add(self, value: Union[object, 'Tree']) -> None:
        """Add an object to the Stack self.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.remove()
        5
        """
        self._content.append(value)

    def is_empty(self) -> bool:
        """Return whether Queue is empty.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.is_empty()
        False
        """
        return len(self._content) == 0

    def remove(self) -> Union[object, 'Tree']:
        """Return and remove an object from Stack self.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.remove()
        5
        """
        if self.is_empty():
            pass
        return self._content.pop()

    def get_size(self) -> int:
        """Return the length of content of self.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.get_size()
        1
        """
        return len(self._content)

    def get_content(self) -> List[object]:
        """Return the copy of _content of self."""
        return self._content[:]


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


def recursive_minimax_strategy(game: Any) -> Any:
    """Return the move for the game which results in the worst outcome for
    the opponent.
    """
    cur_state = game.current_state
    moves = cur_state.get_possible_moves()
    resulting_pairs = {}
    for move in moves:
        resulting_pairs[move] = (-1) * expander(game, cur_state.make_move(move))
    maximal = []
    maximum = max(resulting_pairs.values())
    game.current_state = cur_state
    for move in resulting_pairs:
        if resulting_pairs[move] == maximum:
            maximal.append(move)
    if maximal != []:
        return maximal[randint(0, len(maximal) - 1)]
    return 0


def expander(game: Any, cur_state: Any) -> Any:
    """Return the result for the player of the cur_state guaranteed by child
    states.
    """
    game.current_state = cur_state
    cur_player = 'p1' if cur_state.p1_turn else 'p2'
    other_player = 'p2' if cur_player == 'p1' else 'p1'
    if game.is_over(cur_state):
        if game.is_winner(cur_player):
            return 1
        if game.is_winner(other_player):
            return -1
        return 0
    moves = cur_state.get_possible_moves()
    new_states = [cur_state.make_move(move) for move in moves]
    return max([(-1) * expander(game, x) for x in new_states])


def iterative_minimax_strategy(game: Any) -> Any:
    """Return the move for the game which results in the worst outcome for
    the opponent.
    """
    cur = game.current_state
    s = Stack()
    t = Tree(cur)
    s.add(t)
    while not s.is_empty():
        x = s.remove()
        if x.children != [] and x.mov != 'Root':
            x.highest_score = max([(-1) * y.highest_score for y in x.children])
        elif x.children != [] and x.mov == 'Root':
            x.highest_score = max([(-1) * y.highest_score for y in x.children])
            maximal = find_maximal(x)
            game.current_state = cur
            return maximal[randint(0, len(maximal) - 1)]
        elif game.is_over(x.value):
            cur_player = 'p1' if x.value.p1_turn else 'p2'
            other_player = 'p2' if cur_player == 'p1' else 'p1'
            game.current_state = x.value
            if game.is_winner(cur_player):
                x.highest_score = 1
            elif game.is_winner(other_player):
                x.highest_score = -1
            else:
                x.highest_score = 0
        elif x.children == []:
            moves = x.value.get_possible_moves()
            new = [Tree(x.value.make_move(move), mov=move) for move in moves]
            x.children.extend(new)
            s.add(x)
            for n in new:
                s.add(n)
    game.current_state = cur
    return 0


def find_maximal(x: 'Tree') -> List[Any]:
    """Return the list of children of x with greatest scores.
    """
    maximal = []
    for z in x.children:
        if z.highest_score * (-1) == x.highest_score:
            maximal.append(z.mov)
    return maximal
