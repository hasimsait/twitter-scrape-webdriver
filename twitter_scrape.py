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
            print("Oops!", sys.exc_info()[0], "occurred.")
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

    def findconnections(self,username):
        #returns a list of connections
        print("finding connections of " + username)
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
                if(i>8):
                    forAPI.append(username)
                    print(username)
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
                    '''
                    if (us not in connected) and ('t.co/' not in us )and us != None:
                        connected[str(user)]=username
                        print (str(user))#still dirty, will contain username's username too, requires some additional cleanup or iternum for dfs
                        '''
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")

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
                if(i>8 or j>8):
                    forAPI.append(username)
                    print(username)
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
                        print (str(user))
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")
                    
        print(len(connected))
        return connected
                
    def getconnected(self,username):
        #this function is useless, it used to clean stuff up
        start = time.time()
        links=self.findconnections(username)
        end = time.time()
        print(end-start)
        #counting will decrease performance but i want to see it, TODO delete when done
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
        print("people from " + link)
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
                    print("there are more than "+str(len(connected))+" users in this link.")
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
                print("Oops!", sys.exc_info()[0], "occurred.")
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
        #RETWEETS AND LIKES LIST MAX 80 USERS
        self.bot.set_window_size(400, 2160)
        #pass the link to people who liked a tweet, followed it, hashtags etc.
        #returns a dictionary that has the accs as keys
        #gives up after maxScrolls scrolls, returns whatever it got during those scrolls
        print("tweets by " + link.split('/').pop())
        bot=self.bot
        alltweets={}
        i=0
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
                print("Oops!", sys.exc_info()[0], "occurred.")
        printToFile(alltweets,outputTo)
        return alltweets

ed=TwitterBot()
ed.login()
connected={}

#connected=ed.DFS('yourprofilelink',2,connected)
#connected=ed.listAccs(<mylistmemberslink> or <twitter.com/X/followers>, dont try to list likes or rt, twitter only displays 80,100,5)
#connected=ed.getconnected('yourprofilelink')
#connected=ed.listTweets('https://twitter.com/hasimsait',5,3,targetname)

B=readFileToList("B")
for link in B:
    tweets=ed.listTweets(link,3,3,"bTweets")
