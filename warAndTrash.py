import sys
from operator import itemgetter


def shuffle(deck, r):
    try:
        c = 0
        n = len(deck)
        while (c < n-1):
            try:
                rand = float(r.readline().strip())
            except ValueError:
                r.readline()
                rand = float(r.readline().strip())
            p = int(rand*(n-c) + c)
            deck[c], deck[p] = [deck[p], deck[c]]
#            print("Random number: {}".format(rand))
#            print("swapping card {} with card {}".format(c, p))
#            #input()
            c += 1
 
    except IndexError:
        print("Error, ran out of random numbers")
        sys.exit(1)

    return deck


def playWar(deck, r, N, T, L):
    score = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
                  '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    p1hand = deck[0:26]
    p2hand = deck[26:]
    p1winnings = []
    p2winnings = []

    limbo = []
    winner = 'na'

    while ((len(p1hand) + len(p1winnings) < 52) and (len(p2winnings) + len(p2hand) < 52)):
        if not p1hand:
            p1hand = shuffle(p1winnings, r)
            p1winnings = []
        if not p2hand:
            p2hand = shuffle(p2winnings, r)
            p2winnings = []

        p1card = p1hand.pop(0)
        p2card = p2hand.pop(0)

        limbo.extend([p1card, p2card])

        if (p1card == p2card):
            if (len(p1hand) + len(p1winnings) == 0):
                p2winnings.extend(limbo)
                limbo = []
            elif (len(p2hand) + len(p2winnings) == 0):
                p1winnings.extend(limbo)
                limbo = []
            else:
                continue

        elif (score[p1card] > score[p2card]):
            p1winnings.extend(limbo)
            limbo = []

        elif (score[p2card] > score[p1card]):
            p2winnings.extend(limbo)
            limbo = []

        N += 1
        if (len(p1hand) + len(p1winnings) > len(p2hand) + len(p2winnings)):
            if winner != 'p1':
                T += 1
                winner = 'p1'
                L = N
        elif (len(p1hand) + len(p1winnings) < len(p2hand) + len(p2winnings)):
            if winner != 'p2':
                T += 1
                winner = 'p2'
                L = N

    return winner, N, T, L

def emit(player, cleared, array, seen, inhand, discard, draw, N):
    print("Turn {}: Player {}.".format(N, player))
    print("Score: {}.".format(cleared))
    print("Card in hand: {}.".format(inhand))
    print("Array:")
    print("\t" + "\t".join([str(x+1) for x in range(len(array))]))
    print("\t" + "\t".join(array))
    print("\t" + "\t".join([str(x) for x in seen]))
    print("Discard pile: {}".format(" ".join(discard)))
    print("Draw pile: {}".format(" ".join(draw)))
    print()
    print()
    print()
    print()
    return




def startOfTurn(discard, draw, seen1, seen2, score1, score2, winner, r, N, T, L):
    N += 1
    if not draw:
        draw = shuffle(discard[:-1], r)
        discard = discard[-1]

    if (score1 > score2):
        if winner != 'p1':
            T += 1
            winner = 'p1'
            L = N
    elif (score1 < score2):
        if winner != 'p2':
            T += 1
            winner = 'p2'
            L = N
    else:
        seen1count = 0
        seen2count = 0
        for i in range(len(seen1)):
            seen1count += seen1[i]
            seen2count += seen2[i]
        if seen1count > seen2count:
            if winner != 'p1':
                T += 1
                winner = 'p1'
                L = N
        elif seen1count < seen2count:
            if winner != 'p2':
                T += 1
                winner = 'p2'
                L = N

    return discard, draw, winner, N, T, L

def countInDiscard(discard, value, score):
    count = 0
    for c in discard:
        if score[c] == value:
            count += 1
    return count

def countInHand(hand,seen,value,score):
    count = 0
    for i in range(len(hand)):
        if seen[i] and score[hand[i]] == value:
            count += 1
    return count

def countSeen(discard, hand1, seen1, hand2, seen2, value, score):
    return countInDiscard(discard, value, score) + countInHand(hand1, seen1, value, score) + countInHand(hand2, seen2, value, score)

