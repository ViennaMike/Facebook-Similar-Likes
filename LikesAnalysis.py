import copy
import json
import numpy
from facepy import GraphAPI
from math import sqrt
import locale

# Needed so that alphabetic sort works correctly
locale.setlocale(locale.LC_ALL, "")

# Calculate Jaccard Similarity Coefficients
def jaccard(v1,v2):
    # Simple sums
    sum1=sum(v1)
    sum2=sum(v2)
    # intersection
    intersect =sum([v1[i]*v2[i] for i in range(len(v1))])
    unique1 = sum1 - intersect
    unique2 = sum2 - intersect
    # Calculate j (Jaccard score)
    if intersect == 0: return 0
    return intersect / (unique1+unique2+intersect)

# Return the n highest values in array:
def n_max(arr, n):
    indices = arr.ravel().argsort()[-n:]
    indices = (numpy.unravel_index(i, arr.shape) for i in indices)
    return [(arr[i], i) for i in indices]

# Get data from Facebook
# Get your user access token from https://developers.facebook.com/tools/explorer/ and paste in next line
graph = GraphAPI('PASTE YOUR USER TOKEN HERE')
my_likes = graph.get('me/likes')
friends = graph.get('me/friends/')
friend_likes=graph.get('me?fields=friends.fields(likes,name)')

# Get rid of unneeded stuff in my likes
my_likes.pop('paging', None)
myLikes = []
for page in my_likes['data']:
    myLikes.append(page['name'])
# This gives an array of the names of the pages I like

# Get rid of unneeded stuff in friends list:
friends.pop('paging', None)
friendsList = []
for page in friends['data']:
    friendsList.append(page['name'])
# This gives an array of the names of my Facebook friends
# Add myself
friendsList.append('Self')

# Extract only what's needed from list of page likes of friends
friend_likes.pop('id', None)
friend_likes['friends'].pop('paging', None)

likesList = []
row = {}
for friend in friend_likes['friends']['data']:
    friend.pop('id', None)
    pageList=[]
    if 'likes' in friend:
        friend['likes'].pop('paging', None)
        for pages in friend['likes']['data']:
            pageList.append(pages['name'])
    row['pages']=pageList
    row['name']=friend['name']
    likesList.append(copy.copy(row))

# Add my name and likes
me={}
me['pages']=myLikes
me['name'] = 'self'
likesList.append(copy.copy(me))

## Uncomment next line if you'd like to print out the full likes list (long)
## print json.dumps(likesList, sort_keys=True, indent=4, separators=(',', ': '))

# generate ordered list of unique page likes
# First combine the lists into one big list
combinedList = []
for l in likesList:
    combinedList.extend(l['pages'])

# Eliminate duplicates
uniqueList = list(set(combinedList))
# Put in alphabetical order
uniqueList.sort(cmp=locale.strcoll)

# Create matrix of friends vs. page likes, with 0 or 1 depending on whether
# or not the friend liked the page

# Create zero filled array
likesArray = numpy.zeros(shape=(len(uniqueList), len(likesList)))

# Populate array with a 1 in each cell where the friend likes the page
for person in likesList:
    for page in person['pages']:
        likesArray[uniqueList.index(page),likesList.index(person)] = 1


### Next section not currently used, but if you want to get pure number of overlapping friends
### between two liked pages or pure number of overlapping groups between two friends, this will
### do that for every pair of pages and friends
### Create transpose of this matrix
##likesArrayT = likesArray.T
##
### Multiple arrary by transpose to get matix with matrix of similar pages (common friends)
### Elements now show, for each pair pages, how many friends like both
##similarPagesArray = numpy.dot(likesArray,likesArrayT)
##
### Multiply in the other order to get matrix of similar friends (common pages)
### Elements now show, for each pair of friends, how many pages they have in common
##similarFriendsArray = numpy.dot(likesArrayT, likesArray)
##
### No information in number of similar pages liked by yourself, so set diagonal to zero
##for i in range(0,len(similarFriendsArray)):
##    similarFriendsArray[i,i] = 0

# Find top 3 pages in terms of likes
rowTotals = numpy.array([ sum(x) for x in likesArray ])
topThreePages = n_max(rowTotals, 3)
print "The three Facebook pages most liked by you and your friends are: "
for i in range(2, -1, -1):
    print uniqueList[topThreePages[i][1][0]]," with ", topThreePages[i][0], "likes"

# Calculate Jacccard coefficients
# Use this, because # of pages in common from similarFriendsArray is heavily influenced by total
# number of pages liked. Jaccard coefficient may be better metric for liking similar pages.
# First create array that will be people vs. people
similarityArray = numpy.zeros(shape = (len(likesList), len(likesList)))
for i in range(0,len(likesList)):
    for j in range(0, len(likesList)):
        similarityArray[i,j] = jaccard(list(likesArray[:,i]),list(likesArray[:,j]))
# Don't want diagonal elements
numpy.fill_diagonal(similarityArray, 0)

## Get most similar to self
selfIndex = len(likesList)-1
similarToMe = n_max(similarityArray[:, selfIndex], 1)
similarToMeName = friendsList[similarToMe[0][1][0]]
similarToMeScore = similarToMe[0][0]
itemsInCommonWithMe = list(set(likesList[similarToMe[0][1][0]]['pages']) & set(likesList[selfIndex]['pages']))
print "\n The most similar friend to me is ",similarToMeName
print "The correlation between page likes, on a 0 to 100% score, is: ", "{0:.0f}%".format(similarToMeScore * 100)
print "The page likes we have in common are: ",itemsInCommonWithMe
    
## Get most similar among friends and self
mostSimilar = n_max(similarityArray, 1)
mostSimilarFriends = [friendsList[mostSimilar[0][1][0]], friendsList[mostSimilar[0][1][1]]]
mostSimilarFriendsScore = mostSimilar[0][0]
itemsInCommon = list(set(likesList[mostSimilar[0][1][0]]['pages']) & set(likesList[mostSimilar[0][1][1]]['pages']))

print "\n The two most similar friends are ", mostSimilarFriends
print "The correlation between their page likes, on a 0 to 100% score, is: ", "{0:.0f}%".format(mostSimilarFriendsScore * 100)
print "The pages they have in common are: ", itemsInCommon                                  

