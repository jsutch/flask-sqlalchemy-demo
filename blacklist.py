"""
blacklist.py

This file just contains the blacklist of the JWT tokens–it will be imported by
app and the logout resource so that tokens can be added to the blacklist when the
user logs out.
"""
# This blacklists user ids 2 and 3
# blacklist = [2,3]
# BLACKLIST = set(blacklist)
BLACKLIST = set()
