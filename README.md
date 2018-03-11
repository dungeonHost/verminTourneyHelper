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

7. if your doing a team tournament then a new popup window will open showing you a vermin and asking you to choose its teamate, do this for each team in the tourney

7. When your done you'll have a new folder called bracket that contains all the croped out images, an image of the completed bracket (bracket.png), and 2 csvfiles: bracket.csv (contains filenames, names and stats of each vermin in the tournament) and bracketMetaData.csv (explained below)
	The cropped out images are given the filename of the image they were taken from with a number on the end (0-2 are the stages, 3-5 are each stage's blast, the rest are any extras you needed)

* if the complete vermin image does not open then you'll need to change the program in code\autocrop.py line 56 to your PCs default image display program, then run the python code verminTourneyHelper.py (you'll need to  download python 3.6.4 and pip install any missing libraries)

* I have no idea why the colors are messed up, the final image is in the appropriate colors

* the label is broken, I don't care enough to fix them

Update a tournament with team names:

1. double click verminTourneyHelper.exe choose "Add team names" from the popup window

2. a popup window will open showing the team that needs a name, type in their name and hit enter

3. repeat step 2 for each team in the tournament

4. This will create a new csv file bracket/teamnames.csv that will have the names of each team in the same order as vermin are listed in bracket.csv

* longer team names (>28 characters) may obscure the team below, try not to make team names too long

Update the tournament after a bout:

1. double click verminTourneyHelper.exe choose "Add team names" from the popup window

2. hit the winning vermin/teams image

3. After doing this bracket/bracket.png will be updated with an x next to the team that lost and the winning team moving forward. It will also update BracketMetaData.csv with the winners bracket.csv line number (for teams this number will be the first member in the team)

FILES/IMAGES:

bracket.png:

	The bracket for the tourney, split into 2-4 individual "trees" that meet in the middle

	If you want to you can modify the bracket to add a title/pictures or a loosers bracket, just don't change bracket.png's width or where the trees are located

bracket.csv:

	stage 1 info={stage 1 image filenmane, stage 1 name, stage 1 stats [lifes,muscle,blast,gaurd,fast]},stage 2 info, stage 3 info, filenames for each of the stages's blast, filenmaes for any extra images
	
	* stage filenames = <full Picture filename>0.png, <full Picture filename>1.png, <full Picture filename>2.png
	
bracketMetaData.csv:
	
	line1: team size,number of rounds,number of partisipants (xvx=2, xvxvx=3)
	
	line 2-5: end point for each branch drawn in the bracket, each line represents one "tree" from the bracket (i.e. the right and left trees in a 2 partisipant tourney will have their endpoints stored in line 1 and 2 respectively)
	
	last line: match number, the winner of each matches line number in bracket.csv (the last number is the latest matches winner's number, line number belongs to the first vermin in the team)

teamnames.csv:
	
	contains team names ordered the same way as vermin in bracket.csv (so for a tourney with teamsize of 2 the first name in teamnames.csv belongs to the first two vermin in bracket.csv)


KNOWN PROBLEMS:

	Hitting bracket update will not work for the final match in the tourney (the point at the root of a bracket 'tree' is not saved in bracketMetaData.csv and I'm too lazy to fix all this shit to add it in, just open it in paint)
	
	If a vermin is made of tiny pieces with space inbetween them then they will not be cropped correctly

	If the background of a vermin image is not white or transparent it will not be cropped correctly

	If the vermin/blast is drawn inside of a box, then the box will be cropped out with all the white space intact

	The bracket image (bracket.png) is way bigger than it needs to be for larger tournamnets, anything with over 5 rounds will more than likely cause problems (so don't ask for it)