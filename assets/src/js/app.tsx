import React, { useEffect, useState,useContext } from "react";
import ReactDOM from "react-dom";
import Post from "./components/Post"
import Result from "./components/Result"
import DataProvider,{DataContext} from "./context/dataContext"


const App:React.FC = () => {
    const data=useContext(DataContext)
    return ( 
        <div className="container">
            <Post />
            {data&&<Result />}
        </div>
    )
}

ReactDOM.render(  
    <React.StrictMode >
        <DataProvider>
            <App/>
        </DataProvider>
    </React.StrictMode>, document.getElementById('output')
);