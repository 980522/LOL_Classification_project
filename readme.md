
# Classification: League of Legends

## Introduction:
League of Legends (LOL) is a famous online MOBA game that has lasted for 10 years. 10 players are having a 5 vs 5 competition during every game until one team has destroy another team’s base. During every game, each player chooses a champion, killing minions, monsters, and enemies’ champions to earn golds. Then purchase items to assistant to destroy enemy’s base. Not only the champion user selected are significant, golds, towers, but do the cooperation between teammates contributes significantly to the final result.



## Motivation and introduction of the problem

Every year, LOL worldwide professional competition will be held around the world. Numbers of professional teams fight for their dreams. As the audience, people are significantly expected their favorite team to win. Consequently, many people are willing to develop a method to predict if one team can win during each match. At the same time, since there are many aspect such as gold and kills that may influence during the game, athletes and other LOL players are also interested in how those aspects affect the result of each match.

Consequently, as the main goal of this project, we will focus on the relationship between the amount of golds earned by each five positions (Top, Jungle, Middle, Attack Damage Carry (ADC) and Support) for both blue team (consider as ally) and red team (consider as enemy) and the result of the match. More specifically, we will use different statistical classification models to classify if the blue team in a match will win or lose according to the amount of gold earned by all ten players at the 10th minute, the 20th minute, and finally the 30th minute. And analyses how amounts of gold during each match influence the result of that match.


## Data
The original data are collected from Kaggle (url:https://www.kaggle.com/chuckephron/leagueoflegends#LeagueofLegends.csv), which is distributed by Chuck Ephron.

the original data is ``LeagueofLegends.csv`` and the cleaned data is ``LOL.csv``

## Data Cleanning:
The data is cleaned using Python3, before executing the script, make sure that Pandas is installed

```bash
pip3 install pandas
```

Run the following command to generate new data ``LOL.csv`` in ``DataClean``

```bash
python3 DataClean.py
```

## R program:
The major job including model constructing, selecting, and visuallization is done in R

Make sure following packages are installed (or execute ``install.packages("package name")``):<br>
``MASS
factoextra
klaR
nnet
glmnet
mgcv
car
e1071
rpart
rpart.plot
randomForest
gbm
rlist
``

## File Structures
1. LeagueofLegends.csv: original dataset
2. LOL.csv: cleaned datsset
3. DataCleam.(ipynb/py/pdf): script for data cleanning
4. final_draft.(rmd/pdf): R markdown for classification (major job)
5. Report.pdf: final report
6. readme.md: self

## Work distribution:
Planning, partial body writing, and data selecting: Together<br>
Data Cleanning, intrduction, and conclusion: Lai Wei <br>
R developing: Yizhi Zhang
