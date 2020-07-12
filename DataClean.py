#!/usr/bin/env python
# coding: utf-8

# 
# # Data Cleanning

# In[1]:


import numpy as np
import pandas as pd
import sklearn


# In[2]:


data = pd.read_csv("LeagueofLegends.csv")
data.shape


# In[3]:


data.head()


# ## Feature Engineering: Strings

# ### Missing / Wrong String handling
# Since R will automaticly one-hot encoding string, here we just need to check the quality of those strings.

# #### League, Year, Season, Type

# In[4]:


print("All unique League:")
print(data.groupby("League")["Address"].nunique())
print()
print("All unique Year:")
print(data.groupby("Year")["Address"].nunique())
print()
print("All unique Season:")
print(data.groupby("Season")["Address"].nunique())
print()
print("All unique Type:")
print(data.groupby("Type")["Address"].nunique())


# We can see the quality of those data are proper. Do not need to be clean

# #### Team

# In[5]:


print("All blue unique Team:")
print(data.groupby("blueTeamTag")["Address"].nunique().to_string())
data.groupby("blueTeamTag")["Address"].nunique().count()


# In[6]:


print("All red unique Team:")
print(data.groupby("redTeamTag")["Address"].nunique().to_string())
data.groupby("redTeamTag")["Address"].nunique().count()


# We can see the data are really messy, we can try the following:

# In[7]:


data["blueTeamTag"] = data["blueTeamTag"].apply(str).apply(str.upper)
print("Current Unique Blue Teams: ", data.groupby("blueTeamTag")["Address"].nunique().count())
data["redTeamTag"] = data["redTeamTag"].apply(str).apply(str.upper)
print("Current Unique Red Teams: ", data.groupby("redTeamTag")["Address"].nunique().count())


# In[8]:


data["blueTeamTag"][~data["blueTeamTag"].isin(data["redTeamTag"])]


# In[9]:


data["redTeamTag"][~data["redTeamTag"].isin(data["blueTeamTag"])]


# Since those teams did exist, they will be kept.

# Even though there are still some other problems for those data (e.g. C9C change their name to C9), we do not check here.

# In[10]:


# f0 = lambda x: x[1:-1].split(", ")[0]
# f1 = lambda x: x[1:-1].split(", ")[1]
# f2 = lambda x: x[1:-1].split(", ")[2]
# data["blueBans0"] = data["blueBans"].apply(f0)
# data["blueBans1"] = data["blueBans"].apply(f1)
# data["blueBans2"] = data["blueBans"].apply(f2)
# data["redBans0"] = data["redBans"].apply(f0)
# data["redBans1"] = data["redBans"].apply(f1)
# data["redBans2"] = data["redBans"].apply(f2)


# Since those names seem to be valid, we do not modify them.

# ## Feature Engineering: Arrays:

# ### Golds:
# We decide to engineer all golds by following methods:
# 1. Calculate the golds for all two teams for all five positions for 10min, 20min, and 30 min.
# 2. If the games ends before 30min, we will set the gold to be the amount at the end of gold.

# In[11]:


gold_columns = ["goldblueTop","goldredTop",                "goldblueJungle","goldredJungle",                "goldblueMiddle","goldredMiddle",                "goldblueADC","goldredADC",                "goldblueSupport","goldredSupport",]



def counting_gold(columns, data = data, periods = [10, 20, 30]):
    def modify(s, sep = ", "):
        s = s[1:-1]
        result = []
        l = s.split(sep)
        for p in periods:
            if (p < len(l)):
                result.append(l[p])
            else:
                result.append(l[-1])
        return ",".join(result)
    def modify2(s):
        s = s.apply(modify)
        return s
    rdf = pd.DataFrame()
    df = data[columns]
    df = df.apply(modify2)
    f0 = lambda s: s.split(",")[0]
    f1 = lambda s: s.split(",")[1]
    f2 = lambda s: s.split(",")[2]
    for c in df.columns:
        rdf[c+"10"] = df[c].apply(f0).apply(int)
        rdf[c+"20"] = df[c].apply(f1).apply(int)
        rdf[c+"30"] = df[c].apply(f2).apply(int)
    return rdf
           