def clear(array, discard, draw, r):
    # Shuffle the three card sources together
    draw = shuffle(draw + discard  + array, r)

    # Empty the discard pile and draw a new array
    discard = []
    size = len(array)
    array = []
    for i in range(size-1):
        array.append(draw.pop())

    return array, discard, draw

def playTrash(deck, r, N, T, L):
    score = {'A':0, '2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7, '9':8, '10':9,
             'J':-1, 'Q':50, 'K':50}
    winner = 'na'

    discard = []
    p1array = []
    p2array = []

    discard.append(deck.pop())

    for i in range(10):
        p1array.append(deck.pop())
    
    for i in range(10):
        p2array.append(deck.pop())
    draw = deck

    p1seen = [False]*10
    p2seen = [False]*10

    p1cleared = 0
    p2cleared = 0

    inhand = 'na'

    while (p1cleared < 10 and p2cleared < 10):
        # Start a new turn for player 1
        discard, draw, winner, N, T, L = \
                 startOfTurn(discard, draw, p1seen, p2seen, p1cleared, \
                                       p2cleared, winner, r, N, T, L)
        print("turn start")
        emit('p1', p1cleared, p1array, p1seen, inhand, discard, draw, N)
        #input()

        # If the top card on the discard pile is one you need
        # This conditional is a complicated way of saying:
        # If the card is a jack or a non-face card that we could use,
        # Grab it
        if (score[discard[-1]] == -1 or (
            score[discard[-1]] < len(p1array) and (
                not p1seen[score[discard[-1]]] or (
                    p1seen[score[discard[-1]]] and 
                    p1array[score[discard[-1]]] == 'J')))):

            inhand = discard.pop()          
            print("drew from discard")
            emit('p1', p1cleared, p1array, p1seen, inhand, discard, draw, N)

        # Draw from the draw deck
        else:
            inhand = draw.pop()
            print("drew from hand")
            emit('p1', p1cleared, p1array, p1seen, inhand, discard, draw, N)

        #input()

        # As long as we have more cards to play
        while (score[inhand] == -1 or (
            score[inhand] < len(p1array) and (
                not p1seen[score[inhand]] or (
                    p1seen[score[inhand]] and 
                    p1array[score[inhand]] == 'J')))):
            
            print("Continuing with card to play")
            # If our card is not a Jack
            emit('p1', p1cleared, p1array, p1seen, inhand, discard, draw, N)
            if score[inhand] >= 0:
                
                # Place the card in our array and pick up the card that was there
                p1seen[score[inhand]] = True
                swap = p1array[score[inhand]]
                p1array[score[inhand]] = inhand
                inhand = swap

                print("Placed non-jack card down")
                emit('p1', p1cleared, p1array, p1seen, inhand, discard, draw, N)
                #input()

            # If our card is a Jack
            else:

                # Initialize a dictionary of possible play positions
                options = {}

                # For each unseen card in our array 
                for i in range(len(p1array)):
                    if (p1seen[i]):
                        continue
                    # Count how many cards of that value that we know the location of
                    options[i] = countSeen(discard, p1array, p1seen, p2array, p2seen, i, score)


                # Find the location of the card that we have the highest probability of drawing
                maxLoc, maxVal = max(reversed(list(options.items())), key=itemgetter(1))
                #maxLoc = max(options, key=options.get)
                p1seen[maxLoc] = True
                swap = p1array[maxLoc]
                p1array[maxLoc] = inhand
                inhand = swap
                

                print("Placed jack down")
                emit('p1', p1cleared, p1array, p1seen, inhand, discard, draw, N)
                #input()

            # Check if every spot of the array has been filled
            if False not in p1seen:
    
                # Clear array and repopulate
                print("Clearing for p1")
                p1array, discard, draw = clear(p1array, discard, draw,r)
                p1seen = [False]*(len(p1seen)-1)
                p1cleared += 1
    
                print("Cleared array")
                emit('p1', p1cleared, p1array, p1seen, inhand, discard, draw, N)
                #input()

            if not p1array:
                break



        # Discard remainder of hand
        discard.append(inhand)
        inhand = 'na'
        print("Discarded hand, turn over")
        emit('p1', p1cleared, p1array, p1seen, inhand, discard, draw, N)
        #input()



        if p1cleared == 10:
            break


        print()
        print()
        print()
