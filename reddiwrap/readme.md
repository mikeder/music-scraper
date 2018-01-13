reddiwrap
---------

reddiwrap is a python wrapper for communicating with the reddit.com API.

Compatible with Python 2.6.7, 2.7.1, and 3.2.3

----

Interacting with the reddit API is not very difficult, but figuring it out can take a while.

This class allows the interaction with reddit to be simple and easy.

reddiwrap makes it easy to:

  * login to your reddit account,
  * load posts from:
    * subreddits,
    * user pages,
    * search results.
  * navigate to 'next' and 'previous' pages.
  * vote on posts and comments,
  * save/unsave, hide/unhide, share and report posts,
  * submit links and self-posts,
  * comment on posts and other comments,
  * read, mark, compose and reply to private messages
  * view your own or others' user info,
  * view/subscribe/unsubscribe to the list of public subreddits,
  * moderator functions:
    * remove/approve/mark as spam for comments and posts
    * add/remove approved submitters
    * add/remove moderators
    * distinguish your own comments/posts with the moderator tag
  * mark posts as NSFW
  

Sample usage:
-------------

    # To upvote the first post on the /r/pics front page.
    
    from ReddiWrap import ReddiWrap
    
    reddit = ReddiWrap() # Create new instance of ReddiWrap
    
    login_result = reddit.login('your_username', 'your_password')
    
    if login_result != 0: # Anything other than '0' means an error occurred
      print 'unable to log in.'
      exit(1)
    
    pics = reddit.get('/r/pics')  # Get posts on the front page of reddit.com/r/pics
    reddit.upvote(pics[0])        # Vote
    
    
    
    # To reply back to every message in your inbox:
    
    msgs = reddit.get('/message/inbox') # Get messages
    
    for msg in msgs: # Iterate over the messages
      
      # Parrot back what the original message contained
      reddit.reply(msg, 'You said: \n\n>' + msg.body)
    

More examples showing how reddiwrap works are available in [ReddiWrapTest.py](https://github.com/derv82/reddiwrap/blob/master/ReddiWrapTest.py).


License
-------

ReddiWrap is licensed under the GNU General Public License version 2 (GNU GPL v2)

(C) Copyright 2012 Derv Merkler
