import React, { useState,useContext } from 'react'
import { useHistory } from "react-router-dom"
import axios from 'axios'
import styles from "Post.module.css"
import {useForm} from "react-hook-form"
import {useSetData,useSetPosition,DataContext} from "../context/dataContext"

const Post:React.FC = () => {
    const data=useContext(DataContext).data
    const position=useContext(DataContext).position
    const setData=useSetData()
    const setPosition=useSetPosition()

    const [addresses,setAddresses] = useState<string[]>([])

    const {register,handleSubmit,formState:{errors}} =useForm()

    const addAddress=()=>{
        const c=addresses.slice()
        c.push(`${addresses.length}`)
    }
    
    const removeAddress=()=>{
        const c=addresses.slice()
        addresses.shift()
        setAddresses(c)
    }

    let p={userLat:0,userLon:0}

    const getPlacePosition =(place)=>{
        const res=axios.get("https://maps.googleapis.com/maps/api/geocode/json",{params:{address:place,sensor:false,key:"AIzaSyBTURd9DRDiXn1Dff7FGMjUtQZSWZOjhu8"}})
        .then((res)=>{
                setPosition({
                    userLat:res.data.lat,
                    userLon:res.data.lon
                })
                p=({userLat:res.data.lat,userLon:res.data.lon})
            }
            )
            .catch((err)=>{alert("エラー発生")})
            console.log(res)
            return(p)
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
            setPosition({
                userLat:startPos.coords.latitude,
                userLon:startPos.coords.longitude
            });
        }
        const geoError = function(error) {
            switch(error.code) {
                case error.TIMEOUT:
                showNudgeBanner();
                break;
            }
        };
        navigator.geolocation.getCurrentPosition(geoSuccess,geoError);
        return({userLat:startPos.coords.latitude,userLon:startPos.coords.longitude})
    }

    const onSubmit = async (e) =>{
        e.preventDefault()
        if(e.place){   //場所を入力していればlat,lonをapiで取りに行く
            p=await getPlacePosition(e.place)
        }else{         // 入力してない場合、位置情報を取得する
            p=await getPosition()
        }
        const submitData = new FormData()
        addresses.map((address,index)=>{            //複数検索出来る
                submitData.append("productName", e.address)
        })
        submitData.append("productName",`${p.userLat}`)      
        submitData.append("productName",`${p.userLon}`)
        await axios.post("/search", submitData)
        .then((response)=>{
            console.log(response)
            const data=response.data
            setData(
                response.data.map(()=>{{
                dealer:data.dealer;
                name:data.name;
                price:data.price;
                lat:data.lat;
                lon:data.lon;
                }})
            )
        })
        .catch((error) => { alert("通信できませんでした") })
    }
    return ( 
        <div className="styles.post">
            <div className="styles.post-wrapper">
                <form className="styles.post-form" onSubmit = { handleSubmit(onSubmit) } >
                    <label>現在地
                        <input {...register("place")} />
                    </label>
                    {addresses.map((address)=>{
                        <label>商品名
                            <input {...register(`${address}`,{ required: true, maxLength: 30 })} />
                        </label>
                    })}
                    {errors.name && errors.name.type === "required" && <span>This is required</span>}
                    {errors.name && errors.name.type === "maxLength" && <span>Max length exceeded</span> }  
                    <button className="styles.post-button" >検索 </button> 
                </form> 
                    <a onClick={addAddress}>+</a>
                    <a onClick={removeAddress}>-</a>
            </div>
        </div>
    )
}

export default Post