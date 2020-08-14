import random
import config
import os


class Player:
    def __init__(self, player_id, board, deck):
        self.id = player_id
        self.board = board
        self.deck = deck
        self.hand = None
        self.discard = None
        self.leader_used = False
        self.draw_hand()

    def change_hand(self):
        for cards_changed in range(config.PLAYER_CARD_CHANGE_LIMIT):
            self.print_hand()
            command = int(input(f'Specify card number (1 - {config.PLAYER_HAND_SIZE}) to change it or 0 to finish: '))
            if not command:
                break
            else:
                new_card = self.deck.pop(random.randint(0, len(self.deck)))
                self.deck.append(self.hand[command - 1])
                self.hand[command - 1] = new_card
        else:
            self.print_hand()

    def print_hand(self):
        for i, card in enumerate(self.hand, 1):
            print(f'#{i} - {card}')

    def draw_hand(self):
        indexes = random.sample(range(config.PLAYER_HAND_SIZE + 1), config.PLAYER_HAND_SIZE)
        self.hand = [self.deck[i] for i in indexes]
        for card in self.hand:
            self.deck.remove(card)
        self.change_hand()

    def get_menu_message(self):
        menu_message = '0 - pass\n1 - play a card'
        if not self.leader_used:
            menu_message += '\n2 - use leader_ability'
        menu_message += '\nSpecify action: '
        return menu_message

    def get_menu_command(self):
        available_commands = [0, 1]
        if not self.leader_used:
            available_commands += [2]
        while True:
            command = int(input(self.get_menu_message()))
            if command in available_commands:
                return command

    def play_turn(self):
        command = self.get_menu_command()


p = Player(0, None, [x for x in range(1, 31)])
p.play_turn()
