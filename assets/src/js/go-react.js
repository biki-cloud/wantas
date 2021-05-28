import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import Main from "./components/Main"
import Post from "./components/Post"
import Result from "./components/Result"
import { BrowserRouter as Router, Switch, Route } from "react-router-dom"

const App = () => {
    return ( <
        Post /
        >
    )
}

const app = document.getElementById('output');
ReactDOM.render( <
    React.StrictMode >
    <
    App / >
    <
    /React.StrictMode>, app
);