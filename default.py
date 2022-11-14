# -*- coding: utf-8 -*-

""" Autoruns
    2015 fightnight
    2022 bittor7x0"""

import xbmc,xbmcvfs,xbmcaddon,xbmcgui,xbmcplugin,urllib.request,urllib.parse,urllib.error,os,re,sys
import xml.etree.ElementTree as ET

SERVICE_DISABLED = 'Autoruns_service_disabled'

def list_addons():
      #info directory
      addDir('[COLOR blue][B]%s[/B][/COLOR]' % (translate(30001)),'None',None,xbmcaddon.Addon().getAddonInfo('icon'))

      #get the path of addons
      pathofaddons = xbmcvfs.translatePath('special://home/addons')

      #list with addons
      listofaddons = os.listdir(pathofaddons)
      for individual_addon in listofaddons:
            #path to individual addon, cycle for all the addons
            path_to_addon = os.path.join(pathofaddons, individual_addon)

            #define addon.xml path
            addon_xml_path=os.path.join(path_to_addon,'addon.xml')

            #check the existence of addon.xml, if true, we continue
            if os.path.exists(addon_xml_path):

                  #get addon.xml content
                  xml_content=openfile(addon_xml_path)

                  if re.search(SERVICE_DISABLED,xml_content):
                        #addon with service off
                        addDir('[B][COLOR gold]%s[/B] (off)[/COLOR]' % (individual_addon),path_to_addon,1,xbmcaddon.Addon(individual_addon).getAddonInfo('icon'))
                  elif re.search('point="xbmc.service"',xml_content):
                        #addon with service on
                        addDir('%s (on)' % (individual_addon),path_to_addon,1,xbmcaddon.Addon(individual_addon).getAddonInfo('icon'))
                  else:
                        #addon with no service
                        pass

def change_state(name,path):
      #define addon.xml path to change
      addon_xml_path=os.path.join(path,'addon.xml')

      #get addon.xml content
      content=openfile(addon_xml_path)

      if re.search('COLOR gold',name):
            #service off to on, so we uncomment the service element
            content=content.replace('<!--%s ' % (SERVICE_DISABLED),'').replace(' %s-->' % (SERVICE_DISABLED),'')
      else:
            #service on to off, so we comment the service element
            root = ET.fromstring(content)
            parent = root.findall("./extension[@point='xbmc.service']/..")[0]
            child = parent.findall("./extension[@point='xbmc.service']")[0]
            commented = '%s \n%s %s' % (SERVICE_DISABLED, ET.tostring(child).decode("utf-8"), SERVICE_DISABLED)
            parent.remove(child)
            parent.append(ET.Comment(commented))
            content=ET.tostring(root, encoding='utf8', method='xml')

      #change state on addon.xml
      savefile(addon_xml_path,content)

      #refresh the list
      xbmc.executebuiltin("Container.Refresh")

def openfile(path_to_the_file):
    try:
        fh = xbmcvfs.File(path_to_the_file, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print("Wont open: %s" % filename)
        return None

def savefile(path_to_the_file,content):
    try:
        fh = xbmcvfs.File(path_to_the_file, 'wb')
        fh.write(content)
        fh.close()
    except: print("Wont save: %s" % filename)

def addDir(name,path,mode,iconimage):
      listItem = xbmcgui.ListItem(label=name)
      listItem.setArt({'icon': "DefaultFolder.png"})
      listItem.setArt({'thumb': iconimage})
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url="%s?path=%s&mode=%s&name=%s" % (sys.argv[0],urllib.parse.quote_plus(path),mode,urllib.parse.quote_plus(name)),listitem=listItem,isFolder=False)

def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                  params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]
      return param

def translate(text):
      return xbmcaddon.Addon().getLocalizedString(text)

params=get_params()
path=None
name=None
mode=None

try: path=urllib.parse.unquote_plus(params["path"])
except: pass
try: name=urllib.parse.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

if mode==None: list_addons()
elif mode==1: change_state(name,path)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
