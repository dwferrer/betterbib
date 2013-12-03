#!/usr/bin/python


import requests
import sys

def adsFind(key):
    keyparts = key.split(":")
    title = ""
    authors = ""
    for part in keyparts[:-1]:
        if "t=" in part: title=part.replace("t=","")
        else:
            if not authors: part = "^"+part
            authors = authors +part.replace("+",", ")+"\r\n"

    #authors = authors.replace('^','%5E')
    authors = authors.encode('ascii', 'xmlcharrefreplace')
    title = title.encode('ascii','xmlcharrefreplace')
    date = keyparts[-1]
    params={"author":authors,"start_year":date,"end_year":date,"title":title,"data_type":"BIBTEX","sort":"SCORE","min_score":"0.7","aut_wt":"1.0","obj_wt":"1.0","ttl_wt":"0.7","txt_wt":"3.0","aut_wgt":"YES","obj_wgt":"YES","ttl_wgt":"YES","txt_wgt":"YES","ttl_sco":"YES","txt_sco":"YES","aut_logic":"AND","ttl_logic":"AND","nr_to_return":"10"}

    req = requests.get("http://adsabs.harvard.edu/cgi-bin/nph-abs_connect",params=params)
    #print req.url
    bibitems = req.text

    bibitems = "".join(bibitems.splitlines(True)[4:])
    return bibitems



if __name__ == '__main__':
    print adsFind(sys.argv[1])
