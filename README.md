Facebook-Similar-Likes
======================

Python script that analyzes the page likes of you and your friends.

This script uses the Facebook API to download the page likes of you and all your friends. It then prints out:

  1) the three pages that have the most likes amongst you and your friends
  2) the friend most similar to you in terms of page likes (using the Jaccard coeffiecient as the measure 
     (see http://en.wikipedia.org/wiki/Jaccard_index).  It prints out the similarity score and what pages
     you have in common
  3) the two friends who are most similar to each other in terms of page likes (again, using the same metric
     and printing out the same information)
     
The program does NOT get the required Facebook user access token for account.  You need to go to 
https://developers.facebook.com/tools/explorer/ to do so, and then paste it where indicated in the program.
A nice addition would be for someone to turn this into a web service, and included logging into Facebook and getting
the required token.

Thanks to "Programming Collective Intelligence" by Toby Segaran for some of the ideas used.  

Also thanks to Kieran Healye's article at http://kieranhealy.org/blog/archives/2013/06/09/using-metadata-to-find-paul-revere/
for inspiring this exercise. The code includes calculating the various matrices described in the article, although that
part is commented out, as I ended up not going further with it.  Another great addition would be to add some of th linkage
visualizations as shown in that article.
