<div id="top"></div>
<br />
<div align="center">

  <h2 align="center">TweeToxicity</h2>

  <p align="center">
    Twitter Profile Sentiment Analyzer 
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents"> :book: Table of Contents</h2>
<details open="open">
  <summary>Table of Contents</summary>
  <ul>
    <li><a href="#about-the-project">  About The Project</a></li>
    <li><a href="#screenshots">  Screenshots</a></li>
    <li><a href="#tech-stack"> Tech Stack</a></li>
    <li><a href="#models">  Models</a></li>
    <li><a href="#run-locally">  Run Locally</a></li>
    <li><a href="#environment-variables">  Environment Variables</a></li>
    <li><a href="#references"> References</a></li>

  </ul>
</details>



![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)    

## About the Project


TweeToxicity is a program that analyzes user profiles or hastags based on the recent tweets. The program utilizes machine learning to give Twitter users an appropriate score according to their tweets or retweets. This program is meant for educational purposes and no ill intetions existed prior to creating this program.


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## Screenshots

![Hashtag Screenshot](https://github.com/pri1311/TweeToxicity/screenshots/hashtag.png)
![User Screenshot](https://github.com/pri1311/TweeToxicity/screenshots/profile.png)

  ![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
## Tech Stack

**Client:**
- [React](https://reactjs.org/)
- [Axios](https://axios-http.com/)
- [ChartJs](https://www.chartjs.org/)

**Server:** 
- [NLTK](https://www.nltk.org/)
- [Sklearn](https://scikit-learn.org/stable/index.html)
- [Tweepy](https://github.com/tweepy/tweepy)
- [Twitter API](https://developer.twitter.com/en)
- [Flask Restful API](https://flask-restful.readthedocs.io/en/latest/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png) 

## Models

> DataSet Used for Training : [Sentiment140](https://www.kaggle.com/kazanova/sentiment140)

<table>
	<tr>
	<th colspan="2">
		Model
	</th>
	<th colspan="2" >
		Training
	</th>
	<th colspan="2" >
		Testing
	</th>
   </tr>
  <tr>
    <th>Name</th>
    <th>Settings</th>
    <th>Accuracy </th>
    <th>F1 Score</th>
    <th>Accuracy</th>
    <th>F1 Score</th>
  </tr>
    <tr>
	  <td rowspan="2" >Logistic Regression </td>
	  <td>Count Vect. & Lemmatization Used</td>
	  <td>79.63%</td>
	  <td>0.8008</td>
	  <td>78.71%</td>
	  <td>0.7929</td>
  </tr>
     <tr>
	  <td>TF-IDF & Lemmatization Used</td>
	  <td>80.31%</td>
	  <td>0.8061</td>
	  <td>78.89%</td>
	  <td>0.7930</td>
  </tr>
  <tr>
	  <td rowspan="2" >Multinomial Naive Bayes </td>
	  <td>Count Vect. & Lemmatization Used</td>
	  <td>78.48%</td>
	  <td>0.7838</td>
	  <td>78.71%</td>
	  <td>0.7756</td>
  </tr>
     <tr>
	  <td>TF-IDF & Lemmatization Used</td>
	  <td>79.81%</td>
	  <td>0.7961</td>
	  <td>76.64%</td>
	  <td>0.7664</td>
  </tr>
  <tr>
	  <td rowspan="2" >Bernoulli Naive Bayes </td>
	  <td>Count Vect. & Lemmatization Used</td>
	  <td>78.53%</td>
	  <td>0.7875</td>
	  <td>77.71%</td>
	  <td>0.7803</td>
  </tr>
     <tr>
	  <td>TF-IDF & Lemmatization Used</td>
	  <td>80.15%</td>
	  <td>0.8052</td>
	  <td>77.68%</td>
	  <td>0.7791</td>
  </tr>
  <tr>
	  <td rowspan="2" >Decision Tree Classifier</td>
	  <td>Count Vect. & Lemmatization Used, Decision Tree Parameters : {max_depth=50}</td>
	  <td>72.91%</td>
	  <td>0.7630</td>
	  <td>69.45%</td>
	  <td>0.7334</td>
  </tr>
     <tr>
	  <td>TF-IDF & Lemmatization Used, Decision Tree Parameters : {max_depth=50}</td>
	  <td>73.66%</td>
	  <td>0.7667</td>
	  <td>69.13%</td>
	  <td>0.7297</td>
  </tr>
  <tr>
	  <td rowspan="2" >Linear Support Vector Machine </td>
	  <td>Count Vect. & Lemmatization Used</td>
	  <td>82.92%</td>
	  <td>0.8309</td>
	  <td>78.38%</td>
	  <td>0.7867</td>
  </tr>
     <tr>
	  <td>TF-IDF & Lemmatization Used</td>
	  <td>80.36%</td>
	  <td>0.8051</td>
	  <td>78.28%</td>
	  <td>0.7733</td>
  </tr>
  <tr>
	  <td rowspan="2" >Random Forest Classifier </td>
	  <td>Count Vect. & Lemmatization Used, Random Forest Parameters : {max_depth=25}</td>
	  <td>74.65%</td>
	  <td>0.7615</td>
	  <td>74.04%</td>
	  <td>0.7566</td>
  </tr>
     <tr>
	  <td>TF-IDF & Lemmatization Used, Random Forest Parameters : {max_depth=25}</td>
	  <td>74.80%</td>
	  <td>0.7619</td>
	  <td>74.00%</td>
	  <td>0.7553</td>
  </tr>
     <tr>
	  <td rowspan="2">Gradient Boosting Classifier </td>
	  <td>TF-IDF { min_df=5 } & Lemmatization Used . Gradient Boosting Parameters : {lr=1.25, n=100, depth=25}</td>
	  <td>74.80%</td>
	  <td>0.7619</td>
	  <td>74.00%</td>
	  <td>0.7553</td>
  </tr>
     <tr>
	  <td>TF-IDF { min_df=5 } & Lemmatization Used . Gradient Boosting Parameters : {lr=1.25, n=100, depth=25}</td>
	  <td>85.99%</td>
	  <td>0.8626</td>
	  <td>77.49%</td>
	  <td>0.7791</td>
  </tr>
  <tr>
	  <td rowspan="2" >XGBoost Classifier </td>
	  <td>Count Vect. & Lemmatization Used</td>
	  <td>75.29%</td>
	  <td>0.7661</td>
	  <td>75.21%</td>
	  <td>0.7662</td>
  </tr>
     <tr>
	  <td>TF-IDF & Lemmatization Used</td>
	  <td>75.39%</td>
	  <td>0.7683</td>
	  <td>75.14%</td>
	  <td>0.7667</td>
  </tr>
</table>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
  
## Run Locally

Clone the project

```bash
  git clone https://github.com/pri1311/TweeToxicity
```

Install dependencies in ```server``` folder.
```bash
  cd server
  python -m venv env
  source env/bin/activate
  pip install -r requirements.txt
```
Generate environment variables and fill in the values.

```bash
  cp .env.example .env
```
>  Your  `.env`  is ignored by  `git`, which you can see in  `.gitignore`, and so, it's safe!

Starting Development Server

```bash
  python server.py
```

Install dependencies in ```client``` folder.

```bash
  cd ../client # If you are in ./server
  npm i
```

Starting Client 

```bash
  npm start
```


At the end of this, you should have

- server running at `http://127.0.0.1:5002/`
- new_client running at `http://localhost:3000/`

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
  
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY : Twitter API/Consumer Key `

`API_KEY_SECRET : Twitter API/Consumer Secret `

`BEARER_TOKEN : Twitter Bearer Token  `

`ACCESS_TOKEN : Twitter Access Token `

`ACCESS_TOKEN_SECRET : Twitter Access Secret `


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## References

 - Pre-Processing :
 	- [Kaggle NLP 101 Preprocessing](https://www.kaggle.com/redwankarimsony/nlp-101-tweet-sentiment-analysis-preprocessing)
 - [Machine-Learning-Projects Repo -> Twitter Sentiment Analysis ](https://github.com/utsavk28/DetectiveDog)
 - [Deploy a machine learning model using flask](https://towardsdatascience.com/deploy-a-machine-learning-model-using-flask-da580f84e60c)
