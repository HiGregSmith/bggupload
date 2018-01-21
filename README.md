# bggupload - BGG Interactive Upload Tool 

>This is experimental software in an Alpha release. Expect problems and difficulties at this point. The developer is seeking problem reports via https://github.com/HiGregSmith/bggupload/issues

bggupload is a GUI interface for creating a collection CSV (particularly for interactively finding the BGGID) for updating your boardgamegeek.com collection.

Update your boardgamegeek.com collection using this GUI interface.

Manually enter search terms one at a time. Double click an image to put the desired item into the output file. The row of images representing a single search will then disappear.

Currently, this creates a CSV file for use with BGGCLI program. This program helps you interactively find the BGGID from a partial name, including manual term search and order confirmation emails from coolstuffinc.com and miniaturemarket.com.

 
Import board games from order confirmation email, csv file, or search input.

Each input row eventually makes its way into the output file.
If the row has a 'id', it is placed directly in the output file, if the row does not have a 'id' and does have an 'objectname', the objectname is used as a term search for manual selection.

Each row of images in the GUI represents an individual search. Select the one item per row that corresponds to the desired choice. Use the mouse and single click to navigate and browse. Double click to put the desired item into the output file.