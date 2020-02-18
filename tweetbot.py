import k
import os
import sys
import time
import tweepy
import random
import chris_key
import cheong_key
import rosealerts
from copy import deepcopy
from Twper import TwitterAccount
from progress.bar import ShadyBar
from datetime import datetime, timedelta

################################################################################

# rohhse account authorization
auth = tweepy.OAuthHandler(k.consumer_key, k.consumer_secret)
auth.set_access_token(k.access_token, k.access_token_secret)
api = tweepy.API(auth)

# rosebot account authorization
auth = tweepy.OAuthHandler                                                                                                                                                                                                                        ("eYwzKMn3Q6rAU9LcFOufRvtRd", "ESeS01LEs2ijkOf9bUX39YRezn5YRG2Xmq4mAjtTNdk2oqNu9C")
auth.set_access_token                                                                                                                                                                                                                             ("1085633491826466816-nE1o9NzliI6kLq45voiJj5SHYsAIGE", "Xv2anW58KAVm6QqqxSSXRhWX6IdA6VSdPTfXELxb7wR9G")
api2 = tweepy.API(auth)

# cheong
auth = tweepy.OAuthHandler(cheong_key.consumer_key, cheong_key.consumer_secret)
auth.set_access_token(cheong_key.access_token, cheong_key.access_token_secret)
api3 = tweepy.API(auth)

# cheong
auth = tweepy.OAuthHandler(chris_key.consumer_key, chris_key.consumer_secret)
auth.set_access_token(chris_key.access_token, chris_key.access_token_secret)
api4 = tweepy.API(auth)

# rosealerts
auth = tweepy.OAuthHandler(rosealerts.consumer_key, rosealerts.consumer_secret)
auth.set_access_token(rosealerts.access_token, rosealerts.access_token_secret)
ra = tweepy.API(auth)

################################################################################

me = "@rohhse"

# last follower
f = open("l.txt", "r+")
last_flwr = f.read()
f.close()

top5 = {}
today = {} # dictionary of tweets liked today

ids = "" # id of everyone im following
wait = 500 # sec
myinfo = "" # my info
myratio = 0 # my follower ratio
like_speed = 10
hour_check = 0 # checks if first iteration of hour

frilis = [] # friends list
whitelist = [] # list of people not to unfollow
all_tweets = [] # keep track of all tweets
sleeparray = []
exceptionlist = []
bd_list = []
all_alerts = []
daily_report = []
unfollowed_you = ""
fol_num = 0

# initialize array
j = 0
while j < 55:
    all_tweets.append(" ")
    j += 1

################################################################################

# send to rose
def rosealert(msg):
    try:
        if msg not in all_alerts:
            all_alerts.append(msg)
            ra.update_status("@rohhse " + msg)
    except:
        pass

# clear terminal
def d():
    os.system('cls')

# ME FIGURE OUT WHO INACTIVE OR WHO UNFOLLOW #
def check_unfollow():
    global unfollowed_you
    # ids of all friends
    ids = api.friends_ids(me)
    # date of last year
    last_year = datetime.now() - timedelta(days = 365)

    # makes whilelist array
    with open("w.txt", "r") as f:
        whitelist = [line.strip() for line in f]

    followers = api.followers_ids(me)
    for person in ids:
        screenname = api.get_user(person).screen_name
        # whitelist
        if str(person) in whitelist:
            continue
        # unfollow if not mutual
        if person not in followers:
            unfollowed_you += "\n" + str(screenname) + " unfollowed u"
            # dm_msg = str(screenname) + " unfollowed u"
            # rosealert(dm_msg)
            # unfollow(person)
            continue
        try:
            # check if last tweet is older than year
            last_tweet = api.user_timeline(person)[0].created_at
            if last_tweet < last_year:
                unfollowed_you += "\n" + str(screenname) + " inactive"
                # dm_msg = str(screenname) + " inactive"
                # rosealert(dm_msg)
                # unfollow(person)
        except:
            try:
                # try another tweet
                last_tweet = api.user_timeline(person)[1].created_at
                if last_tweet < last_year:
                    unfollowed_you += "\n" + str(screenname) + " inactive"
                    # dm_msg = str(screenname) + " inactive"
                    # rosealert(dm_msg)
                    # unfollow(person)
            except:
                # something went wrong
                unfollowed_you += "\n" + "!!!!" + str(screenname) + " unfollow code error"
                # dm_msg = "!!!!" + str(screenname) + " unfollow code error"
                # rosealert(dm_msg)

