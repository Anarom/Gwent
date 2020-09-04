from board import Board


class Game:
    factions = ['Northen Relams', 'Nilfgaardian Empire', "Scoia'tael", 'Monsters', 'Neutral']

    def __init__(self, player_1, player_2):
        self.board = Board()
        self.host = player_1
        self.opp = player_2
        self.host.army = self.board.armies[0]
        self.opp.army = self.board.armies[1]


class GameHandler(Game):
    def __init__(self, player_1, player_2):
        super().__init__(player_1, player_2)

    def apply_passive(self):
        order = sorted((self.host, self.opp), key=lambda x: x.leader.order)
        for player in order:
            if player.leader.passive:
                self.switch_host(host=player)
                player.play_leader()

    def switch_host(self, host=None):
        if host:
            self.opp = self.host if self.opp is host else self.opp
            self.host = host
        else:
            self.host, self.opp = self.opp, self.host
