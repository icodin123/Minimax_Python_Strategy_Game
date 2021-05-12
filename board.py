"""module for board."""

from typing import List, Union, Any, Tuple


class Board:
    """A Board for the game Stonehenge.

    data - contains size of the board and winner of the game if any.
    moves_history - history of moves applied to the board by players
    node_reference - reference of all the node-ley-line connections
    upw_leys - upward-facing leys
    downw_leys - downward-facing ley-lines of the board
    horiz_leys - horiz ley-lines of the board

    >>> b = Board(1)
    >>> b.data[0] == 1
    True
    >>> b.possible_variations()
    ['A', 'B', 'C']
    >>> b.occupation_possible('A')
    True
    >>> b.game_over()
    False
    """
    data: list
    moves_history: list
    node_reference: dict
    upw_leys: list
    downw_leys: list
    horiz_leys: list

    def __init__(self, size: int, content: List[Union[None, List['BoardNode']]]
                 =None) -> None:
        """Initialize a new Board self.

        >>> b = Board(0)
        >>> b.possible_variations()
        ['A', 'B']
        >>> b.occupation_possible('A')
        True
        """
        self.data = [size, None]
        self.moves_history = []
        self._content = content if content is not None else []
        self.node_reference = {}
        self.generate_layers()
        self.name_layers()
        upw_diag = self.adjoin(self._content, 'u')
        downw_diag = self.adjoin(self._content, 'd')
        self.upw_leys = self.generate_leys(upw_diag)
        self.downw_leys = self.generate_leys(downw_diag)
        self.horiz_leys = self.generate_leys(self._content)

    def __str__(self) -> str:
        """Return the string representation of self.

        >>> b = Board(0)
        >>> len(str(b)) == 70
        True
        """
        form = [r'/ \ ', r'@ ', r'  \ ', r'  / ']
        m = len(self._content)
        indent = 2 * m
        result = (' ' + ' ' * (indent + 2) + ' {}{}\n'.format(self.upw_leys[0],
                                                              self.upw_leys[
                                                                  1]) + ' ' +
                  ' ' * (indent + 2) + form[3] * 2 + '\n')
        for i in range(m):
            result += ' ' * indent + str(self.horiz_leys[i]).lstrip()
            for b in self._content[i]:
                result += str(b)
            if i == m - 1 and self.data[0] != 0:
                result += str(self.downw_leys[-1])
            if i + 2 < len(self.upw_leys):
                result += str(self.upw_leys[i + 2])
            result += '\n' + ' ' * (indent + 1)
            if i < m - 1:
                mk = '/' if i + 1 < m - 1 else ''
                if i < m - 2:
                    result += (' ' * 2 + form[0] * len(self._content[i]) +
                               mk + '\n')
                else:
                    result += (' ' * 2 + form[2] + form[0] *
                               (len(self._content[i]) - 1) + mk + '\n')
            if i == m - 1:
                result += '  ' + form[2] * len(self._content[i]) + '\n'
                result += ' ' * (indent + 1) + '   '
                result = self.complete_str(result)
            if i == m - 2:
                indent += 2
            else:
                indent -= 2
        return result

    def __eq__(self, other: 'Board') -> bool:
        """Return whether self is equivalent to other.

        >>> b = Board(1)
        >>> b2 = Board(1)
        >>> b == b2
        True
        >>> b3 = Board(0)
        >>> b3 == b2
        False
        """
        return (type(self) == type(other) and self._content == other._content
                and self.node_reference == other.node_reference and
                self.data == other.data and self.upw_leys ==
                other.upw_leys and self.downw_leys == other.downw_leys
                and self.horiz_leys == other.horiz_leys)

    def __repr__(self) -> str:
        """Return representation of self.

        >>> b = Board(5)
        >>> b.__repr__()
        'Board(5)'
        """
        return 'Board({})'.format(str(self.data[0]))

    def complete_str(self, result: str) -> object:
        """HELPER FUNCTION
        Return new version of result depending on current Board parameters.
        """
        if self.data[0] > 0:
            for g in self.downw_leys[:-1]:
                result += str(g)
        else:
            for g in self.downw_leys:
                result += str(g)
        return result

    def _add(self, obj: object) -> None:
        """Private method.
        """
        self._content.append(obj)

    def generate_layers(self, res: list = None, layer: int = 1) -> None:
        """Recursive helper function to generate layers of the board.

        Not to be called from anywhere else except __init__ method of the board.

        Doctests not provided because this helper function continues
        implementation of the init method.
        """
        # check = 3 if self.data[0] == 0 else 2
        if layer == 1:
            res = [BoardNode() for i in range(2)]
            self._add(res)
            # temp0 = layer + 1 if self.data[0] == 1 else layer + 2
            if self.data[0] >= 0:
                self.generate_layers(res, layer + 2)
        elif layer <= self.data[0] + 2:
            temp, temp2 = None, None
            if self.data[0] == 1:
                temp = res
                temp2 = []
            elif layer < self.data[0] + 2:
                temp = res
                temp2 = [BoardNode()]
            if layer == self.data[0] + 2:
                temp = res[1:]
                temp2 = []
            for b in temp:
                b.child = BoardNode()
            new_res = [b.child for b in res if b.child is not None] + temp2
            self._add(new_res)
            self.generate_layers(new_res, layer + 1)

    def name_layers(self) -> None:
        """HELPER FUNCTION to name the nodes of the Board self.

        Not to be called from anywhere else except __init__ method of the board.

        Doctests not provided because this helper function continues
        implementation of the init method.
        """
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                    'V', 'W', 'X', 'Y', 'Z']
        index = 0
        add_on = 0
        for l in self._content:
            for b in l:
                if index == len(alphabet):
                    index = 0
                    add_on += 1
                to_add = '\'' * add_on
                name = alphabet[index] + to_add
                b.value = name
                self.node_reference[name] = [b, []]
                index += 1

    def generate_leys(self, l: list) -> list:
        """Return the list of leys with children from sublists of l.

        >>> l = [[1, 2, 3], [4, 5, 6]]
        >>> b = Board(0)
        >>> b.generate_leys(l)
        [LeyLine([1, 2, 3]), LeyLine([4, 5, 6])]
        """
        result = []
        for x in l:
            line = LeyLine(x)
            for key in self.node_reference:
                if self.node_reference[key][0] in x:
                    self.node_reference[key][1].append(line)
            result.append(line)
        return result

    def max_len_list(self, l: list) -> int:
        """Return the index of a sublist with greatest length contained in l.

        >>> l = [[1, 2, 3], [4, 5]]
        >>> b = Board(0)
        >>> b.max_len_list(l)
        0
        """
        max_ind = 0
        max_res = -1
        for i in range(len(l)):
            if len(l[i]) > max_res:
                max_ind = i
                max_res = len(l[i])
        return max_ind

    def top_to_line(self, a: list, max_width: int, index: int = 0) -> \
            List[object]:
        """Return the list of lists of elements in sublist of a
        grouped by the indices they originally belong to.

        Precondition: an accurate max_width value should be provided - the
        maximum length of a list in a.

        >>> a = [[1, 2, 3, 4], [5, 6]]
        >>> b = Board(0)
        >>> b.top_to_line(a, 3)
        [[1, 5], [2, 6], [3], [4]]
        """
        if index <= max_width:
            k = [x[index] for x in a if len(x) > index]
            if k != []:
                k = [k]
            return k + self.top_to_line(a, max_width, index + 1)
        return []

    def adjoin(self, l: list, mode: Union['u', 'd']) -> list:
        """ HELPER FUNCTION - not to be called from anywhere else other than
        __init__ method. THUS NO DOCTESTS PROVIDED.
        Return of board diagonals depending on the mode - upward or
        downward.
        """
        res1 = None
        if self.data[0] == 0:
            return [[x] for x in l[0]]
        if mode == 'u' and self.data[0] >= 1:
            res1 = self.top_to_line(l[:-1], max([len(x) for x in l[:-1]]))
            for i in range(1, len(res1)):
                res1[i].append(l[-1][i - 1])
        if mode == 'd' and self.data[0] >= 1:
            res1 = self.top_to_line(l[-1:-3:-1],
                                    max([len(x) for x in l[-1:-3:-1]]))
            j = []
            n = l[:-2]
            for count in range(len(n)):
                temp = self.max_len_list(n)
                j.append(n[temp])
                n.pop(temp)
            count = -1
            for i in range(len(res1) - 1, 0, -1):
                for s in j:
                    self.complete_str2(count, -len(s), res1, (s, i))
                count -= 1
        return res1

    def complete_str2(self, count: int, length: int, res1: List[Any],
                      couple: Tuple[List[Any], int]):
        """HELPER FUNCTION - complete the process started in __str__ method.
        Thus no DOCSTRINGS provided.
        """
        if count >= length:
            res1[couple[1]].append(couple[0][count])

    def bottom_to_line(self, a: list, max_width: int, index: int = 0) -> \
            List[object]:
        """Return the list of lists of element in sublist of a
        grouped by the indices they originally belong to.

        Precondition: an accurate max_width value should be provided - the
        maximum length of a list in a.

        >>> a = [[1, 2, 3, 4], [5, 6]]
        >>> b = Board(0)
        >>> b.bottom_to_line(a, 3)
        [[1, 5], [2, 6], [3], [4]]
        """
        if index < max_width:
            k = [x[index] for x in a if len(x) > index]
            if k != []:
                k = [k]
            return k + self.top_to_line(a, max_width, index + 1)
        return []

    def occupy_node(self, node: str, player: str) -> None:
        """Make node player's property if possible.

        Precondition: player should be one of 'p1' or 'p2'.

        >>> b = Board(1)
        >>> b.occupy_node('A', 'p1')
        >>> b.occupation_possible('A')
        False
        """
        # if self.occupation_possible(node): - NO NEED FOR THIS ACCORDING TO
        # PIAZZA SINCE GAME INTERFACE IS HANDLING THIS KIND OF SITUATIONS.

        self.moves_history.append((node, player))
        self.node_reference[node][0].value = 1 if player == 'p1' else 2
        for x in self.upw_leys:
            x.calculate_positions()
        for y in self.downw_leys:
            y.calculate_positions()
        for z in self.horiz_leys:
            z.calculate_positions()
        if self.winner(player) and self.data[1] is None:
            self.data[1] = player

    def occupation_possible(self, node: str) -> bool:
        """Return whether occupation of a node is possible.

        >>> b = Board(1)
        >>> b.occupy_node('A', 'p1')
        >>> b.occupation_possible('A')
        False
        """
        if (self.node_reference[node][0].value == 1 or
                self.node_reference[node][0].value == 2):
            return False
        return True

    def possible_variations(self) -> List[str]:
        """Return the list of possible moves a player can make.

        >>> b = Board(1)
        >>> b.possible_variations()
        ['A', 'B', 'C']
        """
        result = []
        if not self.game_over():
            for node in self.node_reference:
                if self.occupation_possible(node):
                    result.append(node)
        return result

    def winner(self, player: str) -> bool:
        """Return whether player is the winner of the game.

        Precondition: player should be one of 'p1' or 'p2'.

        >>> b = Board(1)
        >>> b.winner('p1')
        False
        """
        total_leys = (len(self.upw_leys) + len(self.upw_leys) + \
                      len(self._content))
        p1_leys, p2_leys = 0, 0
        for x in self.upw_leys:
            if x.taken == 'p1':
                p1_leys += 1
            if x.taken == 'p2':
                p2_leys += 1
        for y in self.downw_leys:
            if y.taken == 'p1':
                p1_leys += 1
            if y.taken == 'p2':
                p2_leys += 1
        for z in self.horiz_leys:
            if z.taken == 'p1':
                p1_leys += 1
            if z.taken == 'p2':
                p2_leys += 1
        if player == 'p1' and p1_leys >= 0.5 * total_leys:
            return True
        if player == 'p2' and p2_leys >= 0.5 * total_leys:
            return True
        return False

    def total_winner(self, player: str) -> bool:
        """Return the winner of the game.

        Precondition: player should be one of 'p1' or 'p2'.

        >>> b = Board(1)
        >>> b.total_winner('p1')
        False
        """
        return self.data[1] == player

    def game_over(self) -> bool:
        """Return whether game is over."""
        return True if self.data[1] is not None else False

    def produce_copy(self) -> 'Board':
        """Produce a complete copy of self."""
        new_board = Board(self.data[0])
        for move in self.moves_history:
            new_board.occupy_node(move[0], move[1])
            for x in new_board.upw_leys:
                x.calculate_positions()
            for y in new_board.downw_leys:
                y.calculate_positions()
            for z in new_board.downw_leys:
                z.calculate_positions()
        return new_board

    def organize_in_structures(self, l1: List[List['BoardNode']], l2:
                               List[List['BoardNode']]) -> list:
        """Return a new list with BoardNodes from l1 organized in the same
        manner as are BoardNodes in l2.

        Precondition: both lists must be nested

        >>> l1 = [[BoardNode(1), BoardNode(6), BoardNode(3)], [BoardNode(2)]]
        >>> l2 = [[BoardNode(1), BoardNode(2)], [BoardNode(3)], [BoardNode(6)]]
        >>> b = Board(0)
        >>> b.organize_in_structures(l1, l2)
        [[1, 2], [3], [6]]
        """
        result = []
        for x in l2:
            temp_result = []
            for x2 in x:
                temp_result.append(self.find_with_value(l1, x2.value))
            result.append(temp_result)
        return result

    def find_with_value(self, l: List[List['BoardNode']], value: str) -> \
            'BoardNode':
        """Return the BoardNode from l that contains value.

        >>> l = [[BoardNode(1), BoardNode(2)]]
        >>> b = Board(1)
        >>> b.find_with_value(l, 1)
        1
        """
        res = None
        for k in l:
            for u in k:
                if u.value == value:
                    res = u
        return res

    def find_cells(self, cells: list, cont: list) -> List['BoardNode']:
        """Return the copy of cells with duplicates of BoardNoades originally
        contained in cont.

        >>> cells = []
        >>> cont = []
        >>> b1 = BoardNode(1)
        >>> cells.append(b1)
        >>> cont.append([b1])
        >>> b = Board(1)
        >>> b.find_cells(cells, cont)
        [1]
        """
        result = []
        for cell in cells:
            for x in cont:
                for i in x:
                    self.add_if(cell, i, result)
        return result

    def add_if(self, cell: 'BoardNode', i: int, result: List[Any]) -> None:
        """HELPER FUNCTION
        Complete the process began in find_cells method.
        Thus no DOCSTRINGS are provided.
        """
        if cell.value == i.value:
            result.append(i)

    def generate_child_states(self, player: str) -> list:
        """Return the list of achievable boards from self.

        Precondition: player should be one of 'p1' or 'p2'.

        >>> b = Board(1)
        >>> b.generate_child_states('p1')
        [Board(1), Board(1), Board(1)]
        """
        states = []
        moves = self.possible_variations()
        for move in moves:
            new_board = self.produce_copy()
            new_board.occupy_node(move, player)
            states.append(new_board)
        return states

    def is_total_winner(self, player: str) -> bool:
        """Return whether player is the winner of the game.

        Precondition: player should be one of 'p1' or 'p2'.

        >>> b = Board(1)
        >>> b.total_winner('p1')
        False
        """
        return player == self.data[1]

    def find_floor(self, n: float) -> int:
        """Return the floor of integer n.

        Precondition: n must be >= 0.

        >>> b = Board(1)
        >>> b.find_floor(5.5)
        5
        """
        return int(n // 1)

    def find_ceiling(self, n: float) -> int:
        """Return the ceiling of number n.

        Precondition: n must be >= 0.

        >>> b = Board(1)
        >>> b.find_ceiling(5.5)
        6
        """
        return int(n) if n % 1 == 0 else self.find_floor(n) + 1

    def set_content(self, l: list) -> None:
        """ HELPER FUNCTION NOT TO BE CALLED FROM ANYWHERE EXCEPT __init__
        method. THUS DOCTESTS NOT PROVIDED.
        Change the value of _content of self.
        """
        self._content = l


class BoardNode:
    """A board node with a child.

    value - value of the BoardNode
    child - child of a BoardNode

    >>> b = BoardNode(1)
    >>> b.value
    1
    """
    value: Union[int, str]
    child: list

    def __init__(self, value: object = '^', child: object = None) -> None:
        """Initialize a new Visual Node.

         >>> b = BoardNode(1)
         >>> b.value
         1
        """
        self.child = child if child is not None else None
        self.value = value

    def __str__(self) -> str:
        """Return the string representation of self.

        >>> b = BoardNode(1)
        >>> str(b)
        '- 1 '
        """
        res = "- {} ".format(self.value)
        if '\'' not in res:
            return res
        return res.replace(' ', '', res.count('\''))

    def __eq__(self, other: 'BoardNode') -> bool:
        """Return whether self is equivalent to other.

        >>> b1 = BoardNode(1)
        >>> b2 = BoardNode(2)
        >>> b1 == b2
        False
        """
        return (type(self) == type(other) and self.child == other.child and
                self.value == other.value)

    def __repr__(self) -> str:
        """"Return representation of self.

        >>> b = BoardNode(1)
        >>> b.__repr__()
        '1'
        """
        return str(self.value)


class LeyLine:
    """A ley-line for the board game Stonehenge.

    taken - indicates whether LeyLine belongs to any player
    cells - BoardNoades that LeyLine consists of

    >>> l = LeyLine([BoardNode(1)])
    >>> l.taken = 'p1'
    >>> l.taken
    'p1'
    """
    taken: Union[None, str]
    cells: list

    def __init__(self, cells: List[object], taken: str = None) -> None:
        """Initialize a new LeyLine self.

        >>> l = LeyLine([BoardNode(1)])
        >>> l.taken = 'p1'
        >>> l.taken
        'p1'
        """
        self.taken = taken if taken is not None else None
        self.cells = cells

    def __str__(self) -> str:
        """Return the string representation of self.

        >>> l = LeyLine([BoardNode(1)])
        >>> str(l)
        '  1 '
        """
        self.calculate_positions()
        if self.taken == 'p1':
            return '  1 '
        if self.taken == 'p2':
            return '  2 '
        return '  @ '

    def __eq__(self, other: 'LeyLine') -> bool:
        """Return self is equivalent to other.

        >>> l1 = LeyLine([BoardNode(1)])
        >>> l2 = LeyLine([BoardNode(2)])
        >>> l1 == l2
        False
        """
        return (type(self) == type(other) and self.taken == other.taken and
                self.cells == other.cells)

    def __repr__(self) -> str:
        """Return the representation of an object.

        >>> l = LeyLine([BoardNode(1)])
        >>> str(l)
        '  1 '
        """
        return 'LeyLine({})'.format(self.cells)

    def almost_owns(self, player) -> bool:
        """Return whether player almost owns a ley-line.

        Precondition: player should be one of 'p1' or 'p2'.

        >>> l = LeyLine([BoardNode(1)])
        >>> l.almost_owns('p1')
        False
        """
        count = 0
        player_code = 1 if player == 'p1' else 2
        nodes = len(self.cells)
        for node in self.cells:
            if node.value == player_code:
                count += 1
        count = count - 1 if count // 1 == count else count // 1
        return count >= nodes * 0.5

    def calculate_positions(self) -> None:
        """Calculate whether any of two players owns a ley-line.

        >>> l = LeyLine([BoardNode(1)])
        >>> l.calculate_positions()
        >>> l.taken
        'p1'
        """
        if self.taken is None:
            p1_number = 0
            p2_number = 0
            for cell in self.cells:
                if cell.value == 1:
                    p1_number += 1
                if cell.value == 2:
                    p2_number += 1
            if p1_number >= 0.5 * len(self.cells):
                self.taken = 'p1'
            if p2_number >= 0.5 * len(self.cells):
                self.taken = 'p2'
