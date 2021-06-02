import React, { useState } from 'react'
import { useHistory } from "react-router-dom"
import axios from 'axios'
import styles from "Post.module.css"
import {DATA,SETDATA} from "../app"
import {useForm} from "react-hook-form"
import {useSetData} from "../context/dataContext"

const Post:React.FC<DATA&SETDATA> = ({data,setdata}) => {
    const [addresses,setAddresses] = useState<string[]>([])

    const {register,handleSubmit} =useForm()

    const addAddress=()=>{
        addresses.push(`${addresses.length}`)
    }
    const removeAddress=()=>{
        addresses.shift()
    }

    const getPlacePosition =(place)=>{
        const res=axios.get("https://www.geocoding.jp/api/",{params:{q:place}})
        .then((res)=>
        setdata({...data,
            userLat:res.data.lat,
            userLon:res.data.lon
        })
        )
        .catch((err)=>{alert("エラー発生")})
        console.log(res)
    }

    //位置情報で検索する場合
    const getPosition=()=>{
        let startPos;      
        const showNudgeBanner = function() {
          //位置情報がoffの場合の処理
        };
        const hideNudgeBanner = function() {
            //位置情報がonの場合の処理
        };
        const nudgeTimeoutId = setTimeout(showNudgeBanner, 5000);
      
        const geoSuccess = function(position) {
          hideNudgeBanner();
          clearTimeout(nudgeTimeoutId); 
          startPos = position;
          setdata({...data,
            userLat:startPos.coords.latitude,
            userLon:startPos.coords.longitude
          })
        };
        const geoError = function(error) {
          switch(error.code) {
            case error.TIMEOUT:
              showNudgeBanner();
              break;
          }
        };
        navigator.geolocation.getCurrentPosition(geoSuccess,geoError);
    }

    const set=useSetData()

    const onSubmit = async (e) =>{
        e.preventDefault()
        if(e.place){
            await getPlacePosition(e.place)
        }else{
            await getPosition()
        }
        const submitData = new FormData()
        addresses.map((address)=>{
            submitData.append("productName", e.address+name)
        })
        submitData.append("productName",`${data.userLat}`)
        submitData.append("productName",`${data.userLon}`)
        await axios.post("/search", submitData)
        .then((response)=>{
            console.log(response)
            const data=response.data
            setdata({...data,
                dealer:data.dealer,
                name:data.name,
                price:data.price,
                lat:data.lat,
                lon:data.lon
            })
        })
        .catch((error) => { alert("通信できませんでした") })
    }
    return ( 
        <div className="styles.post">
            <div className="stlyes.post-wrapper">
                <form className="styles.post-form" onSubmit = { handleSubmit(onSubmit) } >
                    <label>現在地
                        <input {...register("place")} />
                    </label>
                    {addresses.map((address)=>{
                        <label>商品名
                            <input {...register(`${address}name`)} />
                        </label>
                    })}
                    <button className="styles.post-button" >検索 </button> 
                </form> 
                    <a onClick={addAddress}>+</a>
                    <a onClick={removeAddress}>-</a>
            </div>
        </div>
    )
}

export default Post