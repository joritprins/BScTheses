# Everybody a private  search engine


_____

* marx
* 2022-10-31

_______


### Motivation

If you have structured data and get lost and want some overview, you use Excel, or a free spreadsheet program like Google sheets.

If you have a bit more data, and have a smart nephew, you put it into MySQL, the free open relational database engine, which seriously scales.

But if you have raw unstructured text data, where do you go? 

In this project, we "beef up" MySQL so that it can easily proces piles of raw unstructured text data (i.e., most common data formats: mail, pdf, word, markdown, HTML,...), and a search user interface and result page (SERP), of similar quality as we know from Google, LinkedIn, or Marktplaats. 

The high quality *ranking* can be done already by MySQL, asking complex queries too, but the input/output is still too difficult for that smart nephew (and his friends on StackOverflow and YouTube tutorials).


### Use cases

People having a pile of raw unstructured text data? Does that happen?

1. You are a journalist, and sudenly you find boxes of stolen files on your doorstep (or in your inbox).
   * Panama papers, wikileaks, ...
* Your grandmother died, and you need to clean the house in 2 weeks, and do not want or dare to throw any of her papers away, so you scan them all, and then?
* You now have your nth laptop and always downloaded the disk to a flash-drive, and have all that information, but cannot find anythingh back anymore.
* You just bought a small company and need to save its paper archive for tax and god knows what reasons, but have no idea how it is organized.

### Your task(s)

1. Investigate the problem. Is it really a problem? What is solved already?
2. Set your constraints (eg, free, opensource, available on all systems (also with limited RAM, processors), easy,  good userbase, etc....).
3. "Solve" input side. At least for some part.
4. "Solve"  output side.
    * Make your "wish-list" of properties your SERP must have.
        * facets (of course, you are in a DB setting, so have lots of extra information on each document). Compare with LinkedIn, Marktplaats.
        * snippets as rich as on Google, possible richer, as you build a *vertical*
        * ...
5. Evaluate: "how Plug and Play is it?", "How foolproof?", "How fast?", "How friendly?", "How much in line with the literasture, (eg for the SERP what is prescribed in <https://searchuserinterfaces.com/>)".


### Input ideas

1. You need a **document type classifier** telling you what type of document a file is (pdf, html, word,....)
2. You need to **get the text out**
    3. `pandoc` and possibly `pdfplumber`
    4. OCR with `tesseract`
5. Maybe you want to do language detection? Get  other data out of the collection of files to set some parameters for the text-indexer.


### Output ideas

1. Study [the book by Hearst](https://searchuserinterfaces.com/), use it.
2. Re-use known CSS (eg the Google style), so users are on "familiar ground".


### Plug and play

* This is a must. Test it out with serious collections of "piles of documents".
