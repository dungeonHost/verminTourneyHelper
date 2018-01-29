VERMIN TOURNEY HELPER:

made with python v. 3.6.4

includes python-opencv, pillow, glob, tkinter and psutil

This project is a real piece of shit, expect it to work ~70% of the time

It will

solve the problem of croping individual vermin from the postrush, having to create/update the tourneys bracket, and save/update a file containing each vermins name, the path to their png image, and their stats (the user has to enter this)

randomly select how ever many vermin from all vermin in a post rush

automatically extract and crop vermin/blast/other sprites and save them as seperate images

save the vermins names, stats, tourney progress, team names and image filenames in 3 csv files (bracketData.csv, metaBracketData.csv, teamNames.csv)

create and populate an image of the tourney bracket   

allow the user to enter in team names and update the bracket with team names

allow the user to pick the winner(s) from a bout and will automatically update 

the bracket with the winner advancing

INSTRUCTIONS:


Starting up a tournamnet:

1. download all vermin images from the postrush as .pngs and save them in a new directory(make sure that the only .pngs in this directory are vermin)

2. git clone the vermintourneyhelper folder into this directory

3. double click verminTourneyHelper.exe and select "start tourney"

4. follow instructions to enter in the size of the tourney 

(i.e. for a 16 3v3 min tourney 
	#rounds=4
	#teams per round=2
	#vermin per team=3)
 #min in tourney=#min per team*#teams per round^#rounds

BE CAREFULL: the brackets image size scales exponentially with tourney size. Any tournament with more than 7 rounds (4 rounds for a XvXvX tourney) will result in the program crashing

5. Wait for a second then the first vermins image* and a popup window showing a bunch of bullshit will appear

	5a. Follow instructions on the popup window and click the image the first stages primary image and another window will open (the one that has an offwhite background [same color as the popup window] has a transparent background/is the better option, this is usually the second option)

	5b. Enter in this stages's name and stats then hit enter

	5c. do this for each of the stages (if each stage is not unique you can click the same image twice)

	5d. after each stage has been entered then choose the blast sprites for each stage (if all stages share the same blast just pick it multiple times)

	5e. then click on any extra sprites (any sprite that is not the primary vermin body or its primary blast) that you want to save

	5f. hit the "none" button to finish picking images

6. repeat step 5 until all vermin have been entered

* if the complete vermin image does not open then you'll need to change the program in code\autocrop.py line 56 to your PCs default image display program, then run the python code verminTourneyHelper.py (you'll need to  download python 3.6.4 and pip install any missing libraries)

* I have no idea why the colors are messed up, the final image is in the appropriate colors

Update a tournament with team names:

1. double click verminTourneyHelper.exe choose "Add team names" from the popup window

2. a popup window will open showing the team that needs a name, type in their name and hit enter

3. repeat step 2 for each team in the tournament

* longer team names (>28 characters) may obscure the team below, try not to make team names too long

Update the tournament after a bout:

1. double click verminTourneyHelper.exe choose "Add team names" from the popup window

2. hit the winning vermin/teams image

