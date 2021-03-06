import requests
import re
from common.colors import run,W,end,good,bad,que,info
from common.vxrequest import getrequest as vulnxget
wp_contentdorks = {
        'blaze'             : 'inurl:"/wp-content/plugins/blaze-slide-show-for-wordpress/"',
        'catpro'            : 'inurl:"/wp-content/plugins/wp-catpro/"',
        'cherry'            : 'inurl:"/wp-content/plugins/cherry-plugin/"',
        'dm'                : 'inurl:"/wp-content/plugins/downloads-manager/"',
        'fromcraft'         : 'inurl:"/wp-content/plugins/formcraft/file-upload/"',
        'synoptic'          : 'inurl:"/wp-content/themes/synoptic/lib/avatarupload"',
        'shop'              : 'inurl:"/wp-content/plugins/wpshop/includes/"',
        'revslider'         : 'inurl "/wp-content/plugins/revslider/"',
        'adsmanager'        : 'inurl:"/wp-content/plugins/simple-ads-manager/"',
        'inboundiomarketing': 'inurl:"/wp-content/plugins/inboundio-marketing/"',
}
wp_admindorks = {
        'wysija'            : 'inurl":/wp-admin/admin-post.php?page=wysija_campaigns"',
        'powerzoomer'       : 'inurl:"/wp-admin/admin.php?page=powerzoomer_manage"',
        'showbiz'           : 'inurl:"/wp-admin/admin-ajax.php"',
}

wpajx = {
        'jobmanager'        : 'inurl:"/jm-ajax/upload_file/"',
}


wpindex = {
        'injection'         : 'inurl:"/index.php/wp-json/wp/"',
}


joomla = {
        'comjce'            : 'inurl":index.php?option=com_jce"',
        'comfabrik'         : 'inurl":index.php?option=com_fabrik"',
        'comjdownloads'     : 'inurl":index.php?option=com_fabrik"',
        'comfoxcontact'     : 'inurl":index.php?option=com_foxcontact"',
}

def getdorksbyname(exploitname):
        if exploitname in wp_contentdorks:
                return wp_contentdorks[exploitname]
        elif exploitname in wp_admindorks:
                return wp_admindorks[exploitname]
        elif exploitname in wpajx:
                return wpajx[exploitname]
        elif exploitname in wpindex:
                return wpindex[exploitname]
        elif exploitname in joomla:
                return joomla[exploitname]
def searchengine(exploitname,headers,timeout,numberpage):
        try :
                print (' %s Searching for %s dork url\n' %(run,exploitname))
                numberpage = numberpage*10
                for np in range(0,numberpage,10):
                        if np==0:
                                print(' %s Page n° 1 ' % (info))
                                googlequery = 'https://www.google.com/search?q='+getdorksbyname(exploitname)
                                print(' %s searching for : %s'% (que,googlequery))
                                res = vulnxget(googlequery,headers,timeout)
                                robot_detected = re.findall(re.compile(r'(Our systems have detected)?(\w+)'),res)
                                if robot_detected:
                                        print(" %s robot detected for verification, so changed you headers" %(bad))
                                        print ('------------------------------------------------')
                                else:
                                        WP_dorksconditions(exploitname,res)
                                        print ('------------------------------------------------')
                        else:
                                print(' %s Page n° %i ' % (info,np/10+1))
                                googlequery = 'https://www.google.com/search?q='+getdorksbyname(exploitname)+'&start='+str(np)
                                print(' %s searching for : %s'% (que,googlequery))
                                res = vulnxget(googlequery,headers,timeout)
                                robot_detected = re.findall(re.compile(r'(Our systems have detected)?(\w+)'),res)
                                if robot_detected:
                                        print(" %s robot detected for verification, so changed you headers" %(bad))
                                        print ('------------------------------------------------')
                                else:
                                        WP_dorksconditions(exploitname,res)
                                        print ('------------------------------------------------')
        except Exception as msg:
                print(' %s exploitname %s ' %(bad,msg))
        np=+10
def WP_dorksconditions(exploitname,response):
        webs = []
        if exploitname in wp_contentdorks:
                dorks = re.findall(re.compile(r'https?://+?\w+?[a-zA-Z0-9-_.]+?[a-zA-Z0-9-_.]?\w+\.\w+/?/wp-content/plugins/\w+'),response)
                if len(dorks) > 0:
                        for web in dorks:
                                if web not in webs:
                                        webs.append(web)
                                        print (' %s urls found : %s ' %(good," \n                  ".join(webs)))
        elif exploitname in wp_admindorks:
                dorks = re.findall(re.compile(r'https?://+?\w+?[a-zA-Z0-9-_.]+?[a-zA-Z0-9-_.]?\w+\.\w+/?/wp-admin/\w+'),response)
                for web in dorks:
                        if web not in webs:
                                webs.append(web)
                                print (' %s urls found : %s ' %(good," \n                  ".join(webs)))
        elif exploitname in wpajx:
                dorks = re.findall(re.compile(r'https?://+?\w+?[a-zA-Z0-9-_.]+?[a-zA-Z0-9-_.]?\w+\.\w+/?/jm-ajax/upload_file/'),response)
                for web in dorks:
                        if web not in webs:
                                webs.append(web)
                                print (' %s urls found : %s ' %(good," \n                  ".join(webs)))
        elif exploitname in wpindex:
                dorks = re.findall(re.compile(r'https?://+?\w+?[a-zA-Z0-9-_.]+?[a-zA-Z0-9-_.]?\w+\.\w+/index.php/wp-json/wp/'),response)
                for web in dorks:
                        if web not in webs:
                                webs.append(web)
                                print (' %s urls found : %s ' %(good," \n           ".join(webs)))
        elif exploitname in joomla:
                dorks = re.findall(re.compile(r'https?://+?\w+?[a-zA-Z0-9-_.]+?[a-zA-Z0-9-_.]?\w+\.\w+/index.php?option=com_jce'),response)
                for web in dorks:
                        if web not in webs:
                                webs.append(web)
                                print (' %s urls found : %s ' %(good," \n           ".join(webs)))
        else:
                print(' %s No URL founds' %(bad))
