import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import Post from "./components/Post"
import Result from "./components/Result"

//引数として渡すTYPEの指定
export type DATA={
  data:{
      dealer:string,
      name:string,
      price:number,
      userLat:number,
      userLon:number,
      lat:number,
      lon:number
  }
}
export type SETDATA={
  setdata:React.Dispatch<React.SetStateAction<{
    dealer: string;
    name: string;
    price: number;
    userLat: number;
    userLon: number;
    lat: number;
    lon: number;
}>>
}

const App:React.FC = () => {
    const [data,setData]=useState({dealer:"",name:"",price:0,userLat:0, userLon:0,lat:0,lon:0})
    return ( 
        <div className="container">
            <Post data={data} setdata={setData}/>
            {data.name&&<Result data={data} />}
        </div>
    )
}

ReactDOM.render(  
    <React.StrictMode >
        <App/>
    </React.StrictMode>, document.getElementById('output')
);