#!/usr/bin/env python3
import sys
import random
import copy
from itertools import cycle

FIVE_CARDS = 5
FIVE_CARD_POKER = FIVE_CARDS
NUM_OF_CARD_SUITS = 4
NUM_OF_CARD_VALUES = 13
poker_hands={\
            'High Card': 0,
            'Pair': 0,
            'Two Pair': 0,
            '3 of a kind': 0,
            'Straight': 0,
            'Flush': 0,
            'FullHouse': 0,
            '4 of a kind': 0,
            'Straight Flush': 0,
            'Royal Flush': 0}

def sort_cards(cards):
    return copy.deepcopy(sorted(cards, key=lambda x:x['order'], reverse=False))

def build_deck():
    i_value, i_suit, deck = 0, 0, []
    card_suits_gen  = cycle(['CLUBS', 'DIAMONDS', 'HEARTS', 'SPADES'])
    card_values_gen = cycle(['ACE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX',\
        'SEVEN', 'EIGHT', 'NINE', 'TEN', 'JACK', 'QUEEN', 'KING'])
    for value in card_values_gen:
        for suit in card_suits_gen:
            deck += [{'order': i_value, 'card_value': value, 'suit': suit}]
            i_suit+=1
            if i_suit == NUM_OF_CARD_SUITS:
                i_suit = 0
                break
        i_value+=1
        if i_value==NUM_OF_CARD_VALUES:
            return deck

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

def draw_from_deck(deck, num_of_cards=FIVE_CARD_POKER):
    new_hand = []
    for i in range(0,num_of_cards):
        new_hand+=[random.choice(deck)]
        deck.remove(new_hand[i])
    return new_hand

def get_new_hand_from_new_deck(num_of_cards=FIVE_CARD_POKER):
    deck = build_deck()
    deck = shuffle_deck(deck)
    return draw_from_deck(deck, num_of_cards)

def get_high_card(hand):
    hand = sort_cards(hand)
    return hand[-1]

def get_low_card(hand):
    hand = sort_cards(hand)
    return hand[0]

def is_hand_same_suit(hand):
    ret = True
    suit_match = hand[0]['suit']
    for i in range(1,len(hand)):
        if hand[i]['suit'] != suit_match:
            ret = False
            break
    return ret

def is_hand_sequential(hand):
    ret = True
    hand = sort_cards(hand)
    has_ace = True if hand[0]['card_value'] =='ACE' else False
    card = hand[0]['order']
    for i in range(1,len(hand)):
        if not has_ace:
            if card + 1 == hand[i]['order']:
                card = hand[i]['order']
            else:
                ret = False
                break
        else:
            if card + 1 == hand[i]['order']:
                card = hand[i]['order']
            elif hand[i]['card_value']  == 'TEN':
                card = hand[i]['order']
            else:
                ret = False
                break
    return ret

def group_cards(hand):
    grouped_hand = sort_cards(hand)
    for i in range(0,len(grouped_hand)):
        grouped_hand[i]['suit'] = [grouped_hand[i]['suit']]
    card = grouped_hand[0]
    for i in range(1,len(hand)):
        if card['order'] == grouped_hand[i]['order']:
            grouped_hand[i]['suit'] += card['suit']
            grouped_hand[i-1] = None
            card = grouped_hand[i]
        else:
            card = grouped_hand[i]
    grouped_cards = list(filter(lambda x: x!=None, grouped_hand))
    group_len = len(grouped_cards)
    return group_len, grouped_cards

def get_card_groupings(grouped_cards):
    groupings = []
    for i in range(0,len(grouped_cards)):
        groupings += [len(grouped_cards[i]['suit'])]
    groupings.sort()
    return groupings

def print_hand(hand, txt='HAND', flag=True):
    if flag:
        hand = sort_cards(hand)
        print(f'########{txt}########')
        for i in range(0,len(hand)):
            print(f'# {hand[i]["card_value"]}\tof {hand[i]["suit"]}')
        print(f'########{txt}########')

def print_hand_bins(hand_bins, cnt):
    print(f'########HAND_FREQUENCY########')
    for hand_label, hand_freq in hand_bins.items():
        print(f'{hand_label:<15}-->{hand_freq:^10} ({100*hand_freq/cnt:2.2f}%)')
    print(f'########HAND_FREQUENCY########')

if __name__ == '__main__':

    DEBUG = False
    hand_label = ''
    iterations = 0
    num_of_hands = 1_000

    try:
        num_of_hands = int(sys.argv[1])
    except Exception as e:
        pass

    print(f'Number of poker hand iterations {num_of_hands}. Printing turned {"ON" if DEBUG else "OFF"}')

    while iterations < num_of_hands:

        iterations+=1
        hand = get_new_hand_from_new_deck()
        group_len, grouped_cards = group_cards(hand)

        if group_len == FIVE_CARDS: # no pairs

            is_seq = is_hand_sequential(hand)
            is_same_suit = is_hand_same_suit(hand)

            if is_seq and is_same_suit:

                card_high = get_high_card(hand)['card_value']
                card_low = get_low_card(hand)['card_value']

                if card_high == 'KING' and card_low == 'ACE':
                    hand_label = 'Royal Flush'
                else:
                    hand_label = 'Straight Flush'
            elif is_same_suit:
                hand_label = 'Flush'
            elif is_seq:
                hand_label = 'Straight'
            elif group_len == 5:
                hand_label = 'High Card'
        else:
            if group_len == 4:
                hand_label = 'Pair'
            elif group_len == 3:
                groupings = get_card_groupings(grouped_cards)
                if groupings == [1,2,2]:
                    hand_label = 'Two Pair'
                elif groupings == [1,1,3]:
                    hand_label = '3 of a kind'
                else:
                    assert False
            elif group_len == 2:
                groupings = get_card_groupings(grouped_cards)
                if groupings == [1,4]:
                    hand_label = '4 of a kind'
                elif groupings == [2,3]:
                    hand_label = 'FullHouse'

        poker_hands[hand_label]+=1
        print_hand(hand, txt=hand_label, flag=DEBUG)

print_hand_bins(poker_hands, num_of_hands)