# ME LOOK THROUGH TIMELINE AND LIKE THINGS I NO SEE BEFORE #
def like():
    count = 0
    # get tweet from timeline
    public_tweets = api.home_timeline()

    # like tweets in timeline
    for tweet in public_tweets:
        try:
            name = tweet.user.screen_name
            a = tweet.text[0]
            b = tweet.text[1]
            ttext = str(tweet.text)
            if "\n" in ttext:
                ttext.replace("\n", ",").strip()
            # not a retweet
            if a != "R" and b != "T":
                # not a reply to someone else
                if a != "@":
                    # am following them
                    if tweet.user.id in ids:
                        if not tweet.favorited:
                            count += 1
                            # like it and print to terminal
                            api.create_favorite(tweet.id)
                            all_tweets.append(str(name) + ": " + ttext)
                            # add to dictionary
                            if name in today:
                                today[name] = int(today[name]) + 1
                            else:
                                today[name] = 1
        except Exception as e:
            exceptionlist.append(str(e))
            count += 1
    return count

# ME SLEEP ME SLEEP ME SLEEP ME SLEEP LEAVE TWITTER ALONE #
def sleepfor(thisamount):

    d()

    # print (55) tweets
    global all_tweets
    # delete tweets until only 55
    while len(all_tweets) > 55:
        all_tweets.pop(0)
    # print all into console
    for atweet in all_tweets:
        print(atweet)

    # exception list (5)
    global exceptionlist
    try:
        if exceptionlist:
            dm_msg = "ERRORS: " + ', '.join(exceptionlist)
            rosealert(dm_msg)
            exceptionlist = []
    except:
        exceptionlist = []

    # loading bar (1)
    suffix = '%(percent)d%% [%(elapsed_td)s]'
    with ShadyBar(" go away ", suffix=suffix, max=thisamount) as bar:
        for i in range(0, int(thisamount)):
            try:
                bar.next()
                time.sleep(1)
            except:
                pass

    timetaken = int(thisamount / 60)
    all_tweets.append("--- " + str(timetaken) + "min ---")

    d()

# ME TELL U TOP 5 PEOPLE WHO TWEET THE MOST #
def dict_stuff():
    # limit to only 5
    if len(today) > 5:
        top5 = sorted(today, key=today.get, reverse = True)[:5]
        dm_msg = "top tweeters: " + ', '.join(top5)
        rosealert(dm_msg)

# ME UNFOLLOW IF U WANT #
def unfollow(person):
    api.destroy_friendship(person)

# ME DEAL WITH NEW FOLLOWERS #
def newfollower(last_flwr):
    new_flwr = api.followers(me)[0].screen_name
    # got new follower
    if last_flwr != new_flwr:
        # print to terminal
        all_tweets.append("new follower: " + new_flwr)
        # follow if good ratio
        userinfo = api.get_user(new_flwr)
        ratio = userinfo.followers_count / userinfo.friends_count
        # check mutuals
        mutual_list = []
        ex = ""
        try:
            i = 0
            their_followers = api.followers_ids(new_flwr)
            global frilis
            for f in their_followers:
                if f in frilis:
                    mutual_list.append(api.get_user(f).screen_name)
                    i += 1
        except Exception as e:
            i = 0
            ex = str(e)
        followed = "not followed"
        # follow if 10+ mutuals
        if (ratio > myratio and i > 10) or i > 20:
            birthday(new_flwr)
            api.create_friendship(new_flwr)
            followed = "followed"
        if mutual_list:
            mutual_print = ', '.join(mutual_list[0:5])
        else:
            mutual_print = "None"
        # send to rosealerts
        dm_msg = "NEW FOLLOWER: " + new_flwr + str(int(ratio)) + "\n" + "mutuals (" + str(i) + ") : " + str(mutual_print) + "\n" + followed
        rosealert(dm_msg)
        if ex:
            rosealert(ex)
        # update value for next time
        last_flwr = new_flwr
        f = open("l.txt", "w+")
        f.write(last_flwr)
        f.close()
    return last_flwr

# DYNAMIC SLEEPY TIME #
def calc_wait(wait, count):
    x = 250
    if count < 3:
        wait += x
    elif count > 5:
        if wait > x:
            wait -= x
    return wait

