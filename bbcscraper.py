# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 18:52:08 2021

@author: aa
"""


 # -*- coding: utf-8 -*-
"""gp_bbc6_spl.ipynb
 
Automatically generated by Colaboratory.
 
Original file is located at
    https://colab.research.google.com/drive/1scLHe1pKp5Q8ludBVSyg7d-MjHC8Jj8a
"""
 
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
from tqdm import tqdm
 
linktoallshows="https://www.bbc.co.uk/programmes/b01fm4ss/episodes/guide"
 
base_link_for_shows="https://www.bbc.co.uk/programmes/b01fm4ss/episodes/player"#"https://www.mixesdb.com"
 
def request_page_w_headers(url):
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    response = requests.get(url,headers=headers)#"https://www.bbc.co.uk/programmes/b01jypg2")#"https://www.bbc.co.uk/programmes/m000d193")
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        content = response.content
        print("Found page!")
    return(content)
 
def get_soup(link):
    content=request_page_w_headers(link)#base_link_for_shows)
    soup = BeautifulSoup(content, 'html.parser')
    return soup
 
def get_show_links(link=base_link_for_shows):
    soup=get_soup(link)
    showlinks=[]
    for link in soup.find_all('a'):
        foundlink=link.get('href')
        if foundlink is not None:
            if "uk/programmes" in foundlink:
                print(foundlink)
            elif 'sounds/play' in foundlink:
                print(foundlink)
                showlinks.append(foundlink)
                
    return showlinks
 
#content=request_page_w_headers(showlinks[3])
#soupshow = BeautifulSoup(content, 'html.parser')
 
def get_df_with_show_listing(showlink):
    soupshow=get_soup(showlink)
    
    for i in soupshow.find_all("script"):
        
        if i.get_text()[:9]==" window._":
            #print(i.prettify())
            #print(i.get_text().split("__ = ")[1][-3:])
            print('getting playlist')
            js=json.loads(i.get_text().split("__ = ")[1][:-2])
    
    dfurisc=pd.DataFrame([x["uris"] for x in js["modules"]["data"][1]["data"]],columns=["spotify","itunes"])#["uris"])#[4]
    
    dfurisc["sp_uri"]=None
    
    dfurisc["sp_uri"]=dfurisc.loc[(dfurisc.spotify.isna()==False),("spotify")].apply(lambda x: x["uri"],)
    
    dfshow=pd.concat([pd.json_normalize(pd.DataFrame(js["modules"]["data"][1]["data"])["titles"]),dfurisc,], axis=1)
    
    dfshow["showtitle"]=soupshow.title.get_text()
    return dfshow
 
#dfshow.to_csv("/content/drive/My Drive/python/show4.csv")
 
#!ls
 
#from google.colab import drive
#drive.mount('/content/drive')
class playlistInfo:
    #species = "Canis familiaris"
 
    def __init__(self, showlink):#, date, title, playlist, synopsis):
        self.showlink = showlink
        #self.date = date
        #self.title = title
        #self.playlist = playlist
        #self.synopsis = synopsis
 
    # 
    def title(self):
        return extract_playlist_and_show_info(self.showlink)[0]
    # 
    def date(self):
        return extract_playlist_and_show_info(self.showlink)[1]
    # 
    def playlist(self):
        return extract_playlist_and_show_info(self.showlink)[2]
    # 
    def synopsis(self):
        return extract_playlist_and_show_info(self.showlink)[3]
    
    # Instance method
    #def description(self):
    #    return f"{self.name} is {self.age} years old"
 
    # Another instance method
    #def speak(self, sound):
    #    return f"{self.name} says {sound}"
 
 
def extract_playlist_and_show_info(link):
        
    soup1=get_soup(link)#"https://www.bbc.co.uk/programmes/m000rm7m")
    date=soup1.find_all("div", {"class": "broadcast-event__time beta"})[0]["content"]
    titleofshow=soup1.title.text
    playlist=[]
    #synopsis_long= " ".join(["".join(x.text.strip()) for x in soup1.find_all("div", {"class":"synopsis-toggle__long"})[0].find_all("p")])
    for i in soup1.find_all("div", {"class": "segment__track"}):
        if i!=[]:
            track=(i.text.strip().split("\n\n\n"))
        
            if (len(track))==1:
                #print("artist: {}".format(track[0]))
                playlist.append({"artist":" ".join((track[0].strip()).split()),"title":None, "label":None})
        
            elif (len(track))==2:
                #print("artist: {}, title: {}".format(track[0], track[1]))
                playlist.append({"artist":" ".join((track[0].strip()).split()),"title":" ".join((track[1].strip()).split()), "label":None})
            else:
                #print("artist: {}, title: {}, label: {}".format(track[0].strip(), track[1].strip(), track[2].strip()))
                playlist.append({"artist":" ".join((track[0].strip()).split()),"title":" ".join((track[1].strip()).split()), "label":track[2].strip()[:-1]})
            
            
    df_pl=pd.DataFrame(playlist)
    
    return titleofshow,date,df_pl#,synopsis_long
 
 
 
class playlistInfo2:
   
    def __init__(self, showlink):#, date, title, playlist, synopsis):
        self.showlink = showlink
        
        #self.date = date
        title, date, playlist = extract_playlist_and_show_info(self.showlink)#[0]
        self.title = title
        self.playlist = playlist
        self.date = date
        #self.synopsis = synopsis
 
    # 
    #def mtitle(self):
    #    self.title = title == extract_playlist_and_show_info(self.showlink)[0]
    # 
    #def date(self):
    #    return extract_playlist_and_show_info(self.showlink)[1]
    # 
    #def playlist(self):
    #    return extract_playlist_and_show_info(self.showlink)[2]
    # 
    #def synopsis(self):
    #    return 
#soup2.find_all("li", {"class":"pagination__page pagination__page--offset14 pagination__page--last"})
def all_gp_ww_shows_in_df(linktoallshows=linktoallshows): 
    show_access=[]
    soup2=get_soup(linktoallshows)
    lastpage=soup2.find_all("li", {"class":"pagination__page pagination__page--offset14 pagination__page--last"})[0].text.strip()
    
    for page in range(1,int(lastpage)+1):
        print(page)
        next_page=linktoallshows+"?page="+str(page)
        soup2=get_soup(next_page)
        
        for p in soup2.find_all("div", {"class": "programme__body"}):
            if p.find_all("a") != []:
                link_to_show=p.find_all("a")[0]["href"]
                titleshow=p.find_all("a")[0].text
                shortsynopsis=p.find_all("p")[0].text.strip()
                show_access.append({"link":link_to_show, "title":titleshow,"shortsynopsis":shortsynopsis})
            
    df_access_to_all_shows=pd.DataFrame(show_access)
    return df_access_to_all_shows
 
linktoallshows="https://www.bbc.co.uk/programmes/b01fm4ss/episodes/guide"
 
#for i in tqdm(df_access_to_all_shows.link.values):
#    print(extract_playlist_and_show_info(i))