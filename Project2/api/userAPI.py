import hug # hug -f api.py

# Users: 
#   Attributes: usernames, bio, email, password
#   Actions: follow, post messages
# Posts: 
#   Attributes: author username, post message, timestamps
#   Actions: repost -> URL of original post
# Timelines: 
#   Attributes: user (user Posts), home (followed users), public (all users)
#   (Reverse chronological order, newest first)

@hug.get('/user/{username}')
def user(username: str):
    '''returns userdata of given user'''
    
    if username == 'ty37':
        data = 'Tyler Revay'
    if username == 'steph15':
        data = 'Stephanie Wilkinson'
    if username == 'spritce718':
        data = 'Spencer DeMera'

    return '{data} -> {username}'.format(**locals())