# CHECK IF NEW ROHHSE TWEET #
def check_newtweet():
    global exceptionlist
    new_tweet = api2.user_timeline("@rohhse")[0]
    text = new_tweet.text

    try:
        global gen_tweet_count
        gen_tweet_count = 0
        # like
        if not new_tweet.favorited:
            api2.create_favorite(new_tweet.id)

        # retweet if not reply
        if text[0] != "@":
            try:
                api3.create_favorite(new_tweet.id)
            except:
                pass
            try:
                api4.create_favorite(new_tweet.id)
            except:
                pass
            if not new_tweet.retweeted:
                api2.retweet(new_tweet.id)
    # some error
    except Exception as e:
        exceptionlist.append(str(e))

# STORE LIKED TWEETS #
def sleep_tweets():
    global sleeparray
    # get tweet from timeline
    public_tweets = api.home_timeline()

    # like tweets in timeline
    for tweet in public_tweets:
        try:
            # not a retweet
            if a != "R" and b != "T":
                # not a reply to someone else
                if a != "@":
                    # am following them
                    if tweet.user.id in ids:
                        if not tweet.favorited:
                            sleeparray.append(tweet.id)
        except:
            pass

# CATCH UP ON SLEEP TWEETS #
def like_stored_tweets():
    global sleeparry
    global like_speed
    j = 0
    try:
        i = 0
        while i < like_speed:
            i += 1
            if sleeparray:
                api.create_favorite(sleeparray[0])
                j += 1
        if j > 0:
            dm_msg = "liked " + str(j) + " tweets total and have " + str(len(sleeparray)) + "tweets left"
            rosealert(dm_msg)
    except Exception as e:
        dm_msg = str(e)
        rosealert("sleep error " + dm_msg)

# STORE ALL BIRTHDAYS #
def birthday(ids):
    global bd_list
    # just one
    if type(ids) is str:
        try:
            bd = str(TwitterAccount.from_username(ids).birthday)
            if bd != "None":

                month = bd[5:7]
                day = bd[8:10]

                bd_info = []
                bd_info.append(month)
                bd_info.append(day)
                bd_info.append(ids)

                bd_list.append(bd_info)
        except:
            pass
    # for array
    else:
        for id in ids:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                temp_sn = str(api3.get_user(id).screen_name)
                bd = str(TwitterAccount.from_username(temp_sn).birthday)
                if bd != "None":

                    month = bd[5:7]
                    day = bd[8:10]

                    bd_info = []
                    bd_info.append(month)
                    bd_info.append(day)
                    bd_info.append(temp_sn)

                    bd_list.append(bd_info)
            except:
                pass

# CHECK IF TODAY IS BIRTHDAY AND DM IF IT IS #
def check_birthday(month, day):
    # array of month day name
    global bd_list
    for item in bd_list:
        if item[0] == month:
            if item[1] == day:
                dm_msg = "itz " + str(item[2]) + " borthDay UwU;;"
                rosealert(dm_msg)
    return

def doodler():
    # open people not drawn
    with open("retweeters.txt") as f:
        notdone = f.readlines()
    f.close()

    # open people drawn
    with open("donert.txt") as d:
        done = d.readlines()
    d.close()

    # check new retweeters and add to notdone list if there's new person
    ix = 0
    x = ra.retweets(1209580550278668288, 1000)
    for i in x:
        y = i.author.screen_name + "\n"
        z = i.author.screen_name + "\r\n"
        if y not in notdone:
            if z not in done:
                f = open("retweeters.txt", "a+")
                f.write(y)
                f.close()
                ix += 1
    # open all names into array
    with open("retweeters.txt") as f:
        results = f.readlines()

    # clean to rewrite later
    f = open("retweeters.txt", "w+")
    f.close()

    i = 5
    final = []
    for person in results:
        if i > 0:
            # gather 5 @'s to send later
            final.append("@" + person[:-1])
            d = open("donert.txt", "a+")
            d.write(person)
            d.close()
            i -= 1
        else:
            # store others to use later
            f = open("retweeters.txt", "a+")
            f.write(person)
            f.close()

    # sent the @'s to bot
    send = " ".join(final)
    return(send)

