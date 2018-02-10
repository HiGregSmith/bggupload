# bggupload - BGG Interactive Upload Tool

**The developer is seeking [problem or installation reports via github](https://github.com/HiGregSmith/bggupload/issues).**

### Overview
Update your boardgamegeek.com collection using this GUI interface. This program helps you interactively find the BGGID from a partial name or inexact match. Import by hand, from csv file, or from order confirmation email.

This tool takes input and searches BGG for similar names. You can then double click the desired item to create a single game in the output file.

Each row of images in the GUI represents an individual search. Select the one item per row that corresponds to the desired choice. Use the mouse and single click to navigate and browse. Double click to put the desired item into the output file.

### Output

The output file is in CSV format and the headings are designed for uploading to BGG using BGGCLI program.

> **<div style="background-color:LightGray">Currently, this program creates a CSV file for use with BGGCLI program and does not upload directly.</div>**

### Input

- Input can be from several sources:
    - manual input search term,
    - CSV file,
    - Order confirmation email. Currently supports:
        - coolstuffinc
        - miniaturemarket
        - boardlandia
        

> **<div style="background-color:LightGray">Importing from confirmation email will retain other information in the file such as acquisition date and price paid.</div>**

Importing from a CSV file will allow you to match the named headers in the input file with specified headers in the output file.

### Menu Items & Options
- Menu Items:
    - Remove Selected Row: Remove row without writing to output file.
    - Enter BGGID: Directly enter BGGID and write to output file.
    
    
<div style="background-color:LightGray">

- The following menu items DO NOT WORK:
    - Load>Paste from Clipboard
    - Save>To File
    - Save>To BGG
    - View>Output
    - Edit>Fuzzy Local Search
</div>

>**Default options:** Save To File, Fuzzy Local Search Enabled, View Output.

**Not Tested:** If the row has an 'objectid' (when importing from a CSV file), it is placed directly in the output file
if the row does not have a 'id' and does have an 'objectname', the objectname is used as a term search for manual selection.