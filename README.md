# english-broadside-ballad
Parse data from the English Broadside Ballad Archive [(EBBA)](https://ebba.english.ucsb.edu) to create .csv file of ballad metadata

As far as I know, there doesn't seem to be metadata on ballads from EBBA in a tabular format. Having information on ballads, e.g. Title, Year etc. in tabular format makes it much more accessible to researchers because they can analyse it in software like MS Excel.

The EBBA website states that ballad metadata can be accessed via a .xml file download of search results. When looking at the .xml file, I couldn't work out how to differentiate between different tags with the same names, apparently coding different information. Also, there were missing tags - some ballads didn't have their title coded in the .xml but when checking the corresponding 'citation' webpage for the ballad, a title was listed. For this reason, although the .xml file contains more information about the digitisation of the ballad and attributions for that work, I've focused on extracting the information about ballads found on the 'citation' page for each ballad.

We still need the .xml file to get a url for each ballad's citation page, though.

 The homepage states that there are 9575 ballads, but I haven't been able to return this number via the search field. I tried a wild card '*' in the Title and Full Text fields but this searched for the literal '*'. The most results I've been able to return are 9559, achieved by searching ' ' (a space) in the 'Title' field.

On the search results page, click '[View Results as MarcXML]'. There's a download link provided, which didn't download the full .xml file for me. I selected all the xml displayed on the webpage and saved it to a .xml file in a text editor. The xml is not all valid, there were some '&' that were not writting out as '&amp;', but finding and replacing these fixed it. You'll also need to remove the first few and last lines of the xml which aren't part of the xml.

The URL for each ballad is found in this part of the xml:

```xml
<datafield tag="856" ind1="4" ind2="0">
	<subfield code="u">http://ebba.english.ucsb.edu/ballad/20001/</subfield>
	<subfield code="z">English Broadside Ballad Archive.</subfield>
```

For each ballad, I parsed this url field into a list of urls, adding the word 'citation' onto the end to produce a url to the citation page. E.g. http://ebba.english.ucsb.edu/ballad/20001/citation

Here's an example of the citation page for a ballad:
![EBBA citation page sample](citation_page_sample.png "EBBA citation page sample")

I then scraped the data in the table on the citation page. I combined each ballad's citation table into a table of all ballads. I outputting this as a .csv file, which can be opened in MS Excel etc.

|ballad_id|**Date Published**|**Author**|**Standard Tune**|**Imprint**|**License**|**Collection**|**Page**|**Location**|**Shelfmark**|**ESTC ID**|**Keyword Categories**|**Pepys Categories**|**MARC Record**| |**Title**|**Tune Imprint**|**First Lines**|**Refrain**|**Album Page**|**Condition**|**Ornament**|**url**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
20001|1610||[unknown]|At London printed for William Barley, and are / to be sould at his shop in Gratious Streete / 1610.||Magdalene College - Pepys|1.112|Pepys Library|Pepys Ballads 1.112|S126165|country / nation\|death\|news\|punishment\|royalty|Tragedy|Click to View MARC-XML|Part 1|The lamentabe complaint of Fraunce, for the death of the late King Henry the 4. who was lately murdred by one \/ Fraunces Rauilacke, borne in the towne of Angollem, shewing the manner of his death, and of the election and Proclayming of the new King, Lewis / the 13. of that name, being a childe of 9. yeeres of age.|To a new tune|FRaunce that is so famous, \/ and late in ioyes abounded,||single sheet folio, folded, ?365 x 250|cropped right edge, creased and holed, damaged surface, uneven inking|vertical rules|http://ebba.english.ucsb.edu/ballad/20001/citation|

If ballads have more than one part, then the information on each part is separated by a pipe '|' in the relevant field. E.g. `Title` - 'title of first part|title of second part'. I've done the same for fields with mutliple values, e.g. the `Keyword Categories` field.

