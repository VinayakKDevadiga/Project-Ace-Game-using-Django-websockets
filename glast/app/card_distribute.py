# list containing all cards
cardlist = [
    'SA', 'SK', 'SQ', 'SJ', 'S10', 'S9', 'S8', 'S7', 'S6', 'S5', 'S4', 'S3', 'S2',
    'FA', 'FK', 'FQ', 'FJ', 'F10', 'F9', 'F8', 'F7', 'F6', 'F5', 'F4', 'F3', 'F2',
    'HA', 'HK', 'HQ', 'HJ', 'H10', 'H9', 'H8', 'H7', 'H6', 'H5', 'H4', 'H3', 'H2',
    'DA', 'DK', 'DQ', 'DJ', 'D10', 'D9', 'D8', 'D7', 'D6', 'D5', 'D4', 'D3', 'D2'
] 

def distribute_cards(no_of_players,cardlist):
    """
    Distributes the cards in the cardlist to the specified number of players.

    Parameters:
    no_of_players (int): The number of players to distribute the cards to.
    cardlist (list): The list of cards to be distributed.

    Returns:
    tuple: A tuple containing a list of player hands and the index of the player who has the 'SA' card.
    """
    
    # Creating lists for each player
    playerlists = [[] for _ in range(no_of_players)]
    
    # Variable to know who holds the 'Spade A' card to start the game
    starter_index = None

    # Distributing cards
    import random
    while cardlist:  # If cardlist is nonempty, it returns true
        for player in playerlists:
            if cardlist:
                card = cardlist.pop(random.randint(0, len(cardlist) - 1))
                player.append(card)
                if card == 'SA':
                    starter_index = playerlists.index(player)  # Get the index of the player in playerlists
                if not cardlist:
                    break
    return playerlists, starter_index