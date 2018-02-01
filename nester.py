"""
bot implementation.
"""
import os
import wolfram

import ciscospark

# Sets config values from the config file
ACCESS_TOKEN_SPARK = "Bearer " + os.environ['access_token_spark']
WOLFRAMALPHA_CLIENT = os.environ['wolfram_client_id']
MYSELF = os.environ['my_person_id']


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
        result = 'Don\'t have a good answer for you. Try a different factual question.'

    ciscospark.post_message_rich(ACCESS_TOKEN_SPARK, room_id, result)
    return True


def for_future():
    """
    something for the future
    """
    # Try a different error when answer is not found.
    # I have no idea
    # I haven't a clue
    # I haven't the faintest idea
    # Who knows?
    # Your guess is as good as mine.
    # It beats me
    # Dunno.
    return False
