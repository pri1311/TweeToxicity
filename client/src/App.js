import './App.css';
import React from 'react'
import Main from './components/Search'

const App = () => (
  <div>
    <h1>TweeToxicity</h1>
    <p>Analyze Twitter profile using Sentiment Analysis/Opinion Mining</p>
    <p>
      The Flask server sends a request to the Firestore Database, which retrieves all of the applications, and then uses 
      BoW and TF-IDF for vectorization and cosines similarity for comparison to provide a percentage-wise list of likely applicants. 
      This App is built using React, and is therefore responsive across devices.</p>
    <Main />
  </div>
);
export default App;