import React,{useEffect,useContext} from "react";
import axios from "axios"
import styles from "Result.module.css"
import {DataContext} from "../context/dataContext"
import {LoadScript,GoogleMap,Marker} from "@react-google-maps/api"

const containerStyle = {
    width: "400px",
    height: "400px",
  };

const Result:React.FC= () => {
    const data=useContext(DataContext).data
    const position=useContext(DataContext).position
    return (
        <>
        {data.map((datum)=>{

            <table className="table">
                <thead>
                    <tr>
                        <th>店名</th>
                        <th>商品名</th>
                        <th>値段</th>
                        <th>場所</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{`${datum.dealer}`}</td>
                        <td>{`${datum.name}`}</td>
                        <td>{`${datum.price}`}</td>
                        <td>
                            <LoadScript googleMapsApiKey="AIzaSyB_iQKOsqO4b9wcWWd6Y9dxDlgXB1X6I3U">
                            <GoogleMap
                              mapContainerStyle={containerStyle}
                              center={{
                                  lat:position.userLat,
                                  lon:position.userLon
                              }}
                              zoom={17}
                            >
                                <Marker position={{lat:datum.lat,lon:datum.lon}} />
                            </GoogleMap>
                            </LoadScript>
                        </td>
                    </tr>
                </tbody>
            </table>
        })}
        </>
    );
}

export default Result