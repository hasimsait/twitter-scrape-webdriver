from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
maxiter=2#maximum degree of connections (length of the tree)
interval = 2.5# time that it takes to load a certain link, if it doesn't scroll to the end of each page, inrease this; the lower the value faster it works
#entire runtime depends on this variable, as you must wait untill the cards load, with my connection 2.3 when I'm lucky, 2.5 works fine on average
totaltime=0
forAPI=[] #if a given user has more than 540 connected, leave it to API so that you don't spend more than 1 minute on him/her as rate limit is 1 min, we need to beat it

#YOU WILL PROBABLY GET RATE LIMITED, DONT GO TOO WILD WITH THIS

def printToFile(connected,targetName):
    translationTable = str.maketrans("ğĞıİöÖüÜşŞçÇ₺", "gGiIoOuUsScCT")
    f = open(f'{targetName}.txt', "a")
    for conn in connected:
        try:
            f.write(conn.translate(translationTable)+"\n")
        except:
            print("Oops!", sys.exc_info()[0], "occurred while attempting to write this line to",targetName)
    f.close()
    return True
def readFileToList(targetName):
    with open(f'{targetName}.txt') as f:
        lines = f.read().splitlines()
    return lines

class TwitterBot:
    def __init__(self):
        #self.username=username
        #self.password=password
        self.bot=webdriver.Firefox()

    def login(self):
        print("login")
        self.bot.set_window_size(920, 2160)
        #resize the window to avoid connection recommendations from loading may need fixing
        self.bot.get('https://twitter.com/login')
        while(self.bot.current_url!="https://twitter.com/home"):
            time.sleep(interval)
        print("login done")

    def findconnections(self,username,maxScrolls=8):
        #returns a list of connections
        #print("finding connections of " + username)
        bot=self.bot
        connected={}
        i=0
        bot.get(username+ '/followers')
        time.sleep(interval)
        prevlastuser="prevuser"
        currlastuser="curruser"
        while(bot.current_url=="https://twitter.com/i/rate-limited" or bot.current_url== "https://twitter.com/logout/error"):
            time.sleep(20)#wait untill ratelimit times out
            bot.get(username+ '/followers')
            time.sleep(interval)
        #print(bot.current_url)
        while(prevlastuser!=currlastuser): 
            try:
                if(i>maxScrolls):
                    forAPI.append(username)
                    print("there are more than "+str(len(connected))+" followers of",username,"better use the API to get the rest.")
                    break
                #print(i)
                prevlastuser=currlastuser
                #give it some time to load
                user= bot.find_elements_by_class_name('r-ahm1il')
                users=[elem.get_attribute('href') for elem in user]
                #print(len(users))#print number of users you got in this scroll
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                #scroll down a bit to load the page since twitter works that way
                i+=1#number of scrolls
                
                time.sleep(interval)
                if(len(users)>0):
                    currlastuser=str(users[-1])
                    
                for user in users:
                    us=str(user)
                    if (us not in connected):
                        connected[str(user)]=username
                        #print (str(user))
            except:
                print("Oops!", sys.exc_info()[0], "occurred while finding the followers of",username)

        j=0
        bot.get(username+ '/following')
        time.sleep(interval)
        prevlastuser="prevuser"
        currlastuser="curruser"
        while(bot.current_url=="https://twitter.com/i/rate-limited" or bot.current_url== "https://twitter.com/logout/error"):
            time.sleep(20)#wait untill ratelimit times out
            bot.get(username+ '/following')
            time.sleep(interval)
        #print(bot.current_url)
        while(prevlastuser!=currlastuser): 
            try:
                if(i>maxScrolls or j>maxScrolls):
                    forAPI.append(username)
                    print("there are more than "+str(len(connected))+"accounts connected to",username,"better use the API to get the rest.")
                    break
                #print(j)
                prevlastuser=currlastuser
                #give it some time to load
                
                user= bot.find_elements_by_class_name('r-ahm1il')
                users=[elem.get_attribute('href') for elem in user]
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                #scroll down a bit to load the page since twitter works that way
                j+=1#number of scrolls
                
                time.sleep(interval)
                if(len(users)>0):
                    currlastuser=str(users[-1])
                for user in users:
                    us=str(user)
                    if (us not in connected):
                        connected[str(user)]=username
                        #print (str(user))
            except:
                print("Oops!", sys.exc_info()[0], "occurred while finding the users followed by",username)
                    
        #print(len(connected))
        return connected
                
    def getconnected(self,username):
        #this function is useless, it used to clean stuff up
        #start = time.time()
        links=self.findconnections(username)
        #end = time.time()
        #print(end-start)
        return links

    
    def addto(self,connections,connectionsiter1):
        for connection in connectionsiter1:
            if connection not in connections:
                connections[connection]=1
                #this could also be the user that is connected to the connection
        return connections

    def listAccs(self,link,maxScrolls,interval):
        #RETWEETS AND LIKES LIST MAX 80 USERS
        self.bot.set_window_size(400, 2160)
        #pass the link to people who liked a tweet, followed it, hashtags etc.
        #returns a dictionary that has the accs as keys
        #gives up after maxScrolls scrolls, returns whatever it got during those scrolls
        #print("people from " + link)
        bot=self.bot
        connected={}
        i=0
        bot.get(link)
        time.sleep(interval)
        prevlastuser="prevuser"
        currlastuser="curruser"
        while(bot.current_url=="https://twitter.com/i/rate-limited" or bot.current_url== "https://twitter.com/logout/error"):
            time.sleep(20)#wait untill ratelimit times out
            bot.get(link)
            time.sleep(interval)
        while(prevlastuser!=currlastuser): 
            try:
                if(i>maxScrolls):
                    print("there are more than "+str(len(connected))+" users in",link,"better use the API to get the rest.")
                    break
                #print(i)
                prevlastuser=currlastuser
                #give it some time to load
                user= bot.find_elements_by_class_name('r-ahm1il')
                #print(user)
                users=[elem.get_attribute('href') for elem in user]
                #print(users)
                #print(len(users))#print number of users you got in this scroll
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                #scroll down a bit to load the page since twitter works that way
                i+=1#number of scrolls
                
                time.sleep(interval)
                if(len(users)>0):
                    currlastuser=str(users[-1])
                    
                for user in users:
                    us=str(user)
                    if (us not in connected):
                        connected[str(user)]=1
                        print (str(user))
            except:
                print("Oops!", sys.exc_info()[0], "occurred while listing the accounts from",link)
        return connected

        

    def DFS(self,username,iternum,connections):
        if iternum==maxiter:
            return self.getconnected(username)
            #return a dict in connection:<username> format 
        elif iternum<maxiter:
            connections={}
            for person in self.getconnected(username):
                connections= self.addto(connections,self.DFS(person,iternum+1,connections))
                #connections is a dictionary of users that are connected to <username> connected:username format
            return connections
    
    def listTweets(self,link,maxScrolls,interval,outputTo):
        #PROB ONLY WORKS WITH TURKISH TWEETS, FIX LINE 238 FOR YOUR DESIRED LANGUAGE
        self.bot.set_window_size(400, 2160)
        #print("tweets by " + link.split('/').pop())
        bot=self.bot
        alltweets={}
        i=0
        try:
            bot.get(link)
            time.sleep(interval)
            lasttweet=""
            prevlasttweet="aa"
            while(bot.current_url=="https://twitter.com/i/rate-limited" or bot.current_url== "https://twitter.com/logout/error"):
                time.sleep(20)#wait untill ratelimit times out
                bot.get(link)
                time.sleep(interval)
            while(i<maxScrolls and lasttweet!=prevlasttweet): 
                try:
                    gettweets= bot.find_elements_by_css_selector("div[lang='tr']")
                    tweets=[elem.text.replace("\n", " ") for elem in gettweets]
                    bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                    #scroll down a bit to load the page since twitter works that way
                    i+=1#number of scrolls
                
                    time.sleep(interval)
                    #print(tweets)
                    #print(tweet)
                    prevlasttweet=lasttweet
                    lasttweet=tweets[-1]
                    for tweet in tweets:
                        alltweets[tweet]=link
                except:
                    print("Oops!", sys.exc_info()[0], "occurred while listing tweets by",link,"at scroll:",i,"scrolling again")
            printToFile(alltweets,outputTo)
            return alltweets
        except:
            print("couldn't get the link",sys.exc_info()[0], "occurred." )
            #SOMETIMES TWITTER LOADS THE PAGE BUT IT DOES NOT FINISH LOADING, RELOADING WORKS TOO BUT I DON'T INTEND TO RETRIEVE EVERYTHING SO SKIPPING IS FINE
    
    def listTweetsFromLink(self,link,maxScrollsLink,maxScrollsProfile,interval,outputTweetsTo):
        #provide a link that contains profiles (RTs, favs, hashtags, lists...), 
        #outputs the retrieved tweets to outputTweetsTo, returns the accounts it could not retrieve tweets from (blocked, rate limited etc.)
        profiles=self.listAccs(link,maxScrollsLink,interval)
        zeros=[]
        probablyprivate=[]
        for profile in profiles:
            try:
                tw=self.listTweets(profile,maxScrollsProfile,interval,outputTweetsTo)
                if(len(tw)==0):
                    zeros.append(profile)
            except:
                print("couldn't retieve", link,"'s tweets.",sys.exc_info()[0], "occurred." )
                zeros.append(profile)
        for profile in zeros:
            try:
                tw=self.listTweets(profile,maxScrollsProfile,interval,outputTweetsTo)
                if(len(tw)==0):
                    probablyprivate.append(profile)
            except:
                print("couldn't retieve", link,"'s tweets.",sys.exc_info()[0], "occurred." )
                probablyprivate.append(profile)
        print("------------------------------------------------------------------------------------------------------------------------------------------\nList of profiles tweets could not be retrieved from:")
        print(probablyprivate)
        return probablyprivate

ed=TwitterBot()
ed.login()
connected={}
ed.listTweetsFromLink("https://twitter.com/hasimsait",3,3,3,"x")
#connected=ed.DFS('yourprofilelink',2,connected)
#connected=ed.listAccs(<mylistmemberslink> or <twitter.com/X/followers>, dont try to list likes or rt, twitter only displays 80)
#connected=ed.getconnected('yourprofilelink')
#connected=ed.listTweets('https://twitter.com/hasimsait',5,3,targetname)


'''
THIS HAS BEEN ADDED AS LISTTWEETSFROMLINK, WITHOUT THE LAST 5 LOGIC
B=readFileToList("B")
tweetlen=[]
zeros=[]
def lastFiveIsAllZero(myList):
    #if last five elements of a list is  
    testList=myList[-5:]
    for num in testList:
        if num!=0:
            return False
    return True
for link in B:
    try:
        tweets=ed.listTweets(link,3,3,"bTweets")
        tweetlen.append(len(tweets))
        if(len(tweets)==0):
            zeros.append(link)
        if(lastFiveIsAllZero(tweetlen)):
            #last five accounts all being private seems unlikely to me, 
            # change the lastfiveisallzero if you want more, dont forget that you will skip that many accounts when you get rate limited
            time.sleep(60*3)#this needs tuning
            print("We've hit the rate limit.")
    except:
        print(sys.exc_info()[0], "occurred.")

skipped=[]
output=readFileToList("output")
for i in range(len(output)):
    try:
        if output[i+1]=="Oops! <class 'IndexError'> occurred.":
            skipped.append(output[i].split(" ").pop())
    except:
        print(".d")
skippedlinks=['https://twitter.com/'+skippedlink for skippedlink in skipped]
for link in skippedlinks:
    try:
        tweets=ed.listTweets(link,3,3,"bTweets")
        tweetlen.append(len(tweets))
        if(len(tweets)==0):
            zeros.append(link)

    except:
        print(sys.exc_info()[0], "occurred.")
print(zeros)
'''