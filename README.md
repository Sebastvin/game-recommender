# Game recommendation system with analysis of key words using flask and ML.


[<img align="left" alt="p1" width="26px" style="margin-left:.6em" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/flask.svg"/>][flask]
[<img align="left" alt="p2" width="26px" style="margin-left:.6em" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/python.svg"/>][python]
[<img align="left" alt="p3" width="26px" style="margin-left:.6em" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/scikit-learn.svg"/>][scikit-learn]
[<img align="left" alt="p4" width="26px" style="margin-left:.6em" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/heroku.svg"/>][heroku]
[<img align="left" alt="p5" width="26px" style="margin-left:.6em" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/pandas.svg"/>][pandas]

<br />
<br />

The game recommendation system recommends games that have the most similar keywords, starting with title, platform, game genre, developer and description.

The entire database(title, genre, score, description, etc) was scraped from metacritic (https://www.metacritic.com/browse/games/score/metascore/all/all/filtered to be exact from this subpage) using `beautifulsoup4`.

# Note

## The Game Recommendation system

The images were also scraped by searching for the game title on google images and downloading the first 3 records.
They are stored on a separate server and are downloaded via a link that has been corrected for the game title. Some image resolutions may be in poorer quality.
A dataset is modified and added to another one (scraping was done in two rounds) which is the final dataset. On it the merging of keywords takes place, which are subjected to sentiment analysis.

<br />

Link to website: https://game-recommender-engine.herokuapp.com/

## How does the system decide which game to play? [Similarity Score]: 

   How does it decide which item is most similar to the item user likes? Here we use the similarity scores.
   
   It is a numerical value ranges between zero to one which helps to determine how much two items are similar to each other on a scale of zero to one. This similarity score is obtained measuring the similarity between the text details of both of the items. So, similarity score is the measure of similarity between given text details of two items. This can be done by cosine-similarity.
   
## How Cosine Similarity works?
  Cosine similarity measures the similarity between two vectors of an inner product space. It is measured by the cosine of the angle between two vectors and determines whether two vectors are pointing in roughly the same direction. It is often used to measure document similarity in text analysis.
  
  ![image](https://user-images.githubusercontent.com/36665975/70401457-a7530680-1a55-11ea-9158-97d4e8515ca4.png)
<br />
  Formula for calculating Cosine Similarity:
  ![image](https://res.cloudinary.com/dyd911kmh/image/upload/f_auto,q_auto:best/v1590782185/cos_aalkpq.png)

  
Source : [Cosine Similarity](https://www.sciencedirect.com/topics/computer-science/cosine-similarity)

### Sources of the datasets 

The projects were inspired by: 
<br />1.https://github.com/subhamrex/Movie_Recommendation_System_with_Web_App
<br />2.https://www.datacamp.com/community/tutorials/recommender-systems-python
<br />
Some pieces of code have been copied from other sources and are mentioned in the .py files.


Screen from my web-app:

<img src="https://raw.githubusercontent.com/Sebastvin/game-recommender/main/static/image/mywebsite.png" alt="game recommender"/>

[python]: https://www.python.org/downloads/
[heroku]: https://www.heroku.com/
[scikit-learn]: https://scikit-learn.org/
[flask]: https://flask.palletsprojects.com/en/2.0.x/
[pandas]: https://pandas.pydata.org/
