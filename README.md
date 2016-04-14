betterbib
=========

A set of scripts for managing bibtex references to papers on the ADS.

The ADS is already capable of providing references in BibTEX format. Unfortunately, its default keys are not easy to remember or search for. Betterbib will allow you to use keys like

\cite{author1:another,"author I.":t=titleword:date}

It will try to indentify a matching paper on ADS and add it to a bibtex file for you. The citation key you used will then be associated with that ADS entry so that any future uses of it will point to the given paper. 

Let's say we want to cite the paper Sunyaev, R. A., & Zeldovich, Y. B. 1970, Ap&SS, 7, 20. I remember this paper as "Sunyaev and Zeldovich 1970", so when I cite it in latex I write

\cite{sunyaev:zeldovich:1970} (1)

This is easy to write and edit. 


Installation:
Download and install (most easily through pip) the following packages:
1.parse
2.pybtex

You can move the two main betterbib scripts, betterbib.py and ads.py, to your python user packages folder. I, however, usually just copy them into the location of my tex document. This makes it easy to invoke them from a makefile.


When making the latex document, take  the following steps (bibfile.bib is a pre-existing bib file--create an empty one if you don't have one yet):

1. Run latex on file to generate aux file

2. Run betterbib.py input.tex bibfile.bib input.tex input.aux

3. Choose which entry actually matches the paper you want if multiple matches are found.

4. This produces a file input.out.tex with all instances of (1) replaced with the ads bib key

\cite{1970Ap&SS...7....3S}

5. Run latex on the output texfile.


This is of course easily added to your latex makefile if you use one. An example is included. If you use it on your tex file named thesis.tex, it will output the final version as thesis.out.tex, which you can rename as desired.
