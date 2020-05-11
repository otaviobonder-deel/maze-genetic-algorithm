class Graph:
    def __init__(self, Board):
        Board[Board == 9] = 0
        Board[Board == 7] = 0
        self.edges = {}
        for i in range(0, Board.shape[0]):
            for j in range(0, Board.shape[1]):
                possible_moves = []
                if j + 1 < 10 and Board[i][j + 1] == 0:
                    possible_moves.append((i, j + 1))

                if j - 1 >= 0 and Board[i][j - 1] == 0:
                    possible_moves.append((i, j - 1))

                if i + 1 < 10 and Board[i + 1][j] == 0:
                    possible_moves.append((i + 1, j))

                if i - 1 >= 0 and Board[i - 1][j] == 0:
                    possible_moves.append((i - 1, j))

                if i + 1 < 10 and j + 1 < 10 and Board[i + 1][j + 1] == 0:
                    possible_moves.append((i + 1, j + 1))

                if i + 1 < 10 and j - 1 >= 0 and Board[i + 1][j - 1] == 0:
                    possible_moves.append((i + 1, j - 1))

                if i - 1 >= 0 and j + 1 < 10 and Board[i - 1][j + 1] == 0:
                    possible_moves.append((i - 1, j + 1))

                if i - 1 >= 0 and j - 1 >= 0 and Board[i - 1][j - 1] == 0:
                    possible_moves.append((i - 1, j - 1))

                self.edges[(i, j)] = possible_moves

    def neighbors(self, id):
        return self.edges[id]
