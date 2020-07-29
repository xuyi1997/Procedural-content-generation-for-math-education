# Procedural-content-generation-for-math-education
This is a master thesis project aiming at explore procedural content generation methods in the field of math education. 

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Install](#install)

## Introduction

We designed a pipeline to support content editors & developers to procedurally generate math education content, aiming to help them relieve repetitive work. The generated content is math problem in various knowledge topics with textual question and images.

## Prerequisites

Python 3.7x

## Install

### Step 1: Install python dependencies
To install the dependencies, run this in the application folder from the command-line:
```sh
pip install -r requirements.txt
```

### Step 2: Download vectors and place them in /data

For text generation, we use a small-size pre-trained word embeddings made from the text8 Wikipedia dump, and we already put it in the folder.
You can skip this step to test the generator on this small dataset.
However, if a more accurate natural language generation model is needed, you need to download pre-trained word embeddings made from a larger wiki corpus:
(available at:
https://drive.google.com/file/d/1tKex-9FpY96DgIz_kSY4hXiKOTDzkh_j/view?usp=sharing
https://drive.google.com/file/d/1QOwfmPMbzNsIV1aV1GSxtCyxcz2Ndbkp/view?usp=sharing
)
then put them in the data folder, and modify the following code in file "textGenerator.py" to load the new word embeddings:
```sh
w2v = Embeddings.load("data\\vecs.npy")
```

### Step 3: Run

Now, try:
```sh
python interface.py 
```
(Note: As we use online image retreival API and tranlation tool, it is required to run with internet connection.)


You will see an interface that allow you to choose Knowledge Component and language version. Please choose KC, language version and retreival-or-not option before click the "generate" button.

The first time you click generate, it may takes some time for the system to load the dependencies and word embeddings.
Then you will find the text question, answers and image file directories in the three boxes.

Here are some typical KCs for trial:

Arithmetic Problem:

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
