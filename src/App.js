import React, { useState, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  return (
    <div className="App">
      <header className="App-header">
      <div>
        <img src={require("./logo.png")} className="App-logo" alt="logo" />
        <p></p>
        <p></p>
        </div>
        <div>
        <p>
        Welcome to the Reddit Word ☁️ visualizer! 
        </p>
        </div>
        <div>
        <p>
        Please type in a subreddit [ex: ucla]
        and submit to visualize the most popular words in a given community. 
        </p>
        </div>
        <div>
        <p>
        </p>
        <form action="http://127.0.0.1:5000/result" method="get">
        <code> reddit.com/r/ </code>
        <div>
        <input style = {{height: 22}} type="text" name="subreddit"/>
        <input style = {{height: 28}} type="submit" value="Submit"/>
        </div>
        </form>
        </div>
       
      </header>
    </div>
  );
}

export default App;
