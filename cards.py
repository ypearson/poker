#!/usr/bin/env python3
import random
import pprint
import copy
from itertools import cycle
pp = pprint.PrettyPrinter(indent=4)

FIVE_CARDS = 5
FIVE_CARD_POKER = FIVE_CARDS
NUM_OF_CARD_SUITS = 4
NUM_OF_CARD_VALUES = 13

HANDS_SEQUENTIAL=['Royal Flush', 'Straight Flush', 'Straight']
HANDS_SAME_SUIT=['Royal Flush', 'Flush']

HANDS_WITHOUT_PAIRS=['High Card', 'Straight', 'Flush', 'Straight Flush', 'Royal Flush']
HANDS_WITH_PAIRS=['Pair', 'Two Pair', 'Three of a kind', 'Full House', 'Four of a kind']

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
    print(hand)
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
    return list(filter(lambda x: x!=None, grouped_hand))

def get_card_groupings(grouped_cards):
    groupings = []
    for i in range(0,len(grouped_cards)):
        groupings += [len(grouped_cards[i]['suit'])]
    groupings.sort()
    return groupings

def print_hand(hand, txt='HAND'):
    hand = sort_cards(hand)
    print('The current hand is....')
    print(f'########{txt}########')
    for i in range(0,len(hand)):
        print(f'# {hand[i]["card_value"]}\tof {hand[i]["suit"]}')
    print(f'########{txt}########')

while True:

    hand = get_new_hand_from_new_deck()

    grouped_cards = group_cards(hand)

    group_len = len(grouped_cards)


    # hand = \
    # [{'order': 8, 'card_value': 'NINE', 'suit': 'DIAMONDS'},
    # {'order': 9,  'card_value': 'TEN', 'suit': 'DIAMONDS'},
    # {'order': 10, 'card_value': 'JACK', 'suit': 'DIAMONDS'},
    # {'order': 11, 'card_value': 'QUEEN', 'suit': 'DIAMONDS'},
    # {'order': 12, 'card_value': 'KING', 'suit': 'DIAMONDS'}]

    print_hand(hand)

    if group_len == FIVE_CARDS:

        print("No pairs...Possible hands: ")
        print(*HANDS_WITHOUT_PAIRS, sep=', ')

        is_seq = is_hand_sequential(hand)
        is_same_suit = is_hand_same_suit(hand)

        if is_seq and is_same_suit:

            card_high = get_high_card(hand)['card_value']
            card_low = get_low_card(hand)['card_value']

            if card_high == 'KING' and card_low == 'ACE':
                print("Royal Flush!")
                break

            else:
                print("Straight Flush")
        elif group_len == 5:
            print(f'Found {HANDS_WITHOUT_PAIRS[0]}')
            print_hand(hand, txt='HIGH CARD')
    else:
        print("Pairs found...Possible hands: ")
        print(*HANDS_WITH_PAIRS, sep=', ')

        if group_len == 4:
            print_hand(hand,'PAIR')
        elif group_len == 3:
            groupings = get_card_groupings(grouped_cards)
            if groupings == [1,2,2]:
                print_hand(hand,'TWO PAIR')
            elif groupings == [1,1,3]:
                print_hand(hand,'3 Of a Kind')
            else:
                assert False
        elif group_len == 2:
            groupings = get_card_groupings(grouped_cards)
            if groupings == [1,4]:
                print_hand(hand,'4 Of a Kind')
                # break
            elif groupings == [2,3]:
                print_hand(hand,'FullHouse')
                # break