counting_gold(gold_columns).to_excel("tmpgold.xlsx", index = False)


# ### Counting Legendary Monsters: Dragon
# We decide to engineer dragon by following methods:
# 1. Count the first dragon slained for both sides, and the total number of dragons for both sides.
# 2. If one side does not slained any dragon, record the time as the end of game.
# 3. There are elements dragon in 2017 and 2018, we ingnore them here for now.

# In[12]:


dragon_columns = ["bDragons","rDragons"]

def counting_dragon(columns, data = data, end_column = "gamelength"):
    def modify(s, sep = ", "):
        s = s[1:-1]
        l = s.split(sep)
        if l[0] != '':
            return str(l[0][1:].split(", ")[0]) + ":" + str(len(l)/2)
        else:
            return "100:0"
    def modify2(s):
        s = s.apply(modify)
        return s
    rdf = pd.DataFrame()
    df = data[columns]
    df = df.apply(modify2)
    f0 = lambda s: s.split(":")[0]
    f1 = lambda s: s.split(":")[1]
    for c in df.columns:
        rdf[c[0] + "FirstDragon"] = df[c].apply(f0).apply(float)
        rdf[c[0] + "FirstDragon"] = rdf[c[0] + "FirstDragon"].combine(data[end_column], min)
        rdf[c[0] + "NumofDragon"] = df[c].apply(f1).apply(float)
    return rdf
           
counting_dragon(dragon_columns).to_excel("tmpdragon.xlsx", index = False)


# ### Counting Legendary Monsters: Baron
# We decide to engineer baron by following methods:
# 1. Count the first baron slained for both sides.

# In[13]:


baron_columns = ["bBarons","rBarons"]

def counting_baron(columns, data = data):
    def modify(s, sep = ", "):
        s = s[1:-1]
        l = s.split(sep)
        if l[0] != '':
            return len(l)
        else:
            return "0"
    def modify2(s):
        s = s.apply(modify)
        return s
    rdf = pd.DataFrame()
    df = data[columns]
    df = df.apply(modify2)
    for c in df.columns:
        rdf[c[0] + "NumofBaron"] = df[c].apply(float)
    return rdf
           
counting_baron(baron_columns).to_excel("tmpBaron.xlsx", index = False)


# ### Counting Legendary Monsters: Herald
# We decide to engineer herald by following methods:
# 1. Count the number of heralds slained for both sides.

# In[14]:


herald_columns = ["bHeralds","rHeralds"]

def counting_herald(columns, data = data):
    def modify(s, sep = ", "):
        s = s[1:-1]
        l = s.split(sep)
        if l[0] != '':
            return len(l)
        else:
            return "0"
    def modify2(s):
        s = s.apply(modify)
        return s
    rdf = pd.DataFrame()
    df = data[columns]
    df = df.apply(modify2)
    for c in df.columns:
        rdf[c[0] + "NumofHerald"] = df[c].apply(float)
    return rdf
           
counting_herald(herald_columns).to_excel("tmpHerald.xlsx", index = False)


# ### Counting Towers: Tower
# We decide to engineer tower by following methods:
# 1. Count the first tower destroyed for both sides, and the total number of towers for both sides.
# 2. If one side does not destroy any tower, record the time as the end of game.

# In[15]:


tower_columns = ["bTowers","rTowers"]

def counting_tower(columns, data = data, end_column = "gamelength"):
    def modify(s, sep = ", "):
        s = s[1:-1]
        l = s.split(sep)
        if l[0] != '':
            return str(l[0][1:].split(", ")[0]) + ":" + str(len(l)/3)
        else:
            return "100:0"
    def modify2(s):
        s = s.apply(modify)
        return s
    rdf = pd.DataFrame()
    df = data[columns]
    df = df.apply(modify2)
    f0 = lambda s: s.split(":")[0]
    f1 = lambda s: s.split(":")[1]
    for c in df.columns:
        rdf[c[0] + "FirstTower"] = df[c].apply(f0).apply(float)
        rdf[c[0] + "FirstTower"] = rdf[c[0] + "FirstTower"].combine(data[end_column], min)
        rdf[c[0] + "NumofTower"] = df[c].apply(f1).apply(float)
    return rdf
           
