# ILNewsDiff

See feed here: https://twitter.com/ILNewsDiff

A Twitter bot that keeps track of changes made in Israeli news websites.

Currently tracking:
 * [Haaretz](https://www.haaretz.co.il/)
 * [Israel Hayom](https://Israelhayom.co.il/)
 * [Walla](https://www.walla.co.il/)
 
How does it work?
------------
Once a minute the code queries news RSS feeds and compares them to a previous state saved in a local SQLite DB.

If an _interesting_ change is found, a tweet is published with the diff.

The first tweet of a diff is always the article itself as a link, and all the subsequent changes are chained by order. 

### What is _interesting_?
A change that
 * Has happened and is not there because of a delay in the RSS feed. The code queries the article's page to look for the change.
 * Is not comprised of only whitespace or punctuation. 
 * Has a difference of more than one letter (Though adding/removing a question mark '?' is interesting)
 

Installation
------------
+ The [phantomjs](http://phantomjs.org/) binary needs to be installed and the path updated in the run_diff.sh file.
+ `pip install -r requirements.txt`

[Twitter keys](https://dev.twitter.com/) are needed.

Credits
-------
Based on @j-e-d's code for the Twitter bot [@nyt_diff](https://twitter.com/nyt_diff).  
RSS feed fetching added for @xuv's Twitter bot [@lesoir_diff](https://twitter.com/lesoir_diff)

+ Original script and idea: @j-e-d Juan E.D. http://unahormiga.com/
+ RSS fetching: @xuv Julien Deswaef http://xuv.be
+ Font: [Merriweather](https://fonts.google.com/specimen/Merriweather)
+ Background pattern: [Paper Fibers](http://subtlepatterns.com/paper-fibers/).
