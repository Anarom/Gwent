from board import Board


class Game:
    def __init__(self, player_1, player_2):
        self.board = Board()
        self.players = [player_1, player_2]
        self.host = player_1
        self.opp = player_2

    def switch_host(self):
        self.host, self.opp = self.opp, self.host

class GameHandler(Game):
    def __init__(self, player_1, player_2):
        super().__init__(player_1, player_2)
        for player_id, player in enumerate(self.players):
            player.player_id = player_id
            player.army = self.board.armies[player_id]
            player.opponent = self.players[1 - player_id]