def dailyprint():
    global daily_report
    import datetime
    today_day = datetime.today().weekday()
    doodle_ppl = ""

    # decide doodle_ppl
    if today_day == 1 or today_day == 3:
        doodle_ppl = doodler()

    # decide love_person
    with open('lovelist.txt', 'r') as f:
        love_list = f.readlines()
    len_ll = len(love_list)
    if len_ll > 0:
        try:
            love_person = love_list[random.randint(0,len_ll)]
        except:
            love_person = love_list[random.randint(0,len_ll-1)]
    else:
        love_person = "yourself"

    # monday 0
    if today_day == 0 or today_day == 2 or today_day == 4:
        dm_msg = "love " + love_person + "\n" + daily_report[0] + "\n\n" + str(len(sleeparray)) + " tweets while sleep\n\n" + "GYM TODAY"
        rosealerts(dm_msg)

    # tuesday thursday 1 3
    if today_day == 1 or today_day == 3:
        dm_msg = "love " + love_person + "\n" + daily_report[0] + "\n\n" + str(len(sleeparray)) + " tweets while sleep\n\n" + "DRAW " + str(doodle_ppl)
        rosealerts(dm_msg)

    # saturday 5
    if today_day == 5:
        global unfollowed_you
        if len(unfollowed_you) > 0:
            dm_msg = "love " + love_person + "\n" + str(len(sleeparray)) + " tweets while sleep\n" + unfollowed_you
        else:
            dm_msg = "love " + love_person + "\n" + str(len(sleeparray)) + " tweets while sleep\n\n" + "nobody unfollowed you gj"
        if len(dm_msg) > 270:
            if len(dm_msg) < 540:
                chunks, chunk_size = len(dm_msg), len(dm_msg)/2
                dm_msgs = [dm_msg[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
                rosealerts(dm_msgs[0])
                rosealerts(dm_msgs[1])
            else:
                chunks, chunk_size = len(dm_msg), len(dm_msg)/3
                dm_msgs = [dm_msg[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
                rosealerts(dm_msgs[0])
                rosealerts(dm_msgs[1])
                rosealerts(dm_msgs[3])
        else:
            rosealerts(dm_msg)

    # sunday 6
    if today_day == 6:
        global fol_num
        new_fol_num = api.get_user(me).followers_count
        dm_msg = "love " + love_person + "\n" + str(len(sleeparray)) + " tweets while sleep\n\n" + "CLEAN HOUSE and VID FOR PARENTS\n\n" + "followers gained: " + str(new_fol_num - fol_num)
        rosealerts(dm_msg)
        fol_num = new_fol_num


################################################################################

# ANALYSIS STUFF

def get_day(day):
    if day == 0:
        return "Mon"
    if day == 1:
        return "Tue"
    if day == 2:
        return "Wed"
    if day == 3:
        return "Thurs"
    if day == 4:
        return "Fri"
    if day == 5:
        return "Sat"
    if day == 6:
        return "Sun"

def get_analysis():
    person = "rohhse"
    f = open(str(person) + ".txt", "w").close()
    i = 0
    # format #OFLIKES HOUR DAY
    while i < 200:
        timeline = api3.user_timeline(person, page = i)
        for tweet in timeline:
            try:
                a = tweet.text[0]
                b = tweet.text[1]
                # not a retweet
                if a != "R" and b != "T":
                    # not a reply to someone else
                    if a != "@":
                        created_at = tweet.created_at
                        likes = tweet.favorite_count
                        hour = str(created_at).split(":")[0]
                        hour = hour.split(" ")[1]
                        day = created_at.weekday()
                        f = open(str(person) + ".txt", "a+")
                        f.write(str(likes) + " " + str(hour) + " " + str(get_day(day)) + "\n")
                        f.close()
            except:
                pass
        i += 1

    file = "rohhse"
    results = []
    with open(file + ".txt") as f:
        results = f.readlines()

    day_dict = {
        "Mon":0,
        "Tue":0,
        "Wed":0,
        "Thurs":0,
        "Fri":0,
        "Sat":0,
        "Sun":0
    }
    day_counter = {
        "Mon":0,
        "Tue":0,
        "Wed":0,
        "Thurs":0,
        "Fri":0,
        "Sat":0,
        "Sun":0
    }
    hour_dict = {
        "00":0,
        "01":0,
        "02":0,
        "03":0,
        "04":0,
        "05":0,
        "06":0,
        "07":0,
        "08":0,
        "09":0,
        "10":0,
        "11":0,
        "12":0,
        "13":0,
        "14":0,
        "15":0,
        "16":0,
        "17":0,
        "18":0,
        "19":0,
        "20":0,
        "21":0,
        "22":0,
        "23":0
    }
    hour_counter = {
        "00":0,
        "01":0,
        "02":0,
        "03":0,
        "04":0,
        "05":0,
        "06":0,
        "07":0,
        "08":0,
        "09":0,
        "10":0,
        "11":0,
        "12":0,
        "13":0,
        "14":0,
        "15":0,
        "16":0,
        "17":0,
        "18":0,
        "19":0,
        "20":0,
        "21":0,
        "22":0,
        "23":0
    }

    for item in results:
        item = item.split(" ")
        likes = int(item[0])
        hour = item[1]
        day = item[2].strip()

        if hour in hour_dict:
            hour_dict[hour] += likes
            hour_counter[hour] += 1
        else:
            hour_dict[hour] = likes
            hour_counter[hour] = 1
        if day in day_dict:
            day_dict[day] += likes
            day_counter[day] += 1
        else:
            day_dict[day] = likes
            day_counter[day] = 1

    new_day_dict = {}
    new_hour_dict = {}

    for item in day_dict:
        if int(day_counter[item]) == 0:
            continue
        new_name = str(item) + " (analyzed " + str(day_counter[item]) + " tweets)"
        new_day_dict[new_name] = int(int(day_dict[item]) / int(day_counter[item]))

    for item in hour_dict:
        if int(hour_counter[item]) == 0:
            continue
        if int(item) > 12:
            new_hour_format = str(int(int(item) - 12)) + "pm"
        else:
            new_hour_format = str(item) + "am"
        new_name = str(new_hour_format) + " (analyzed " + str(hour_counter[item]) + " tweets)"
        new_hour_dict[new_name] = int(int(hour_dict[item]) / int(hour_counter[item]))

    dm_msg = "\npopular day: " + str(max(new_day_dict, key=new_day_dict.get)) + "\npopular hour: " + str(max(new_hour_dict, key=new_hour_dict.get))
    global daily_report
    daily_report.append(dm_msg)

################################################################################

### FIRST ITERATION ###

ids = api.friends_ids(me) # id of everyone im following
myinfo = api.get_user(me) # my info
fol_num = myinfo.followers_count
myratio = fol_num / myinfo.friends_count # my follower ratio
frilis = ids # copied so we can fuck idk

en = ""

birthday(ids)

#######################

while 1:
    try:
        en = "decide day"
        hour = int(datetime.now().hour)
        month = datetime.now().month
        day = datetime.now().day

        en = "append all tweets"
        all_tweets.append(hour)

        en = "check if sleep time"
        if hour != 23:
            if hour_check == 1:
                rosealert("hope you are ok <3\n")
            hour_check = 0 # reset for new day

        # start of day
        if (hour_check == 0 and hour == 23):

            # dailys ###########################################################
            en = "get analysis"
            # analyze this week
            get_analysis()
            en = "dict stuff"
            # print top tweeters (1)
            dict_stuff()
            en = "check birthday"
            # check if birthday today
            check_birthday(month, day)

            # reset dictionary
            today = {}
            en = "reset values"
            # reset values
            ids = api.friends_ids(me) # id of everyone im following
            myinfo = api.get_user(me) # my info
            myratio = myinfo.followers_count / myinfo.friends_count # my follower ratio
            frilis = ids # copied so we can fuck idk
            en = "check unfollow"
            # do actions
            check_unfollow()
            en = "storing sleep tweets"
            # before 8, just keep storing tweets only
            while int(datetime.now().hour) != 8:
                sleep_tweets()
                sleepfor(wait)
            en = "decide like speed"
            # calculate how fast to like sleep_tweets
            like_speed = int(len(sleeparray) / 10)
            if like_speed == 0:
                like_speed = 1
            en = "daily print error"
            dailyprint()

            daily_report = [] # report reset

            hour_check = 1 # mark as done

            ####################################################################

        # regular iteration ####################################################
        en = "check new tweet"
        # new rohhse tweet check
        check_newtweet()
        en = "new follower check"
        # deal with new followers
        last_flwr = newfollower(last_flwr)
        en = "like tweets"
        # like and add users to dict
        count = like()
        en = "store liked tweets"
        like_stored_tweets()
        en = "calculate wait"
        wait = calc_wait(wait, count)
        en = "sleep time"
        # sleep to not clog api
        sleepfor(wait)

        ########################################################################

    except Exception as e:
        exceptionlist.append("from " + str(en) + ": " + str(e))
        sleepfor(wait)

################################################################################
