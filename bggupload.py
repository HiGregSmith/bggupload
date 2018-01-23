# BGG Collection Program
# This program allows you to enter board games into a CSV file for upload into your collection
# using the bggcli program.
#
# Input to this program is in the form of
# 1) Name search,
# 2) CSV file,
# 3) Miniature Market email, or
# 4) CoolStuffInc email

# If no BGG ID is present, then the objectname is used as a search term. Other information in the input file
# is retained.

# Search
# The BGG XMLAPI2 is used to actively search for names, first for exact match,
# Then for partial match if there are no exact matches.
# In either case, a local database is used for a fuzzy search of possible BGGIDs.
# The primary thumbnails for the BGGIDs associated with the found names are
# downloaded and displayed for the user to select from.
# A single row is written to the output CSV file corresponding to the selection,
# and the row is removed from the UI.


# HISTORY
# January 2018 #######################################################
    # get zip file from module file location instead of directory where program is started
    # added column matching dialog
    # capture all CSV data and carry through to output.
    # When importing, queue items for background processing.
    # Added status bar thread, but not yet extensively used, the output debugging window is still the primary status.
#


# preferences
# 'HOME'   : os.path.expanduser('~'),
# USERSAVEPATH : os.path.join(HOME, 'bggupload'),

    # if not os.path.exists(USERSAVEPATH):
        # os.makedirs(USERSAVEPATH)
        # output('created ~/bggupload')

from __future__ import print_function
# This must be the first statement before other statements.
# You may only put a quoted or triple quoted string, 
# Python comments, other future statements, or blank lines before the __future__ line.

import os
import codecs
import bggupload_gui
import json
import wx
import xml.etree.ElementTree as ET
try:
    import urllib.parse as urlparse
except:
    import urlparse # The urlparse module is renamed to urllib.parse in Python 3.
import sys
import requests
import csv
import time
# retrieve xml results from query
# import requests
# from html.parser import HTMLParser
import lxml.html
#pip install python-dateutil
import dateutil
import re
from xlrd import open_workbook

# use a ListCtrl in report mode with a 
# single column and with the header turned off.  It looks and acts almost like a ListBox in that case. 


modulefile = sys.modules[__name__].__file__
modulefolder = os.path.dirname(modulefile)
print(modulefolder)

app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.

class wxoutput():    
    def __init__(self,pobject,method,*args,**kwargs):
        self._object = pobject
        self._method = method
        
    def output(self,*args,**kwargs):
        #end = kwargs.get('end','\n')
        #ostring = ' '.join(args)+end
        ostring = ' '.join(map(lambda s: str(s),args[0]))+kwargs.get('end','\n')
        #aplugin.g.outputbox.AppendText(ostring)
        getattr(self._object,self._method)(ostring)
        return
        # # Here's the simple 'print' definition of output
        # for arg in args:
            # print(arg,)
        # print
# helpdialog
# helptextbox
try:
    import __builtin__
except ImportError:
    # Python 3
    import builtins as __builtin__

def print(*args, **kwargs):
    """My custom print() function."""
    # Adding new arguments to the print function signature 
    # is probably a bad idea.
    # Instead consider testing if custom argument keywords
    # are present in kwargs
    return woutput.output(args,kwargs)
    #__builtin__.print('My overridden print() function!')
    return __builtin__.print(*args, **kwargs)

    
hd = bggupload_gui.helpdialog(None)        
woutput = wxoutput(hd.helptextbox,'AppendText')
hd.SetTitle("BGGUP Debugging Output")
hd.Show(True)
print('Don\'t close this window!\n\nThis is the program debugging output. Closing this window results in unknown behavior.')


#######################################################
#############   Threading Begin    ####################
#######################################################

import threading
from time import sleep
import queue
#import fuzzywuzzy as fuzz
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
#from collections import *
import collections
from os import walk
global SearchStop
SearchStop=False
SearchQueue = queue.Queue()
SearchList = []
SearchThread = None


#######################################################
#############   Status Threading Begin    #############
#######################################################
StatusQueue = queue.Queue()
StatusThread = None
def StatusThreadStart():
    global StatusThread
    if StatusThread is None:
        StatusThread = threading.Thread(target=StatusThreadFunction, name="StatusThread", args=(), kwargs={}, daemon=False)#, *, daemon=None)
        StatusThread.start()

def StatusThreadFunction():
    while True:
        currentStatus = StatusQueue.get()
        wx.CallAfter(UpdateStatus,currentStatus)
        
def UpdateStatus(statusstring):
    try:
        mframe.status.SetStatusText(statusstring)
    except:
        pass
StatusQueue.put('Enter Search Term, Load a file, or click Help for more assistance!')
#######################################################
#############   Status Threading End      #############
#######################################################


preferences = {'fuzzymincount':2,'fuzzymaxcount':20,'fuzzyminscore':80}
BggSummaryInfo = collections.namedtuple('BggSummaryInfo','category itemid itemtype itemname itemnametype itemyear')

#print('-{0:>6}-'.format(345))
things = [ # lowest priority first
    'rpgissue',
    'rpgitem',
    'videogame',
    'boardgameaccessory',
    'boardgame',
    'boardgameexpansion',
    ]
families = ['rpg','rpgperiodical','boardgamefamily']
def heading(value):
    return value.upper().center(len(value)+8).center(70,'#')


import gzip
import json

        # for i in range(N):
            # uid = "whatever%i" % i
            # dv = [1, 2, 3]

            # data = {
                # 'what': uid,
                # 'where': dv
            # }                                            # 1. data

def jsonzipdump(filename,data):
    with gzip.GzipFile(filename, 'w') as fout:
        json_str = json.dumps(data) + "\n"           # 2. string
        json_bytes = json_str.encode('utf-8')        # 3. bytes (i.e. UTF-8)
        fout.write(json_bytes)                       # 4. gzip
        
def jsonzipload(filename):
    with gzip.GzipFile(filename, 'r') as fin:        # 4. gzip
        json_bytes = fin.read()                          # 3. bytes (i.e. UTF-8)
        json_str = json_bytes.decode('utf-8')            # 2. string
        data = json.loads(json_str)                      # 1. data
        #print(data)
        data = map(lambda x: BggSummaryInfo(*x),data)
        return data

# objecttype is category ('thing' or 'family')
# itemtype is 'standalone' or 'expansion'
csv_output_headings = [
    'objectname', 'objectid', 'rating', 'numplays', 'weight',
    'own', 'fortrade', 'want', 'wanttobuy', 'wanttoplay',
    'prevowned', 'preordered', 'wishlist', 'wishlistpriority',
    'wishlistcomment', 'comment', 'conditiontext', 'haspartslist',
    'wantpartslist', 'collid', 'baverage', 'average', 'avgweight',
    'rank', 'numowned', 'objecttype', 'originalname', 'minplayers',
    'maxplayers', 'playingtime', 'maxplaytime', 'minplaytime',
    'yearpublished', 'bggrecplayers', 'bggbestplayers',
    'bggrecagerange', 'bgglanguagedependence', 'publisherid',
    'imageid', 'year', 'language', 'other', 'itemtype', 'pricepaid',
    'pp_currency', 'currvalue', 'cv_currency', 'acquisitiondate',
    'acquiredfrom', 'quantity', 'privatecomment',
    'version_publishers', 'version_languages',
    'version_yearpublished', 'version_nickname'
    ]
#objectname	objectid	rating	numplays	weight	own	fortrade	want	wanttobuy	wanttoplay	prevowned	preordered	wishlist	wishlistpriority	wishlistcomment	comment	conditiontext	haspartslist	wantpartslist	collid	baverage	average	avgweight	rank	numowned	objecttype	originalname	minplayers	maxplayers	playingtime	maxplaytime	minplaytime	yearpublished	bggrecplayers	bggbestplayers	bggrecagerange	bgglanguagedependence	publisherid	imageid	year	language	other	itemtype	pricepaid	pp_currency	currvalue	cv_currency	acquisitiondate	acquiredfrom	quantity	privatecomment	version_publishers	version_languages	version_yearpublished	version_nickname

