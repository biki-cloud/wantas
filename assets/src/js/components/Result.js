import React, { useEffect, useState } from "react";
import axios from "axios"

export const http = axios.create({
    baseURL: 'http://localhost:8080',
})


const Result = () => {
    const [data, setData] = useState({
        name: ""
    })
    useEffect(() => {
        // <script src="/assets/js/go-react.min.js"></script> を起動するとここに来る。
        // http.get("/results")でmain.goの/resultsにアクセスする。帰ってきたのがresponseになる。
        http.get("/name")
            .then((response) => setData(JSON.stringify(response.data)))
            .catch((error) => { alert("データがありません") });
    }, [])
    return ( <
        h1 > { `${data}` } < /h1>
    );
}

export default Result