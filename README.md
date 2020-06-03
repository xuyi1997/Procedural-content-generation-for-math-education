# Procedural-content-generation-for-math-education
This is a master thesis project aiming at explore procedural content generation methods in the field of math education. 
The project is still under implementation.
You can try:
python Menu.py
to get a first insight to the input and output of the generator

### Python Dependencies:
Numpy
tracery
word2vec
xlrd
prettytable
plotly 

You also need to download pre-trained word embeddings and put them in the data folder:
https://drive.google.com/file/d/1tKex-9FpY96DgIz_kSY4hXiKOTDzkh_j/view?usp=sharing
https://drive.google.com/file/d/1QOwfmPMbzNsIV1aV1GSxtCyxcz2Ndbkp/view?usp=sharing


Some functions are still under implementing, now you can input knowledge components ID below to have an insight of the generated content for typical math problems

Calculation Problem:
KC 122:  add and sub under 20
KC 173: Divide under 12
KC 177: multiply under 100
Number Sequence:
KC 23: count and count back up to at least 100 with jumps of 2, 5 (the vijfvouden) and 10.
Ratio:
KC 286: simple relationship problems with a relationship table
Percentage:
KC 309: calculate the discount rate as the old and new prices are known
Table and Chart:
KC 621: organize and view data collection in an appropriate graphic representation (such as a table, line chart, picture, pie or bar chart)