class OutputManager():
    
    def __init__(self,filebase='BggUploadSaveFile'):
        # very inefficient, but should work
        count = 0
        while True:
            self.backupfile = '{}{:03d}{}'.format(filebase,count,'.csv')
            if not os.path.isfile(self.backupfile):
                break
            count += 1
            
        self.fullpath = os.path.abspath(self.backupfile)
        with codecs.open(self.backupfile,'w', encoding='utf-8') as csvfile:
        #with open(self.backupfile,'w') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=csv_output_headings)
            writer.writeheader()
        print('New Output File: ',self.backupfile)
            
    def saverows(self,rows):
        with codecs.open(self.backupfile,'a', encoding='utf-8') as csvfile:
        #with open(self.backupfile,'a') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=csv_output_headings)
            for row in rows:
                try:
                    del(row['searchterm'])
                except:
                    pass
                writer.writerow(row)
                print('OUTPUT: ({})\n{}'.format(outputmgr.backupfile,row))
outputmgr = OutputManager()

cat = {
    'boardgame':'thing',
    'rpgitem':'thing',
    'videogame':'thing',
    'rpgissue':'thing',
    'rpg':'family',
    'rpgperiodical':'family',
    'boardgameexpansion':'thing',
    'thing':'thing',
    'family':'family',
    }
class ReadBGGResults():
    sortorder = {
        'rpg'                :1,
        'rpgperiodical'      :2,
        'boardgamefamily'    :3,
        'rpgissue'           :4,
        'rpgitem'            :5,
        'videogame'          :6,
        'boardgameaccessory' :7,
        'boardgame'          :8,
        'boardgameexpansion' :9,
        'family'            :10,
        'thing'             :11,
    }
    def __init__(self):
        self.idlist = collections.defaultdict(set)
        self.idbyname = collections.defaultdict(set)
        self.fullbgg = collections.defaultdict(set)
        self.typebyid = collections.defaultdict(list)
        self.fullbgg2 = {}
        self.fullbgg3 = {'thing':{},'family':{}}
        self.allset = set()
    # <item type="videogame" id="89336">
    # <name type="primary" value="Your Shape Fitness Evolved"/>			
            # </item>
    # <item type="videogame" id="110313">
    # <name type="primary" value="Your Shape Fitness Evolved 2012"/>			
    # </item>
    # fullbgg[type][id][nametype] = name
    # tag, attribute, for child in xxx
            
    def getall(self):
        files = []
        #idlist = collections.defaultdict(set)
        whole = collections.defaultdict(set)
        inametypes = set()
        itypes = set()

        for (dirpath, dirnames, filenames) in walk('fullbgg'):
            files.extend(map(lambda x: os.path.join(dirpath,x),filenames))
            break
        for file in files:
            tree = ET.parse(file)
            root = tree.getroot()
            for item in root:
                itemid = item.attrib['id']
                itemtype = item.attrib['type']
                itypes.add(itemtype)
                itemname = ''
                itemnametype = ''
                itemyear = ''
                for child in item:
                    if child.tag == 'name':
                        itemname = child.attrib['value']
                        itemnametype = child.attrib['type']
                        inametypes.add(itemnametype)
                    if child.tag == 'yearpublished':
                        itemyear = child.attrib['value']
                whole[itemname].add(itemid)
                self.allset.add(BggSummaryInfo(self.cat[itemtype], itemid, itemtype, itemname, itemnametype, itemyear))
        s=list(self.allset)
        s.sort(key=lambda x:self.sortorder[x[2]])
        jsonzipdump('data_json.zip',s)
                # # from id, need itemtype
                # self.fullbgg. \
                    # setdefault(itemtype    ,{}). \
                    # setdefault(itemid      ,{}). \
                    # setdefault(itemnametype,[]). \
                    # append((itemname,itemyear))
                # self.idlist[itemtype].add(itemid)
                # self.typebyid[itemid].append(itemtype)
                # if itemtype.startswith('boardgame'):
                    # self.idbyname[itemname].add(itemid)
                # if itemid not in self.fullbgg2:
                    # self.fullbgg2.setdefault(itemtype,{})[itemid] = (set(),set(),set(),set())
                # self.fullbgg2[itemtype][itemid][0].add(itemtype)
                # self.fullbgg2[itemtype][itemid][1].add(itemyear)
                # if itemnametype.startswith('pri'):
                    # self.fullbgg2[itemtype][itemid][2].add(itemname)
                # else:
                    # self.fullbgg2[itemtype][itemid][3].add(itemname)
        # print('Collating...')
        # for typecategory, typelist in (('thing',things),('family',families)):
            # for itemtype in typelist:
                # for bggid in self.fullbgg.get(itemtype,{}).keys():
                    # pvalues = self.fullbgg[itemtype][bggid].get('primary',(('',''),))
                    # avalues = self.fullbgg[itemtype][bggid].get('alternate',(('',''),))
                    # pvalues = tuple(set(pvalues))
                    # #print(avalues)
                    # avalues = tuple(set(avalues))
                    # pname = ''
                    # year = ''
                    # if len(pvalues)>1:
                        # print('warn p > 1 (={})'.format(len(pvalues)))
                        # print(pvalues)
                    # try:
                        # pnames = list(set([x[0] for x in pvalues]))
                        # yearset = set([x[1] for x in pvalues])
                        # pname = pvalues[0][0]
                        # year  = pvalues[0][1]
                    # except:
                        # pass
                    # anames = list(set([x[0] for x in avalues]))
                    # yearset = yearset.union(set([x[1] for x in pvalues]))
                    # if len(yearset) != 1:
                        # print('!=1: ',yearset)
                    # #print(typecategory,bggid,year,itemtype,pname,anames)
                    # self.fullbgg3[typecategory][bggid] = (year,itemtype,pnames,anames)
        # print('Done.')
        # print('Writing subtype.txt...')
        # with codecs.open('subtype.txt','w', encoding='utf-8') as f:
            # for itemcategory,iddict in self.fullbgg3.items():
                # for itemid,values in iddict.items():
                    # year,itemtype,pnames,anames = values
                    # f.write('{},{},{},{}\n{}\n{}\n'.format(itemcategory,itemid,year,itemtype,u'\u0000'.join(pnames),'\u0000'.join(anames)))
        #s.sort(key=lambda x:int(x[0]))
        
        # with codecs.open('list.txt','w', encoding='utf-8') as f:
            # for line in s:
                # f.write(str(line))
                # f.write('\n')
        # self.byid = {'thing':{},'family':{}}
 
        # for line in s:
            # #(itemid, itemtype, itemname, itemnametype, itemyear)
            # (category, itemid, itemtype, itemname, itemnametype, itemyear) = line
            # self.byid[category].setdefault(itemid,[]).append(line)
        # with codecs.open('list.txt','w', encoding='utf-8') as f:
            # for cat,idlist in self.byid.items():
                # f.write(heading(cat))
                # f.write('\n')
                # for id,lines in idlist.items():
                    # for line in lines:
                        # f.write(str(line))
                        # f.write('\n')
                # # Writing JSON data
        # # with codecs.open('data_json.txt','w', encoding='utf-8') as f:
             # # json.dump(s, f)
        # # for item, lines in self.fullbgg4.items():
        
        # print('Writing catid.txt...')
        # with codecs.open('catid.txt','w', encoding='utf-8') as f:
            # for catid, lines in self.fullbgg4.items():
                # for line in lines:
                    # f.write(str(line))
                    # f.write('\n')
        # print('Done.')
        # # Reading data back
        # with open('data.json', 'r') as f:
             # data = json.load(f)
            
            
                    # self.fullbgg2[itemid] = ([],[],[],[])
                # self.fullbgg2[itemid][0].append(itemtype)
                # self.fullbgg2[itemid][1].append(itemyear)
                # if itemnametype.startswith('pri'):
                    # self.fullbgg2[itemid][2].append(itemname)
                # else:
                    # self.fullbgg2[itemid][3].append(itemname)
                
                # else
                    # if self.fullbgg2[itemid][0] != itemtype:
                        # print('warning multiple item types for an id')
                    # if self.fullbgg2[itemid][1] != itemyear:
                        # print('warning multiple item years for an id')
                # self.fullbgg2[itemid] = (itemtypes, itemyears, primarynames, altnames)
                # if not fullbgg.haskey(itemtype):
                    # fullbgg[itemtype] = {}
                # if not fullbgg[itemtype].haskey(itemid):
                    # fullbgg[itemtype][itemid] = {}
                # if not fullbgg[itemtype][itemid].haskey(nametype):
                    # fullbgg[itemtype][itemid][nametype] = []
                    
                #fullbgg[itemtype][itemid][nametype].append((itemname,yearlist)) 
                #print (name)
                    #print(child.tag)
                # type = 
                # id =
                # nametype = 
                # name = 
        # count = 0
        # print(len(whole))
        # print(itypes)
        # print(inametypes)
        # # for name,ids in whole.items():
            # # if len(ids) > 1:
                # # print(len(ids),name)
        
        # for name,ids in whole.items():
            # print('{} {}'.format(','.join(ids),name))
            
            
        # for itemtype in fullbgg.keys():
            # print('{} {}'.format(len(fullbgg[itemtype]),itemtype))
            
        # for itemtype, a in fullbgg.items():
            # for itemid, b in a.items():
                # for itemnametype, c in b.items():
                    # for item in c:
                        # print('{} {} {} {}'.format(itemtype,itemid,itemnametype,item))

        # for itemtype, a in fullbgg.items():
            # print('{} {}'.format(len(a),itemtype))
        #print('Item types:',self.fullbgg.keys())

