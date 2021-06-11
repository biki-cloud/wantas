import React, { useEffect, useState, useContext } from "react";
import ReactDOM from "react-dom";
import Post from "./components/Post";
import Result from "./components/Result";
import DataProvider, { DataContext } from "./context/dataContext";
import { Grid, CssBaseline } from "@material-ui/core";

const App: React.FC = () => {
  const data = useContext(DataContext).data;
  return (
    <Grid container className="container">
      <Grid item md={4} className="item">
        <Post />
      </Grid>
      <Grid item md={8} className="item">
        {data.name && <Result />}
      </Grid>
    </Grid>
  );
};

ReactDOM.render(
  <React.StrictMode>
    <DataProvider>
      <CssBaseline />
      <App />
    </DataProvider>
  </React.StrictMode>,
  document.getElementById("output")
);
