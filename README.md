Overview
========

Processes a [json formatted Pinboard export][pinboard_export] and tests each
link to determine if it's reachable. Invalid links are reported, along with
a reason, in markdown formatted text.

Usage
=====

    Usage: pinboard_linkrot.py <bookmarks.json> [space separated tags to ignore]

All arguments after the bookmarks file will be considered tags you want to
ignore. Any bookmarks with these tags will be skipped. Usefull for
bookmarklets that can't be validated or links only accessible from a network
you're not currently connected to.

Dependencies
============

Requires the Python [Requests][python_requests] module.

[pinboard_export]: https://pinboard.in/export/
[python_requests]: http://docs.python-requests.org/en/latest/