print('Reading Name / BGGID database files.')
# typebyid = {}
#bggr = ReadBGGResults() ; bggr.getall()
# bggnames = set(bggr.idbyname.keys())
# for subtype,values in bggr.fullbgg2.items():
    # for id in values.keys():
        # typebyid.setdefault(id,[]).append(subtype)
        
# ids2 = list(filter(lambda c: len(typebyid[c])==2,typebyid.keys()))
# ids3 = list(filter(lambda c: len(typebyid[c])>2,typebyid.keys()))
# # sys.exit()
# #set(map(lambda c: frozenset(c),typebyid))
# idsbyset = collections.defaultdict(list)
# for k,s in typebyid.items():
    # idsbyset[frozenset(s)].append(k)
        
# for s,i in idsbyset.items():
    # print('#',list(s),'                  #',len(i))
# print()
# for s,i in filter(lambda x: len(x[0]) > 1,idsbyset.items()):
    # print(s,len(i))

s = jsonzipload(os.path.join(modulefolder,'data_json.zip'))
fullbgg4 = {} #collections.defaultdict(list)
#byid = {'thing':{},'family':{}}

for line in s:
    #(category, itemid, itemtype, itemname, itemnametype, itemyear) = line
    #byid[category].setdefault(itemid,[]).append(line)
    #fullbgg4.setdefault((line.category,line.itemid),[]).append(line)
    if line.itemtype in ('thing','family'):#,'boardgameexpansion'):
        continue
    fullbgg4.setdefault((line.itemtype,line.itemid),[]).append(line)

#print('FULLBGG4',set([itemtype for itemtype, itemid in fullbgg4.keys()]))
# # here, check that every boardgameexpansion has a
# # corresponding boardgame with same name and year
# for id, values in bggr.fullbgg2['boardgameexpansion'].items():
    # v1 = values[2:]
    # v2 = bggr.fullbgg2['boardgame'][id][2:]
    # if v1 != v2:
        # print('ex',id,values[1:])
        # print('bg',id,bggr.fullbgg2['boardgame'][id][1:])
        # print()
    
# for t in things:
    # if t in 
        # return t
        
# print('Writing subtype.txt...')
# with codecs.open('subtype.txt','w', encoding='utf-8') as f:
    # for subtypes in subtypesets:
        # f.write('\n\n')
        # f.write(heading(' & '.join(list(subtypes))))
        # f.write('\n\n')
        # for id in idsbyset[frozenset(subtypes)]:
            # #f.write('{} {}\n'.format(id,))
            # for t in subtypes:
                # pl = list(map(lambda x: str(x),bggr.fullbgg2[t][id]))
                # pl.reverse()
                # f.write('{:>6} {}'.format(id,' '.join(pl)))
                # f.write('\n')
            # f.write('\n')
# print('Done.')
# 7221 frozenset({'rpg', 'boardgame'})
# 15188 frozenset({'boardgameexpansion', 'boardgame'})
# 866 frozenset({'boardgame', 'rpgperiodical'})
# 458 frozenset({'rpg', 'boardgameexpansion', 'boardgame'})
# 46 frozenset({'boardgameexpansion', 'boardgame', 'rpgperiodical'})
# 2 frozenset({'boardgameexpansion', 'boardgame', 'rpgitem'})
# 3 frozenset({'boardgame', 'rpgitem'})
# 1 frozenset({'boardgame', 'videogame'})
# 160 frozenset({'rpg', 'rpgitem'})
# 41 frozenset({'rpgperiodical', 'rpgitem'})
# 1 frozenset({'rpgissue', 'rpgperiodical'})
    
#set(map(lambda c: frozenset(typebyid[c]),typebyid.keys()))

def SearchThreadFunction():
    global SearchThread
    print ('Start Search Thread.')
    while not SearchStop and not SearchQueue.empty():
        data = SearchQueue.get()
        searchterm = data.get('searchterm') or data.get('objectname')
        data['objectname']=searchterm
        print ('\tThread:',searchterm,SearchQueue.qsize())
        process_row(data)
        #tree = searchname(searchterm)
        sleep(3)
    SearchThread = None
    print ('End Search Thread.')

def SearchQueueStart():
    global SearchThread
    if SearchThread is None:
        SearchThread = threading.Thread(target=SearchThreadFunction, name="SearchThread", args=(), kwargs={}, daemon=False)#, *, daemon=None)
        SearchThread.start()

#######################################################
#############   Threading End    ######################
#######################################################

#######################################################
#############   Import CoolStuff    ###################
#######################################################
from dateutil.parser import parse
class import_coolstuffemail():
    """Be sure to capture the "Order #CSI-" line so the importer can recognize
       CoolStuffInc email."""
       
    def __init__(self):
        self.date = None
        
    def canimport(self,stream):
        for line in stream:
            if line.startswith('Order #CSI-'):
                return True
        return False
                
    def getrows(self,stream):
        rows = []
        for line in stream:
            #line = stream.readline()
            #sleep(1)
            if line.startswith('Order #CSI-'):
                self.order = line.split()[-1]
            if line.startswith('Date'):
                #self.date = dateutil.parser.parse(line.split()[-1])
                self.date = parse(line.split()[-1])
            if re.match(r'^[0-9]+\s+-\s+.*(.+).*$',line): # line is a row
                print('importing row:',line)
                #print('found row')
                # find last paren expression
                rparen = line.rfind(')')
                lparen = line.rfind('(')
                firstdash = line.find('-')
                numowned = line[:firstdash]
                objectname = line[firstdash:lparen-1]
                print('[{}]'.format(line[rparen+1:]))
                temp,pricepaid,temp = line[rparen+1:].split()
                conditiontext, category, publisher = line[lparen:rparen].split(', ')
                row = {'objectname':objectname[2:],'own':1,'conditiontext':conditiontext[1:],
                       'numowned':numowned, 'pricepaid':pricepaid,
                       'comment':self.order+', '+category+', '+publisher
                       }
                if self.date is not None:
                    row['acquisitiondate'] = self.date
                print(row)
                rows.append(row)
        # 2 - Harbour (New, Board Games, Tasty Minstrel Games) at $7.99 each
        headings = ['objectname','own','conditiontext','numowned',
                    'objecttype','pricepaid','acquisitiondate','comment'] # comment has publisher name
        return rows
 
#######################################################
#############   CoolStuff End    ######################
#######################################################
#https://stackoverflow.com/questions/11314339/make-column-width-take-up-available-space-in-wxpython-listctrl
class ColumnsMatch(bggupload_gui.ColumnMatcher):
    def getmatchlist(self):
        match = []
        for index in range(self.listcontrols[2].GetItemCount()):
            match.append((
                self.listcontrols[2].GetItemText(index,col=0),
                self.listcontrols[2].GetItemText(index,col=1),
                ))
        return match
    def load(self,event):
        lists = collections.defaultdict(list)
        with codecs.open('matchfile.csv', 'r', encoding='utf-8') as f:
            for line in f:
                linevals = line.strip().split(',')
                key = linevals[0]
                vals = linevals[1:]
                # if not isinstance(vals,list):
                    # print('not list')
                lists[key].append(vals)
        self.resetlists(lists.get('list1',[]),lists.get('list2',[]),lists.get('listmatch',[]))
        # wx.QueueEvent(self,) or wx.PostEvent()
        # wx.EventHandler()
        # wx.Event()
    def save(self,event):
        with codecs.open('matchfile.csv', 'w', encoding='utf-8') as f:
            for listname, wxcontrol in (('list1',self.listcontrols[1]),
                                        ('list2',self.listcontrols[0]),
                                        ('listmatch',self.listcontrols[2])):
                ccount = wxcontrol.GetColumnCount()
                for i in range(wxcontrol.GetItemCount()):
                    v = [wxcontrol.GetItemText(i,col=c) for c in range(ccount)]
                    f.write(','.join((listname,*v)))
                    f.write('\n')
        event.Skip()
    #self.listcontrols[]
    def __init__(self,parent,listleft,listright,automatch=False,title='Column Matcher',*args,**kwargs):
        super(ColumnsMatch,self).__init__(parent,*args,**kwargs)
        self.SetTitle(title)
        self.listcontrols = list(filter(lambda x: isinstance(x,wx.ListCtrl),list(self.ListsPanel.GetChildren())))
        print('LC',self.listcontrols)
        listmatch = []
        list1 = list(listleft)
        list2 = list(listright)
        setright = set([x[0] for x in listright])
        #rightset = set(listright)
        for match in listleft:
            #print(match)
            if match in listright:
                #print('yes')
                listmatch.append((match[0],match[0]))
                list2.remove(match)
                list1.remove(match)
        
        print(len(list1),len(list2),len(listmatch),)

        print(list1,list2,type(listmatch))
        self.resetlists(list1,list2,listmatch)
        
        self.MakeModal()
    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler
    def resetlists(self,list1,list2,listmatch):
        self.listcontrols[1].ClearAll()
        self.listcontrols[1].AppendColumn('Export Column')
        self.listcontrols[0].ClearAll()
        self.listcontrols[0].AppendColumn('Import Column')
        self.listcontrols[2].ClearAll()
        self.listcontrols[2].AppendColumn('Export')
        self.listcontrols[2].AppendColumn('Import')
        print('RL',list1,list2,listmatch)
        for item in list1:
            print(item)
            self.listcontrols[1].Append(item)
        for item in list2:
            self.listcontrols[0].Append(item)
        for item in listmatch:
            # print(item)
            # if not isinstance(item,tuple):
                # print('not list')
            self.listcontrols[2].Append(item)
        for w in (self.listcontrols[1],self.listcontrols[0],self.listcontrols[2]):
            event = wx.SizeEvent(w.GetSize(),w.GetId())
            event.SetEventObject(w)
            wx.QueueEvent(w.GetEventHandler(), event)



    def unmatch(self,event):
        lastindex = None
        index = self.listcontrols[2].GetFirstSelected()
        while index != -1:
            try:
                e = self.listcontrols[2].GetItemText(index,col=0)
                i = self.listcontrols[2].GetItemText(index,col=1)
                self.listcontrols[1].Append([e])
                self.listcontrols[0].Append([i])
                self.listcontrols[2].DeleteItem(index)
                lastindex = index
                index = self.listcontrols[2].GetNextSelected(index)
            except:
                raise
        if lastindex is not None:
            self.listcontrols[2].Select(lastindex)
                
    def match(self,event):
        try:
            eindex = self.listcontrols[1].GetFirstSelected()
            iindex = self.listcontrols[0].GetFirstSelected()
            
            if (eindex != -1 and iindex != -1):
                e = self.listcontrols[1].GetItemText(eindex)
                i = self.listcontrols[0].GetItemText(iindex)
                self.listcontrols[2].Append((e,i))
                
                self.listcontrols[1].DeleteItem(eindex)
                self.listcontrols[0].DeleteItem(iindex)
                self.listcontrols[1].Select(0)
                print('Match Columns',e,i)
        except:
            raise
    def resize(self,event):
        listctrl = event.GetEventObject()
        #print('resize',listctrl)
        count = listctrl.GetColumnCount()
        width,height = listctrl.GetClientSize()
        colwidth = width/count
        for col in range(count):
            listctrl.SetColumnWidth(col,colwidth)

#######################################################
##########   Import CSV    ############################
######### ##############################################
class import_csv():
    """This becomes the default if no other importer works."""
    # rows1 = []
    # rowsmulti = []
    # with open(filename, 'r') as csvfile:
        # #reader = csv.reader(csvfile)
        # reader = csv.DictReader(csvfile)
        # for row in reader:
            # process_row(row)
    
    def __init__(self):
        pass
    def canimport(self,stream):
        try:
            sniff = csv.Sniffer()
            sample = stream.read(1024)
            self.dialect = sniff.sniff(sample)
            stream.seek(0)
            # reader = csv.reader(stream, dialect)
            # # ... process CSV file contents here ...
            if not sniff.has_header(sample):
                return False # Must have header
            reader = csv.DictReader(stream, dialect=self.dialect)
            self.inputfieldnames = reader.fieldnames
            for row in reader:
                pass
            return True
        except:
            print('Error in csv')
            raise
            return False
    def getrows(self,stream,title='Column Matcher'):
        rows = []
        reader = csv.DictReader(stream,dialect=self.dialect)
        #headings = map(lambda x: list(x),csv_output_headings)
        # headings = csv_output_headings
        #self.resetlists(map(lambda x: tuple(x),list1),map(lambda x: tuple(x),list2),listmatch)

        cm = ColumnsMatch(None,list(map(lambda x: (x,),csv_output_headings)),list(map(lambda x: (x,),self.inputfieldnames)),automatch=True,title=title)
        matchdict = {}
        
        cm.ShowModal()
        for e,i in cm.getmatchlist():
            matchdict[i] = e
        cm.Destroy()
        print(matchdict)
        # try:
            # cm.ShowModal()
        # except:
            # cm.Show()
            # cm.MakeModal(True)
            
        for row in reader:
            #print('before',len(row.keys()))
            for key in list(row.keys()):
                if key in matchdict:
                    if matchdict[key] != key:
                        # move
                        row[matchdict[key]] = row[key]
                        del(row[key])
                else:
                    del(row[key])
            for rowkey in row.keys():
                print(rowkey,row[rowkey])
            #print('after',len(row.keys()))
            #process_row(row)
            rows.append(row)
        return rows

#######################################################
#############   CSV End    ######################
#######################################################

#######################################################
##########   Import Miniature Market    ###############
#######################################################
class import_miniaturemarket():
    """Be sure to capture the "Thank you for your order from Miniature Market"
       line so the importer can recognize Miniature Market email.
       
       Email subject: Miniature Market: New Order
       """
    def __init__(self):
        self.date = None

    def canimport(self,stream):
        for line in stream:
            if line.startswith('Thank you for your order from Miniature Market'):
                return True
        return False
                
    def getrows(self,stream):
        rows = []
        #Your Order #101050456 (placed on December 1, 2017 2:46:31 AM CST)
        stage = 2
        for line in stream:
            #line = stream.readline()
            #print('importing row:',line)
            #sleep(1)
            if stage == 0:
                if line.startswith('Thank you again,'):
                    stage = 2
                    continue
                if re.match('^\s*$;',line):
                    continue
                s = line.split()
                pricepaid = s[-1]
                numowned = s[-2]
                try:
                    int(numowned)
                except:
                    continue
                print('importing row:',line)
                mmsku = s[-3]
                reducedline = ' '.join(s[:-3])
                rparen = reducedline.rfind(')')
                lparen = reducedline.rfind('(')
                #print('lparen={}; rparen={}; line={}'.format(lparen,rparen,reducedline))
                if lparen != -1 and rparen != -1:
                    comment1 = reducedline[lparen+1:rparen]
                    objectname = reducedline[:lparen].strip()
                else:
                    objectname = reducedline.strip()
                    
                comment = ', '.join(['MM SKU: '+mmsku,self.order,comment1])
                row = { 'objectname':objectname,
                        'own':1,
                        #'conditiontext':conditiontext,
                       'numowned':numowned,
                       'pricepaid':pricepaid,
                       'comment':comment
                       }
                if self.date is not None:
                    row['acquisitiondate'] = self.date
                print(row)
                rows.append(row)
                
# Item	Sku	Qty	Subtotal
# Master Builder (Clearance)	VLY204	1	$10.00


            if line.startswith('Your Order #'):
                octothorpe = line.find('#')
                spaceafter = line.find(' ',octothorpe)                
                self.order = line[octothorpe-6:spaceafter]
                placedon = line.find('placed on ')
                date = line[placedon+10:].strip()[:-1]
                self.date = dateutil.parser.parse(date)
                print('order: {}, on {}'.format(self.order,date))
                if stage == 2:
                    stage = 1
            if line.startswith('Item'):
                if stage == 1:
                    stage = 0

            # if line.startswith('Date'):
                # #self.date = dateutil.parser.parse(line.split()[-1])
                # self.date = parse(line.split()[-1])
            # if re.match(r'^[0-9]+\s+-\s+.*(.+).*$',line): # line is a row
                # print('found row')
        return rows

#######################################################
##########   Miniature Market End    ##################
#######################################################

#######################################################
##########   Import True    ###########################
#######################################################
# class import_true():
    # # def __init__(self):
        # # pass
    # def canimport(self,stream):
        # return True
#######################################################
##########   End Import True    #######################
#######################################################
#######################################################
##########   Import False   ###########################
#######################################################
class import_false():
    """For testing"""
    # def __init__(self):
        # pass
    def canimport(self,stream):
        return False
    def getrows(self,stream):
        return []
#######################################################
##########   End Import False   #######################
#######################################################
importers = list(filter(lambda x: x.startswith('import_'),dir()))#__builtins__)))
#importers
#print(dir(__builtins__))
#print('IMPORTERS:\n\t{}\n\t'.format('\n\t'.join(map(lambda x: x[len('import_'):],importers))))
for i in importers:
    iclass = globals()[i]
    print(i[7:].upper())
    print('      ',iclass.__doc__)
    print()

# for filename in ['coolstuff1.txt','mm1.txt']:
    # print('FILE: {}'.format(filename))
    # with open(filename,'r') as f:
        # for importer in importers:
            # print('IMPORTER: {}'.format(importer))
            # impclass = globals()[importer]()
            # canimport = impclass.canimport(f)
            # print(importer,canimport)
            # f.seek(0)
            # if canimport:
                # rows = impclass.getrows(f)
                # break
            # print(rows)
# sys.exit()