counting_tower(tower_columns).to_excel("tmptower.xlsx", index = False)


# ### Counting Towers: Inhibitors
# We decide to engineer inhibitor by following methods:
# 1. Count the first inhibitor destroyed for both sides, and the total number of inhibitors for both sides.
# 2. If one side does not destroy any inhibitor, record the time as the end of game.

# In[16]:


inhib_columns = ["bInhibs","rInhibs"]

def counting_inhib(columns, data = data, end_column = "gamelength"):
    def modify(s, sep = ", "):
        s = s[1:-1]
        l = s.split(sep)
        if l[0] != '':
            return str(l[0][1:].split(", ")[0]) + ":" + str(len(l)/2)
        else:
            return "100:0"
    def modify2(s):
        s = s.apply(modify)
        return s
    rdf = pd.DataFrame()
    df = data[columns]
    df = df.apply(modify2)
    f0 = lambda s: s.split(":")[0]
    f1 = lambda s: s.split(":")[1]
    for c in df.columns:
        rdf[c[0] + "FirstInhib"] = df[c].apply(f0).apply(float)
        rdf[c[0] + "FirstInhib"] = rdf[c[0] + "FirstInhib"].combine(data[end_column], min)
        rdf[c[0] + "NumofInhib"] = df[c].apply(f1).apply(float)
    return rdf
           
counting_inhib(inhib_columns).to_excel("tmpinhib.xlsx", index = False)


# ### Counting Kills
# We decide to engineer kills by following methods:
# 1. Count the first kill for both sides, and the total number of kills for both sides.
# 2. If one side does not kill, record the time as the end of game.

# In[17]:


kill_columns = ["bKills","rKills"]

def counting_kill(columns, data = data, end_column = "gamelength"):
    def modify(s, sep = "["):
        s = s[2:-1]
        l = s.split(sep)
        if l[0] != '':
            return str(l[0].split(", ")[0]) + ":" + str(len(l)/2)
        else:
            return "100:0"
    def modify2(s):
        s = s.apply(modify)
        return s
    rdf = pd.DataFrame()
    df = data[columns]
    df = df.apply(modify2)
    f0 = lambda s: s.split(":")[0]
    f1 = lambda s: s.split(":")[1]
    for c in df.columns:
        rdf[c[0] + "FirstKill"] = df[c].apply(f0).apply(float)
        rdf[c[0] + "FirstKill"] = rdf[c[0] + "FirstKill"].combine(data[end_column], min)
        rdf[c[0] + "NumofKill"] = df[c].apply(f1).apply(float)
    return rdf
           
counting_kill(kill_columns).to_excel("tmpkill.xlsx", index = False)


# ## Columns Dropping:
# We will drop Address, Bans, and players for now.

# ## Final Step: merge data:

# In[18]:


target = data[["bResult","League","Year","Season","Type",              "blueTeamTag","redTeamTag","gamelength",              "blueTopChamp","blueJungleChamp","blueMiddleChamp","blueADCChamp","blueSupportChamp",              "redTopChamp","redJungleChamp","redMiddleChamp","redADCChamp","redSupportChamp"]]
target.columns = ["bResult","League","Year","Season","Type",              "blueTeamTag","redTeamTag","gamelength",              "blueTopChamp","blueJungleChamp","blueMiddleChamp","blueADCChamp","blueSupportChamp",              "redTopChamp","redJungleChamp","redMiddleChamp","redADCChamp","redSupportChamp"]
df1 = pd.read_excel("tmpgold.xlsx")
df2 = pd.read_excel("tmpdragon.xlsx")
df3 = pd.read_excel("tmpBaron.xlsx")
df4 = pd.read_excel("tmpHerald.xlsx")
df5 = pd.read_excel("tmptower.xlsx")
df6 = pd.read_excel("tmpinhib.xlsx")
df7 = pd.read_excel("tmpkill.xlsx")


# In[21]:


target = pd.concat([target, df1, df2, df3, df4, df5, df6, df7], axis= 1, ignore_index=False, sort = False)
#target
target.to_csv("LOL.csv", sep = ",", index = False)


# In[ ]:




