"""
bot implementation.
"""
import os
import random

import ciscospark
import wolfram

# Sets config values from the config file
ACCESS_TOKEN_SPARK = "Bearer " + os.environ['access_token_spark']
WOLFRAMALPHA_CLIENT = os.environ['wolfram_client_id']
MYSELF = os.environ['my_person_id']


def random_dunno():
    """
    return random string
    """
    dunno_list = [
        'Dunno.',
        'It beats me.',
        'Your guess is as good as mine.',
        'Who knows?',
        'I have no idea.',
        'I don\'t have a clue.',
        'I don\'t have the faintest idea'
    ]

    return random.choice(dunno_list)


def handler(event, context):
    """
    nester
    """
    print "Event is {0}".format(event)

    try:
        room_id = event['data']['roomId']
        message_id = event['data']['id']
        person_id = event['data']['personId']
        person_email = event['data']['personEmail']
        # print "Yay - found room_id: {}, msg_id: {}".format(room_id, message_id)
        print "Consumer: {}".format(person_email)
    except KeyError as error:
        print "Duh - key error %r" % error
        return False

    if person_id == MYSELF:
        return False

    message = ciscospark.get_message(ACCESS_TOKEN_SPARK, message_id)
    user_query = message.get('text', "None")
    print "Query: {}".format(user_query)

    if user_query is None:
        return False

    if user_query.lower().startswith('nester'):
        user_query = user_query[6:]

    print "Query (final): {}".format(user_query)

    if "help" in user_query.lower():
        print "No trigger word. Returning ..."
        ciscospark.post_message_rich(
            ACCESS_TOKEN_SPARK, room_id, "Supported commands: help, or ask any factual question")
        return True

    result = wolfram.execute_spoken_query(WOLFRAMALPHA_CLIENT, user_query)
    if "did not understand" in result.lower() or "no spoken result" in result.lower():
        result = '{} Try a different factual question.'.format(random_dunno())

    ciscospark.post_message_rich(ACCESS_TOKEN_SPARK, room_id, result)
    return True