helptext = """BGG Interactive Upload Tool

Update your boardgamegeek.com collection using this GUI interface.

Manually enter search terms one at a time. Double click an image to put the desired item into the output file. The row of images representing a single search will then disappear.

Currently, this creates a CSV file for use with BGGCLI program. This program helps you interactively find the BGGID from a partial name, including manual term search and order confirmation emails from coolstuffinc.com and miniaturemarket.com.

This is experimental software in an Alpha release. Expect problems and difficulties at this point. The developer is seeking problem reports via https://github.com/HiGregSmith/bggupload/issues
 
Import board games from order confirmation email, csv file, or search input.

Each input row eventually makes its way into the output file.
If the row has a 'id', it is placed directly in the output file, if the row does not have a 'id' and does have an 'objectname', the objectname is used as a term search for manual selection.

Each row of images in the GUI represents an individual search. Select the one item per row that corresponds to the desired choice. Use the mouse and single click to navigate and browse. Double click to put the desired item into the output file.
"""
# http://www.iconarchive.com/show/pretty-office-7-icons-by-custom-icon-design/Save-as-icon.html
class gui(bggupload_gui.mainframe):
    def __init__(self,parent):
        bggupload_gui.mainframe.__init__(self,parent)
        
        #self.itemselected = [] # index is row
        #self.rowbyitem = {}
        #self.rowsgui = []
        #self.databyitem = {}
        self.databyrow = {}
        self.current = None
        #self.searchbylabel = {}
    def GetRowData(self,row):
        return self.databyrow[row]
        
    def GetData(self,item):
        return self.databyitem[item]
        
    def RemoveRow(self,event):
        if self.current:
            self.DeleteRow(self.current.GetParent())
            self.GetSizer().Layout()
        else:
            msg = "You must first select an item within the row to delete."
            wx.MessageDialog(None,msg).ShowModal()

    def AddRow(self,data):
        print('Adding row:',data)
        parent = self.mainwindow
        row = wx.Panel( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.databyrow[row] = data
        bsizer = wx.BoxSizer( wx.HORIZONTAL )
        row.SetSizer( bsizer )
        row.Layout()
        bsizer.Fit( row )
        #parent.GetSizer().Add( row, proportion=1, flag=wx.EXPAND, border=5 )
        parent.GetSizer().Add( row, proportion=0, flag=wx.EXPAND, border=5 )
        #self.rowsgui.append((row,bsizer))
        #self.itemselected.append(None)
        return row
    def DeleteRow(self,row):
        #row = self.rowsgui[rownum][0]
        #row = panel.GetParent()
        #rowholder = row.GetParent()
        #s = row.GetSizer()
        row.Destroy()
        #s.Layout()
        # psizer = panel.GetSizer()
        # psizer.Remove(rownum)
        # panel.Parent().Remove
        #rowholder.GetSizer().Layout()
    # def GetRowFromItem(self,item):
        # return self.rowbyitem.get(item,None)
        
    def AddRowItem(self,item,data):
        pass
        #print (item)
        #self.rowsgui[-1][0].AddChild(item)
        # self.rowsgui[-1][1].Add(item)
        # self.rowbyitem[item] = len(self.rowsgui)-1
        # self.databyitem[item] = data

    def DeselectRow(self,item):
        #row = item._row # self.rowbyitem[item]
        previousitems = item.GetParent().GetChildren() # self.itemselected[row]
        if previousitems:
            for previousitem in previousitems:
                if previousitem._status != 0:
                    previousitem.SetStatus(0)
                    #self.itemselected[row] = None
                    previousitem.Refresh()

    def SelectRowItem(self,item,deselect=True):
        row = item._row # self.rowbyitem[item]
        print ('Row = {}'.format(row))
        if deselect:
            self.DeselectRow(item)
        #self.itemselected[row] = item
        item.SetStatus(1)
        item.Refresh()
        print(self.databyitem[item])
        

	# Overide virtual event handlers.
    def KillFocusImage( self, event ):
        self.SetBackgroundColour('white')
        print('white')
        event.Skip()
        	
    def SetFocusImage( self, event ):
        self.SetBackgroundColour('blue')
        print('blue')
        event.Skip()
        
    def Search( self, event ):
        global SearchQueue    
        print('search')
        searchterm = self.searchbox.GetValue()
        self.searchbox.SetSelection(-1,-1)
        self.AddToQueue({'searchterm':searchterm})
        event.Skip()
        
    def AddToQueue(self,data):
        searchterm = data.get('searchterm',None) or data.get('objectname',None)
        print('Text label [{}] {}'.format(searchterm,data))
        t=wx.StaticText(self.importlist,label=searchterm)
        self.importlist.GetSizer().Add(t)
        self.importlist.Layout()
        # add to search queue and start search
        SearchQueue.put(data)
        SearchQueueStart()

        
    def About(self,event):
        d=bggupload_gui.helpdialog(self)
        finalhelptext = helptext+'\n\nCurrent Preferences: {}\nThese preferences are editable in the source code.'.format(str(preferences))
        d.helptextbox.SetValue(finalhelptext)
        d.ShowModal()

    def SearchResult(self,result):
        search,images,tree = result
        child = self.importlist.Children[0]
        if search != child.GetLabel():
            print("Search and result out of sync. Wanted {} got {}.".format(child.GetLabel(),search))
        p = child.GetParent()
        s = p.GetSizer()
        #s.Remove(child)
        child.Destroy()
        #self.importlist.RemoveChild(child)
        p.Update()
        s.Layout()
        time.sleep(2)
        print("Got Search Results.")
    def ImportFile(self,event):
        '''Import selected file using automatic format detection'''
        # ask the user what new file to open
        # with wx.FileDialog(self, "Open XYZ file", wildcard="XYZ files (*.xyz)|*.xyz",
                           # style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
        with wx.FileDialog(self, "Import boardgame file", wildcard="All files|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            for filename in [pathname]:#['coolstuff1.txt','mm1.txt']:
                try:
                    with open(filename, 'r') as f:
                        print('FILE: {}'.format(filename))
                        for importer in importers:
#                            print('Trying IMPORTER: {}  ...  '.format(importer),end='')
                            impclass = globals()[importer]()
                            canimport = impclass.canimport(f)
                            # print(importer,canimport)
                            f.seek(0)
                            if canimport:
                                print('Importing using {}.'.format(importer))
                                rows = impclass.getrows(f)
                                if not rows:
                                    msg = "There are no rows in the input file."
                                    wx.MessageDialog(None,msg).ShowModal()
                                    break
                                print('Importing {} rows.'.format(len(rows)))
                                # DO STUFF WITH ROWS HERE
                                for row in rows:
                                    print('RK',list(row.keys()))
                                    mframe.AddToQueue(row)
                                #print(rows)
                                break
                            
                            print('NOPE!')
                except IOError:
                    wx.LogError("Cannot open file '%s'." % filename)        

    

# There are several search results distinguished by background color:
#    dark green - bgg search, exact
#    dark green - local db, exact
#    light green - bgg search, non-exact (matching word beginnings)
#    gray - local db fuzzy match with score

# black - highlighted
# red - Selected
class ImgPanel(wx.Panel,wx.ClientDataContainer):
    #data = None
    _MATCHSCORE = 100
    #databyitem = {}
    
    def __init__(self,parent, image, text, url, data, score, guiinstance, tip = None):
        #print('text: ',text)
        self._row = None
        self._data = data
        self._status = 0
        self._selected = False
        self._score = score
        # scale so 60-100 is 0-256
        fromtorange = ((70,100),(0,256))
        #gray = 70+(100-score)*256/30
        gray = max((score - 70)*(256-0)/(100-70)+0,0)
        self.unselectedbgcolor = wx.Colour(gray,gray,gray)
        self.guiinstance = guiinstance
        wx.ClientDataContainer.__init__(self)
        wx.Panel.__init__(self, parent)
        #self.data = data
        #self.SetClientData(self.data)
        try:
            img = wx.Image(image, wx.BITMAP_TYPE_ANY)
            self.sBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
        except:
            try:
                raise
                img = wx.Image(getseekablestream(r'https://cf.geekdo-images.com/images/pic1657689_t.jpg'), wx.BITMAP_TYPE_ANY)
                self.sBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
            except:
                try:
                    noimagefile = r'noimageavailable_t.jpg'
                    img = wx.Image(open(noimagefile,'rb'), wx.BITMAP_TYPE_ANY)
                    self.sBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
                except:
                    p = wx.Panel(self,id=wx.ID_ANY)
                    p.SetBackgroundColour('blue')
                    self.sBmp = p 

        if tip:
            self.SetToolTip(tip)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.sBmp, proportion=0, flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER, border=10)
        #infolink = 
        self.getlink(sizer,text,url)
        #self.SetBackgroundColour('green')
        self.SetSizerAndFit(sizer)
        #self.defaultbg = self.sBmp.
        self.Bind( wx.EVT_KILL_FOCUS, self.KillFocusImage )
        self.Bind( wx.EVT_SET_FOCUS, self.SetFocusImage )
        self.Bind( wx.EVT_KEY_DOWN, self.KeyDownImage )
        self.sBmp.Bind( wx.EVT_LEFT_DCLICK, self.DClickItem )
        self.sBmp.Bind( wx.EVT_LEFT_DOWN, self.ClickItem )
        #self.sBmp.Bind( wx.EVT_MOUSE_EVENTS, self.MouseEvents )
        self.sBmp.Bind( wx.EVT_ENTER_WINDOW, self.HoverDisplay )
        #self.sBmp.Bind( wx.EVT_LEAVE_WINDOW, self.MouseEvents )

        # #self.Bind( wx.EVT_NAVIGATION_KEY, self.KeyDownImage)
        # self.Bind( wx.EVT_COMMAND_ENTER, self.KeyDownImage)
        #print (self.IsFocusable())
        #self.Bind( wx.EVT_CHAR, self.KillFocusImage )
        #self.Bind( wx.EVT_KEY_UP, self.KillFocusImage )
        #self.SetBackgroundColour('green')
        #print("IsFoc: {}".format(self.IsFocusable()))
        #self.SetDoubleBuffered(False)
        # onchar
        # on_keydown
        # EVT_KEY_DOWN
        # EVT_KEY_UP
        # EVT_CHAR
        self.SetBackgroundColour(self.unselectedbgcolor)
    def getlink(self,sizer,text,link):
        infolink = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, text, link, wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
        infolink.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        infolink.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        #sizer.Add( infolink, wx.BOTTOM, wx.CENTER, 10 )
        sizer.Add(infolink, flag=wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER, border=10)
        return infolink
    def KeyDownImage( self, event ):
        #print('white')
        p = event.GetEventObject()
        p.guiinstance.SelectRowItem(p)
        # if self.status == 0:
            # self.status = 1
        # else:
            # self.status = 0
        # self.SetFocusImage(event)
        event.Skip()
        
    def KillFocusImage( self, event ):
        #print('white')
        p = event.GetEventObject()#.GetParent()
        if p._status:
            p.SetBackgroundColour('red')
        else:
            p.SetBackgroundColour(self.unselectedbgcolor)
        p.Refresh()
        event.Skip()
    def ClearCurrent( self ):
        p = mframe.current
        mframe.current = None
        if p:
            if p._status:
                p.SetBackgroundColour('red')
            else:
                p.SetBackgroundColour(p.unselectedbgcolor)
            p.Refresh()
        #event.Skip()

    def SetCurrent(self):
        self.ClearCurrent()
        mframe.current = self
        #print('SetCurrent')
        self.SetBackgroundColour('green')
        self.Refresh()
        itype,id = item2idt[self]
        #names = '{} {}'.format(str(id),
        pri = [line.itemname for line in filter(lambda x: x.itemnametype=='primary', fullbgg4[(itype,id)])]
        alt = [line.itemname for line in filter(lambda x: x.itemnametype!='primary', fullbgg4[(itype,id)])]
        print('Highlighted',itype,id, ', '.join(pri))
        if alt:
            label='{} alt: {}'.format(' | '.join(pri),' | '.join(alt))
        else:
            label='{}'.format(' | '.join(pri))
        #print()
        data = mframe.GetRowData(self.GetParent())
        searchterm = data.get('searchterm',None) or data.get('objectname',None)
        mframe.searchbox.SetValue(searchterm)
        mframe.infolink.SetToolTip('{}:{}'.format(itype,id))
        mframe.infolink.SetLabel(label)
        mframe.infolink.SetURL(r'https://boardgamegeek.com/{}/{}/'.format(cat[itype],str(id)))
    
    def SetFocusImage( self, event ):
        imgpanel = event.GetEventObject()
        print('sfi: {}'.format(item2idt[imgpanel]))
        self.SetCurrent()
        event.Skip()

    def MouseEvents(self,event):
        attributes = filter(lambda c: 'A' <= c[0] <= 'Z', dir(event))
        print('mouse event:')
        for a in attributes:
            if a.startswith('Set') or a == 'Clone' or a == 'Destroy':
                continue
            try:
                val = getattr(event,a)()
                if val != False:
                    print('\t{} IS {}'.format(a,str(val)))
            except:
                pass
        print()
        event.Skip()

    def HoverDisplay(self,event):
        object = event.GetEventObject().GetParent()
        itype,id = item2idt[object]
        #print('hover {} {}'.format(itype,id))
        
        event.Skip()

    def ClickItem(self,event):
        child = event.GetEventObject()
        imgpanel = child.GetParent()
        #child.SetFocus()
        imgpanel.SetCurrent()
        # if imgpanel.HasFocus():
            # imgpanel.SetCurrent()
        # else:
            # imgpanel.SetFocus()
        #self.focus(imgpanel)
        #print('click {}'.format(item2idt[imgpanel]))
        event.Skip()

    def DClickItem(self,event):
        #print("item dclicked")
        object = event.GetEventObject()
        object._selected = True
        
        p = object.GetParent() # Get ImgPanel
        rowobject = p.GetParent()
        dataorig = mframe.GetRowData(rowobject)
        datanew = fullbgg4[p._data]
        
        print('data',datanew)
        datanew = {
            'objectid':datanew[0].itemid,
            #'yearpublished':datanew[0].itemyear,
            #'':datanew[0].itemtype,
            #'objecttype':datanew[0].category,
            'own':1,
        }
        dataorig.update(datanew)
        #p.guiinstance.SelectRowItem(self)
        #mframe.SelectRowItem(p)
        #datanew = mframe.GetData(p)
        
        row = p.GetParent()
        rowdata = mframe.GetRowData(row)
        print('ROWDATA',rowdata)
        outputmgr.saverows([dataorig]) # hash of values corresponding to CSV columns
        mframe.DeleteRow(row)
        mframe.GetSizer().Layout()
    def GetStatus(self):
        return self._status

    def SetStatus(self,status):
        self._status = status
        if self._status:
            self.SetBackgroundColour('red')
        else:
            self.SetBackgroundColour(wx.NullColour)
	

def search(searchstring,exact=False):
    parameters = {'type':'boardgame',
                  # 'type':'boardgame,boardgameaccessory,boardgameexpansion',
                  # 'query':'yam'
                  }
    parameters['query'] = searchstring.replace(' ','+')
    if exact:
        parameters['exact'] = '1'
    url = fullurl('search',parameters)
    return getxmlresponse(url)
import sys, traceback
def getxmlresponse(url):
    print(url)
    try:
        response = requests.get(url)
        print (response.status_code, 'response from',url)
        tree = ET.fromstring(response.content)
        return tree
    except:
        traceback.print_exc(limit=2, file=sys.stdout)
        return []
    
def gethtmlresponse(url,printresponse=False):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.get(url, headers=headers)
    print (response.status_code, 'response from',url)
    if printresponse:
        print(response.content)
    with open('upc_response.txt','wb') as f:
        f.write(response.content)
    tree = lxml.html.document_fromstring(response.content)
    return tree
    
def fullurl(command,parameters,base='https://www.boardgamegeek.com/xmlapi2/'):
    qstring = '?'+'&'.join(['='.join((k,v)) for k,v in parameters.items()])
    return base+command+qstring

# tree = search('yam')

def tree2idts(tree):
    p = []
    #print len(tree),tree
    for item in tree:
        #print 'item',item
        p.append([])
        #print item.tag,item.attrib
        p[-1].append(item.attrib['id'])
        p[-1].append(item.attrib['type'])
        
        for i in item:
            #print '\t',i.tag,i.attrib
            if i.tag == 'name':
                p[-1].append(i.attrib['value'])
    val = [(row[0],row[1]) for row in p]
    #print('tree2idts:',val)
    return val
    
import io

def getseekablestream(url):
    try:
        r = requests.get(url, stream=True)
    except:
        return None
    if r.status_code != 200:
        print ('Status returned {}'.format(r.status_code))
        return None
    r.raw.decode_content = True
    return io.BytesIO(r.raw.data)

def getbitmap(url):
    bm = wx.Bitmap( wx.Image( getseekablestream(url) ))
    return bm 

def getstaticbitmap(parent,url):
    return wx.StaticBitmap(parent,bitmap=getbitmap(url))

def chunklist(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def getthumbnails(idlist):
    # list of id,type
    idthumb = []
    idbytype = collections.defaultdict(list)
    for idt in idlist:
        idbytype[idt[1]].append(idt[0])
        
    #types = list(set([x[1] for x in idlist]))
    #t=','.join(types)

    print(idbytype)
    for t,ids in idbytype.items():
        for idchunk in list(chunklist(ids, 20)):
            print (t, idchunk)
            ids = ','.join(idchunk)
            url = fullurl('thing',{'id':ids})#,'type':t})
            print(url)
            for item in getxmlresponse(url):
                id = item.attrib.get('id',None)
                #t = item.attrib['type']
                thumb = None
                for element in item:
                    if element.tag == 'thumbnail':
                        thumb = element.text
                        break
                idthumb.append((id,t,thumb))
        
    return idthumb
    
def getids(name):
    time.sleep(2)
    tree = search(name,exact=1)
    if len(tree) == 0:
        time.sleep(2)
        tree = search(name)
    if len(tree) == 0:
        return [] #print("Can't find.")
    return tree2idts(tree)
# def addimagerow():
    # Add panel
    # Add horizontal box sizer
    
# '609456647236'
import re
# walmart api key: utvw9w4bk9ee27zqmr34knnn
class upc3():
    @staticmethod
    def getproductinfo(upc_codes):
        apikey = 'utvw9w4bk9ee27zqmr34knnn'
        #upc = '035000521019'
        url = r'http://api.walmartlabs.com/v1/items?apiKey={apikey}&upc={upc}'.format(apikey=apikey,upc=upc_codes[0])
        response = requests.get(url)
        print(response.content)
        

class upc2():
    @staticmethod
    def getproductinfo(upc_codes):
        #https://www.upcse.com/upc/782361602122/
        url = r'http://www.upcse.com/upc/'+upc_codes[0]+r'/'
        tree = gethtmlresponse(url)
        #print(tree.xpath("//ul[@class='tabled-data' and label[text()='Product']]"))#/div[@class='value']/text()"))
        productname = tree.xpath("//ul/li[label[contains(text(),'Product')]]/div[@class='value']/text()")[0]#/div[@class='value']/text()"))
        #print(tree)
        
        # Remove parenthetical phrases
        productname = re.sub(r'\([^)]*\)', '', productname)
        return productname
        
#print(upc3.getproductinfo(['782361602122']))
#print(upc3.getproductinfo(['035000521019']))

#tree = lxml.html.document_fromstring(r.content)

class upc4():
#//*[@id="internal-db"]/div/table/tbody/tr[2]/td[1]
    @staticmethod
    def getproductinfo(upc_codes):
        #782361602115
        url = r'https://barcodesdatabase.org/barcode/'+upc_codes[0]+r'/'
        tree = gethtmlresponse(url)
        productname = tree.xpath('//tr[td="Product name"]')#/td[2]')
        productname = tree.xpath('//tr/td')
        return productname
class asin:
    @staticmethod
    def get_asin(upc):
        url = r'https://www.amazon.com/s/?field-keywords={upc}'.format(upc=upc)
        print ('URL:',url)
        tree = gethtmlresponse(url)
        asin = tree.xpath('//li/@data-asin')
        return asin
        
# Use UPC to lookup ASIN 
# https://www.amazon.com/s/?field-keywords=782361602122
upcs = [
    '782361602122',
    '035000521019', # Sensitive Toothpaste, for Sensitive Teeth and Cavity Protection, Maximum Strengt
#                      12345678901234567890123456789012345678901234567890123456789012345678901234567890
#                               1         1         1         1         1         1         1         1
    '0609456647236',
    '8594156310400',
    ]
# for upc in upcs:
    # try:
        # #value = asin.get_asin(upc)
        # value = upc4.getproductinfo([upc])
        # print(value)
    # except Exception as e:
        # print(e)
        
    # sleep(5)
# sys.exit()
class upc5():
    @staticmethod
    def getproductinfo(upc_codes,printresponse=False):
        url = r'https://api.upcitemdb.com/prod/trial/lookup?upc={upc}'.format(upc=upc_codes[0])
        response = requests.get(url)
        print ('page from url',url, response.status_code )
        if printresponse:
            print(response.content)
        with open('upc_response.txt','wb') as f:
            f.write(response.content)
        jsonresult = lxml.html.document_fromstring(response.content)
        return tree
import json        
  # \"upc\": \"4002293401102\"
# }" "https://api.upcitemdb.com/prod/trial/lookup?upc=4002293401102"

class upc1():
    @staticmethod
    def getproductinfo(upc_codes):
        upc = ','.join(upc_codes)
        url = 'http://www.searchupc.com/handlers/upcsearch.ashx'
        '?request_type=1&access_token=29A4EF8F-6053-4A75-BB67-3F9857E328C7&'
        'upc=' + upc
        # http://www.searchupc.com/handlers/upcsearch.ashx?request_type=1&access_token=29A4EF8F-6053-4A75-BB67-3F9857E328C7&upc=
        r = requests.get(url, stream=True)

        if r.status_code != 200:
            print ('Status returned {}'.format(r.status_code))
            return None
        r.raw.decode_content = True
        
        reader = csv.DictReader(r.raw)
        rows = []
        for row in reader:
            rows.append(row)
        return rows
        
class upc_common():
    @staticmethod
    def isupc(upc):
        upc=str(upc)[::-1] # reverse the string
        if len(upc) < 5:
            return False
        #print('UPC:',upc)
        # Check digit is now upc[0]
        # Mult odd digits by 3 and even by 1
        # Result should match the check digit
        # print(upc[1::2])
        # print(upc[2::2])
        try:
            three = map(lambda s: int(s),upc[1::2])
            one = map(lambda s: int(s),upc[2::2])
            # print(three)
            # print(one)
            total = sum(map(lambda s: int(s),upc[1::2])) * 3 +\
                    sum(map(lambda s: int(s),upc[2::2])) 
            zero = 10 - (total%10) - int(upc[0])            
        except ValueError:
            return False
        return zero == 0

name2id = collections.defaultdict(list)
def matchsetup():

    masterwordlistfile = r'..\..\2017-02-21.csv'
    masterwordlistfile = r'..\..\currentlistover30ratings.csv'
    
#    with open(masterwordlistfile,'r') as f:
    with codecs.open(masterwordlistfile, encoding='utf-8') as f:
        for line in f:
            seg = line.split(',')
            name2id[seg[1]].append(seg[0])
# print('Reading Over 30 Ratings file.')
# matchsetup()
# over30 = set(name2id.keys())
# over30 vs. bggnames
#notinbggnames = over30 - bggnames
#notinover30 = bggnames - over30
#print('In bggnames:',len(bggnames))
#print('In over30:',len(over30))
#print('Not in bggnames:',len(notinbggnames))
#print('Not in over30:',len(notinover30))
#print('Not in bggnames:',notinbggnames)
#https://raw.githubusercontent.com/beefsack/bgg-ranking-historicals/master/2017-12-31.csv

#print(name2id)
catidbyname = collections.defaultdict(list)
def matchname(name):
    # fuzz.token_set_ratio(name)
    #choices = name2id.keys()
    #choices = bggr.idbyname.keys()
    itypes = set()
    for catid, lines in fullbgg4.items():
        for line in lines:
            #(category, itemid, itemtype, itemname, itemnametype, itemyear) = line
            if line.itemtype in set(['boardgame','thing']):
                catidbyname[line[3]].append((line.itemtype,line.itemid))
                itypes.add(line.itemtype)
    print('match types',itypes)
    choices = catidbyname.keys()
    #print(list(filter (lambda x : x.startswith('Timelin'),choices)))
    #print(choices)
    #results = process.extract(name,choices,scorer=fuzz.ratio,limit=5)
    #results = process.extractOne(name,choices,score_cutoff=90)#,limit=5)
    # fuzzycount':2,'fuzzyminscore
    print('Searching local database...')#,end='')
    results = process.extract(name,choices,limit=preferences['fuzzymaxcount'])
    resultsabovemin = list(filter(lambda x: x[1] >= preferences['fuzzyminscore'],results))
    print('done.')
    if len(resultsabovemin) < preferences['fuzzymincount']:
        results = results[:preferences['fuzzymincount']]
    else:
        results = resultsabovemin
    print('{} MATCHES'.format(name))
    for name,score in results:
        print('\t{} {} {}'.format(score,str(catidbyname[name]),name))        
    return results
    # bggr = ReadBGGResults(); bggr.getall(); len(bggr.idbyname); len(bggr.fullbgg['boardgame'])
def searchname(name):
    print('Searching BGG for: {}...'.format(name),end='')
    time.sleep(2)
    tree = search(name,exact=1)
    if len(tree) == 0:
        time.sleep(2)
        tree = search(name)
    if len(tree) == 0:
        print("Zero exact matches from boardgamegeek.com.")
    return tree

MatchItem = collections.namedtuple("MatchItem","id itype thumbstream score")
item2idt = {}
def process_row(rowdata):
    id = rowdata.get('objectid',None)
    if id is None or id == '':
        try:
            name = rowdata['objectname']
        except:
            return
            print(rowdata)
            #continue
        if upc_common.isupc(name):
            print('isupc:',name)
            
            upcrows=getproductinfo(name)
            print(upcrows)
        try:
            tree = searchname(name)
            idlist = tree2idts(tree)
        except:
            idlist = []
        matchlist = []
        resultmatchlist = []
        for id,itype in idlist:
            matchlist.append([id,itype,None,100])
        
        namescorelist = matchname(name) # returns list of (name,score)
        for name,score in namescorelist:
            for category,id in catidbyname[name]:
                matchlist.append([id,category,None,score])
                
            #id,t,getseekablestream(thumb),100
        #matchids = []
        # for match in namescorelist:
            # matchids.extend(catidbyname[match[0]])
        #getseekablestream(thumb)
        #print('('+str(len(tree))+') '+' '.join(idlist))
    #print()
        if len(idlist) == 1:
            #print(dir(rowdata))
            rowdata['objectid'] = idlist[0][0]
            rowdata['objecttype'] = idlist[0][1]
            #rows1.append(rowdata)
            
        if len(matchlist) > 1:
            #rowsmulti.append(rowdata)
            print('pre matchlist',matchlist)
            idthumburl = getthumbnails(list(set([(m[0],m[1]) for m in matchlist])))
            # returns list of id,t,thumb
            print('pre idthumburl',idthumburl)
            pset = set()
            for m in matchlist:
                key = (m[0],m[1])
                if key in pset:
                    continue
                pset.add(key)
                try:
                    #print('?',end='')
                    r = list(filter(lambda x: x[0]==m[0] and x[1]==m[1] ,idthumburl))[0]
                    #print('r',r)
                except:
                    print("Doesn't match",m)
                    r=(None,'https://cf.geekdo-images.com/images/pic1657689_t.jpg',None)
                resultmatchlist.append(MatchItem(m[0],m[1],getseekablestream(r[2]),m[3]))
                
            # for id,t,thumb in idthumburl:
                # matchlist.append(MatchItem(id,t,getseekablestream(thumb),100))
            #print('post',resultmatchlist)
        wx.CallAfter(append_gui_row,resultmatchlist,rowdata)

def append_gui_row(matchlist,data,row=None):
    print('append_gui_row',len(matchlist))
    if row is None:
        r = mframe.AddRow(data)
    else:
        r = None
        raise
        
    s = r.GetSizer()
    for matchitem in matchlist:
    #for id,itype,thumbstream in idthumbstream:
        #bsi = fullbgg4[(itype,id)]
        bsi = list(filter(lambda x: x.itemnametype=='primary',fullbgg4[(matchitem.itype,matchitem.id)]))[0]
        #url = fullurl('thing',{'id':bsi.itemid,'type':bsi.itemtype})
        #print('matchid',matchitem.id)
        paren = ''
        if fullbgg4.get(('boardgameexpansion',matchitem.id),None) is not None:
            paren = 'expansion '
            
        if bsi.itemyear:
            paren +=  bsi.itemyear
        else:
            paren += matchitem.itype
        url = r'https://boardgamegeek.com/{}/{}/'.format(cat[matchitem.itype],str(matchitem.id))
        bmp = ImgPanel( r,
            matchitem.thumbstream,
            '{n}\n({y}) fuzzy:{s}'.format(s=matchitem.score,n=bsi.itemname,y=paren),
            url,
            (matchitem.itype,matchitem.id), # <---- data
            matchitem.score,
            mframe,
            tip=str(bsi)
        )
        mframe.AddRowItem(bmp,(matchitem.itype,matchitem.id))
        s.Add(bmp)
        item2idt[bmp] = (matchitem.itype,matchitem.id)
    mframe.GetSizer().Layout()
    if len(mframe.importlist.Children) > 0:
        child = mframe.importlist.Children[0]
        # if search != child.GetLabel():
            # print("Search and result out of sync. Wanted {} got {}.".format(child.GetLabel(),search))
        p = child.GetParent()
        s = p.GetSizer()
        #s.Remove(child)
        child.Destroy()
        #self.importlist.RemoveChild(child)
        p.Update()
        s.Layout()

def process_csv(filename):
    rows1 = []
    rowsmulti = []
    with open(filename, 'r') as csvfile:
        #reader = csv.reader(csvfile)
        reader = csv.DictReader(csvfile)
        for row in reader:
            process_row(row)

    with open(filename+'multi', 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in rowsmulti:
            writer.writerow(row)
    with open(filename+'1', 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in rows1:
            writer.writerow(row)

            
# for row in p:
    # print ' '.join(row).encode("utf-8")

mframe = gui(None)
mframe.SetTitle(outputmgr.backupfile)
#mframe.SetTitle(outputmgr.fullpath)
mframe.Show(True)
StatusThreadStart()
app.MainLoop()
sys.exit()

url = r'https://www.boardgamegeek.com/xmlapi2/search?type=boardgame,boardgameaccessory,boardgameexpansion&query=yam'


print ( urlparse.urlparse(url))

rooturl = 'https://boardgamegeek.com/'
apipath = 'xmlapi2'
command = 'query'
parameters = {'type':'boardgame,boardgameaccessory,boardgameexpansion',
              'query':'yam'
            }

            
sys.exit(0)

rooturl = 'https://boardgamegeek.com/'
#r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
r = requests.get(rooturl,stream=True)
print (r.cookies)
# https://www.boardgamegeek.com/xmlapi2/
# type=boardgame,boardgameaccessory,boardgameexpansion

# thing?
# https://www.boardgamegeek.com/xmlapi2/search?type=boardgame,boardgameaccessory,boardgameexpansion&query=yam


# Construct full url

def DictFromForm(formelement):
    for input in formelement.inputs:
        
        if hasattr(input,'type'):
            t=input.type
        else:
            t=None 
        print(input.name,t,input.value)

        
tree = lxml.html.document_fromstring(r.content)
for form in tree.xpath("//form[@action='/login']"):
    print(type(form))
    print('FORM={} ACTION="{}"'.format(form.method,form.action,form.base_url))
    for input in form.inputs:
        if hasattr(input,'type'):
            t=input.type
        else:
            t=None 
        print(input.name,t,input.value)

# print("waiting 10\n")
# sleep(10)
# SearchStop = True
