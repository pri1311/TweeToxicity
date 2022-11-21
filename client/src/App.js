import './App.css';
import React from 'react'
import Main from './components/Search'

const App = () => (
  <div>
    <h1>TweeToxicity</h1>
    <p>Analyze Twitter profile using Sentiment Analysis/Opinion Mining</p>
    <p>
      The Flask server uses Twitter API to get latest tweets on a particular hashtag or get tweets from a particular profile. We then perform various pre-processing tasks on them and predict the sentiment associated with profile/tweet/hashtag from models pretrained on sentiment140 dataset - a dataset of 1.6 million tweets.
      This App is built using React, and is therefore responsive across devices.</p>
    <Main />
  </div>
);
export default App;