#        #input('Press any button to continue')


        # Start player 2's turn
        discard, draw, winner, N, T, L = \
                 startOfTurn(discard, draw, p1seen, p2seen, p1cleared, \
                             p2cleared, winner, r, N, T, L)

        
        print("turn start")
        emit('p2', p2cleared, p2array, p2seen, inhand, discard, draw, N)
        #input()

        # If the top card on the discard pile is one you need
        if (score[discard[-1]] == -1 or (
            score[discard[-1]] < len(p2array) and (
                not p2seen[score[discard[-1]]] or (
                    p2seen[score[discard[-1]]] and 
                    p2array[score[discard[-1]]] == 'J')))):

            inhand = discard.pop()
            print("Drew from discard")
            emit('p2', p2cleared, p2array, p2seen, inhand, discard, draw, N)

        # Draw from the draw deck
        else:
            inhand = draw.pop()
            print("Drew from deck")
            emit('p2', p2cleared, p2array, p2seen, inhand, discard, draw, N)
        
        #input()



        # As long as we have more cards to play
        while (score[inhand] == -1 or (
            score[inhand] < len(p2array) and (
                not p2seen[score[inhand]] or (
                    p2seen[score[inhand]] and 
                    p2array[score[inhand]] == 'J')))):
            
            print("Continuing with more cards to play")

            # If our card is not a Jack
            #emit('p2', p2cleared, p2array, p1seen, inhand, discard, draw, N)
            if score[inhand] >= 0:
                
                # Place the card in our array and pick up the card that was there
                p2seen[score[inhand]] = True
                swap = p2array[score[inhand]]
                p2array[score[inhand]] = inhand
                inhand = swap

                print("Placed non-jack card")
                emit('p2', p2cleared, p2array, p2seen, inhand, discard, draw, N)
                #input()


            # If our card is a Jack
            else:

                # Initialize a dictionary of possible play positions
                options = {}

                # For each unseen card in our array 
                for i in range(len(p2array)):
                    if (p2seen[i]):
                        continue
                    # Count how many cards of that value that we know the location of
                    options[i] = countSeen(discard, p1array, p1seen, p2array, p2seen, i, score)
                
                # Find the location of the card that we have the highest probability of drawing
                maxLoc, maxVal = max(reversed(list(options.items())), key=itemgetter(1))
                #maxLoc = max(options, key = options.get)
                p2seen[maxLoc] = True
                swap = p2array[maxLoc]
                p2array[maxLoc] = inhand
                inhand = swap

                print("Placed jack")
                emit('p2', p2cleared, p2array, p2seen, inhand, discard, draw, N)
                #input()
            


            # Check if every spot of the array has been filled
            if False not in p2seen:
        
                # Clear array and repopulate
                #print("Clearing for p2")
                p2array, discard, draw = clear(p2array, discard, draw,r)
                p2seen = [False]*(len(p2seen)-1)
                p2cleared += 1
        
                print("Cleared array")
                emit('p2', p2cleared, p2array, p2seen, inhand, discard, draw, N)
                #input()
    
            if not p2array:
                break
    
       
        # Discard remainder of hand
        discard.append(inhand)
        inhand = 'na'


        print("Discarded hand, turn over.")
        emit('p2', p2cleared, p2array, p2seen, inhand, discard, draw, N)
        #input()


        print()
        print()
        print()
#        #input('Press any button to continue')

    return winner, N, T, L

def play(gameName, r):

    N = 0
    T = 0
    L = 0.
    deck = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']*4
    deck = shuffle(deck, r)
    if gameName == 'war':
        winner, N, T, L = playWar(deck, r, N, T, L)


    elif gameName == 'trash':
        winner, N, T, L = playTrash(deck, r, N, T, L)

    else:
        print("Invalid arguments. Game name passed was not war or trash.")
        sys.exit(1)


    

    return N, T, float(L)/N



