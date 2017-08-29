# About

This project allows to get the ids for an entire thread in twitter. It works
by giving an **id** of a tweet of the thread and it take cares of looking for
The previous tweets and get following ones.

The best performance is archived using as *root* (starting point) the last tweet,
Since it just follows the chain. Using the first one as a root has the worst performance
as it has to look for more tweets in a twitter search.

# Use

By now you need to configure the database (I use peewee with postgresql).
To get the threat call the **root** function in *status.py* with the id of a tweet.
