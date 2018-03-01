import requests
import xml.etree.ElementTree as ET
import sys, traceback
import io
from urllib.parse import urlparse
# o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')

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

def getxmltree(url):
    print(url)
    try:
        response = requests.get(url)
        print (response.status_code, 'response from',url)
        tree = ET.parse(io.StringIO(response.text))
        print('got tree')
        return tree
    except:
        traceback.print_exc(limit=2, file=sys.stdout)
        return []

def fullurl(command,parameters,base='https://www.boardgamegeek.com/xmlapi2/'):
    qstring = '?'+'&'.join(['='.join((k,v)) for k,v in parameters.items()])
    return base+command+qstring

# Examples:
#    https://boardgamegeek.com/xmlapi2/thing?id=432&versions=1
#    bggid = 432
#    getxmlresponse(fullurl(thing,{'id':bggid,'versions':1))

# items
#   item...
#     versions...
#        item...
#        

# Example of parsing:
            # for item in getxmlresponse(url):
                # id = item.attrib.get('id',None)
                # #t = item.attrib['type']
                # thumb = None
                # for element in item:
                    # if element.tag == 'thumbnail':
                        # thumb = element.text
                        # break
                # idthumb.append((id,t,thumb))
def get_versions(tree):
    """Given the ElementTree, get an organized list of objects corresponding to the version information from BGG."""
    print('getting versions')
    infolist = []
    # #print(type(tree))
    # #print(dir(tree))
    # ids = tree.findall(r'./item')
    # print(list(map(lambda x: x.get('id'),ids)))
    # #print(ids[0].attrib['id'])
    # vitems = ids[0].findall('./versions/item')
    # vinfo = vitems[0].findall('./*[self()="yearpublished" or self()="name"]')
    # #vinfo = vitems[0].findall("*[local-name()='yearpublished' or local-name()='name']")
    
    # #vid = vitems.findall('yearpublished')
    # print(vinfo)
    # return
    #print(dir(tree))
    for item in tree.getroot():
        print('item',item.tag)
        itemid = item.attrib.get('id',None)
        for iteminfo in item:
            if iteminfo.tag != 'versions':
                continue
            #print('iteminfo',iteminfo.tag)
            for versionitem in iteminfo:
                info = {'itemid':itemid}
                versionid = versionitem.attrib.get('id')
                info['vid'] = versionitem.attrib.get('id')
                #print('versionitem',versionitem.tag,versionid)
                for versioniteminfo in versionitem:
                   #thumbnail,image,name (attrib='primary'),yearpublished,
                    if versioniteminfo.tag == 'link':
                        info.setdefault(versioniteminfo.tag,[]).append(
                            (versioniteminfo.attrib['type'],
                            versioniteminfo.attrib['id'],
                            versioniteminfo.attrib.get('value',None),
                            versioniteminfo.attrib.get('inbound',None),
                            ))
                        #type="boardgameversion" id="432" value="6 nimmt!" inbound
                    elif versioniteminfo.tag in ('image','thumbnail'):
                        info[versioniteminfo.tag] = versioniteminfo.text
                    elif versioniteminfo.tag == 'yearpublished':
                        info[versioniteminfo.tag] = versioniteminfo.attrib['value'] 
                    elif versioniteminfo.tag == 'name':# and versioniteminfo.attrib['sortindex']==1:
                        info[versioniteminfo.tag] = versioniteminfo.attrib['value']
                    else:
                        info[versioniteminfo.tag] = versioniteminfo.attrib.get('value',None)
                    
                infolist.append(info)
    # for i in infolist:
        # print(i)
    #imagefile = urlparse(info['image']).path.split('/')[-1]
    print('returning infolist')
    return infolist
# get_id2file(get_versions(tree))    
def get_id2file(infolist):
    """return dictionary of filenames accessible by version id"""
    print('id2file')
    #infolist = get_versions(tree)
    id2file = {info['vid']:url2file(info['image']) for info in infolist}
    # for k,v in id2file.items():
        # print(k,v)
    print(id2file)
    return id2file

def url2file(url):
    """return the last portion of the path (i.e. filename) from the url"""
    return urlparse(url).path.split('/')[-1]