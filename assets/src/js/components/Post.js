import React, { useState } from 'react'
import { http } from "./Result"
import { useHistory } from "react-router-dom"

const Post = () => {
    const [name, setName] = useState("")
    const handleChange = (e) => {
        console.log(name)
        setName(e.target.value)
    }
    const handleSubmit = () => {
        console.log(name)
        http.post("/name", { name: name })
            .then(setTimeout(5000000))
            .catch((error) => { alert("postoooooo") })
    }
    return ( <
        >
        <
        form onSubmit = { handleSubmit } >
        <
        input onChange = { handleChange }
        /> <
        button > 登録 < /button> < /
        form > <
        />
    )
}

export default Post