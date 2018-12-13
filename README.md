# AI Final Project (ErinHH)
#### Andrew Callahan, MacKenzie Cavanagh, Christopher Clarizio, Kyle Miller and Ethan Williams

## Installation Procedure
Before running the program, make sure you are running the programs in Python 3 and have installed praw, sklearn, and Markovify.    
To install praw:
```
pip install praw
```
To install sklearn:
```
pip install sklearn
```
To install Markovify:
```
pip install markovify
```

## Basic Usage, Running the Program


#### To run the bot:
```
$ python erinhhbot.py -i data/aww.txt -w 1 -s 3
```
The erinhhbot.py file is our bot that reads in data from a .txt file. Use the -i flag to specify the file.    
To add different weights to the data files use the -w flag and to specify the state size, use the flag -s.     
This script will output a sentence created from the Markov chain from the aww.txt file and output it to the command line.     
We have commented out the line of code that directly posts it to reddit to avoid having our bot be blocked by reddit.       
You can find examples of some of our outputs in the good_examples.txt file.     

#### To run the predict_upvotes:
```
$ python predict_upvotes.py 
```
