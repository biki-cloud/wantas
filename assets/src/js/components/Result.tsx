import React, { useEffect, useContext } from "react";
import axios from "axios";
import styles from "./Result.module.css";
import { DataContext } from "../context/dataContext";
import { LoadScript, GoogleMap, Marker } from "@react-google-maps/api";

const containerStyle = {
  width: "200px",
  height: "200px",
};
const Result: React.FC = () => {
  const data = useContext(DataContext).data;
  const position = useContext(DataContext).place;
  const center = {
    lat: position.userLat,
    lng: position.userLon,
  };
  return (
    <div className={styles.result}>
      <div className={styles.wrapper}>
        <table className={styles.table}>
          <tbody>
            <tr className={styles.thead}>
              <th>店名</th>
              <th>商品名</th>
              <th>値段</th>
              <th>場所</th>
            </tr>
            <tr>
              <th className={styles.bar} colSpan={4}></th>
            </tr>
            {data.map((datum, index) => {
              return (
                <tr className={styles.tbody} key={index}>
                  <td>{`${datum.dealer}`}</td>
                  <td>{`${datum.name}`}</td>
                  <td>{`${datum.price}`}</td>
                  <td>{`${datum.lat}`}</td>
                  <td>{`${datum.lon}`}</td>
                  <td>
                    <div>
                      <LoadScript googleMapsApiKey="AIzaSyDzeU7QqfTOkKg58HQujHzTI8jTaOiDfB0">
                        <GoogleMap
                          mapContainerStyle={containerStyle}
                          center={center}
                          zoom={17}
                        >
                          <Marker
                            position={{ lat: datum.lat, lng: datum.lon }}
                          ></Marker>
                        </GoogleMap>
                      </LoadScript>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Result;
