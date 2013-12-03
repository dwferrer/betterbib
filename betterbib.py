#!/usr/bin/python
import sys
import os
import ads
import pickle
import StringIO
import parse

from pybtex.database.input import bibtex as bibtex_in
from pybtex.database.output import bibtex as bibtex_out


def resolve_key(key,key_map,bib):
    if key in key_map.keys() and key_map[key] and bib.entries.get(key_map[key]):
        #print key
        #print key_map[key]
        return key_map[key]
    else:
        result = "ERROR"
        ads_result = ads.adsFind(key)
        if not ads_result.strip():
            print "No Result for: " + key
            raise ValueError
        rst = StringIO.StringIO(ads_result)
        bp = bibtex_in.Parser()
        try:
            ads_items = bp.parse_stream(rst)
            if len(ads_items.entries) ==1:
                key_map[key] = ads_items.entries.keys()[0]
                result = key_map[key]
                if not result: raise ValueError
                if not bib.entries.get(result): bib.add_entry(result,ads_items.entries[result])
                return result
            elif len(ads_items.entries) <11 and len(ads_items.entries) >0:
                print("Multiple items matched for " + key)
                print("Please select one to continue:")
                i = 0
                for bibkey in ads_items.entries.keys():
                    print ("[{:d}]: {!s}  \"{!s}\" ,{!s} ({!s})".format(i,ads_items.entries[bibkey].fields["author"],
                            ads_items.entries[bibkey].fields["title"],ads_items.entries[bibkey].fields["year"],ads_items.entries[bibkey].fields.get("journal","")))
                    i+=1
                ans = int(raw_input("Choice: "))
                if ans <0 or ans > 10: raise ValueError
                key_map[key] = ads_items.entries.keys()[ans]
                result = key_map[key]
                if not result: raise ValueError
                if not bib.entries.get(result): bib.add_entry(result,ads_items.entries[result])
                return result
            else:
                print("A problem occured: " + key + " : "+ ads_result)
                raise ValueError

        except:
            print("An error occurred looking up ("+key+"). Check and try again.")
            raise


def getKeys(auxfile,key_map,bib):
    f = open(auxfile,"r")
    cites = parse.findall("\citation{{{}}}",f.read())
    f.close()
    keys = [s for c in cites for s in c[0].split(",")]
    remap = {}
    for key in keys:
        if ":" in key:
            result = resolve_key(key,key_map,bib)
            remap[key] = result
            #print key+ " : " + result
    return remap

def remapKeys(texfile,remap):
    f = open(texfile,"r")
    text = f.read()
    for key in remap.keys():
        if not remap[key]: raise ValueError("Empty Entry: " + key +" : "+ remap[key])
        text = text.replace(key,remap[key])
    fout = open(texfile.replace(".tex",".out.tex"),"wb")
    fout.write(text)
    return


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print ("Usage: ./betterbib [bibfile] [texfile] [auxfile]")
        sys.exit(1)
    bibfile = sys.argv[1]
    resolved_keys = {}
    if os.path.exists(bibfile + ".bb"):
       resolved_keys = pickle.load(open(bibfile+".bb","rb"))
    #for key in resolved_keys.keys():
    #    print key, resolved_keys[key]
    bp_main = bibtex_in.Parser()
    bib = bp_main.parse_file(bibfile)
    try:
        print ("Input file: " + sys.argv[2])
        remap = getKeys(sys.argv[3],resolved_keys,bib)
        print ("Writing file: " + sys.argv[2].replace(".tex",".out.tex"))
        remapKeys(sys.argv[2],remap)
    finally:
        print ("Exiting")
        bw = bibtex_out.Writer()
        bw.write_file(bib,bibfile)
        pickle.dump(resolved_keys,open(bibfile+".bb","wb"))





