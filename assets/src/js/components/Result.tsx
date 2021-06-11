import React, { useEffect, useContext } from "react";
import axios from "axios";
import styles from "./Result.module.css";
import { DataContext } from "../context/dataContext";
import { LoadScript, GoogleMap, Marker } from "@react-google-maps/api";

const containerStyle = {
  width: "200px",
  height: "200px",
};

const center = {
  lat: 33.2488525,
  lng: 129.6930912,
};

const point = {
  lat: 33.2488525,
  lng: 129.6930912,
};

const Result: React.FC = () => {
  const data = useContext(DataContext).data;
  const position = useContext(DataContext).place;
  return (
    <div className={styles.result}>
      <div className={styles.wrapper}>
        {/*data.map((datum) => {
          <table className={styles.table}>
            <tbody>
              <tr className={styles.thead}>
                <th>店名</th>
                <th>商品名</th>
                <th>値段</th>
                <th>場所</th>
              </tr>


              <tr>
                <td className={styles.bar} colSpan={4}></td>
              </tr>
              <tr className={styles.tbody}>
                <td>{`${datum.dealer}`}</td>
                <td>{`${datum.name}`}</td>
                <td>{`${datum.price}`}</td>
                <td>
                  <LoadScript googleMapsApiKey="AIzaSyDzeU7QqfTOkKg58HQujHzTI8jTaOiDfB0">
                    <GoogleMap
                      mapContainerStyle={containerStyle}
                      center={{
                        lat: position.userLat,
                        lon: position.userLon,
                      }}
                      zoom={17}
                    >
                      <Marker position={{ lat: datum.lat, lon: datum.lon }} />
                    </GoogleMap>
                  </LoadScript>
                </td>
              </tr>


            </tbody>
          </table>;
        })*/}
        <table className={styles.table}>
          <tbody>
            <tr className={styles.thead}>
              <th>店名</th>
              <th>商品名</th>
              <th>値段</th>
              <th>場所</th>
            </tr>
            <tr>
              <td className={styles.bar} colSpan={4}></td>
            </tr>
            <tr className={styles.tbody}>
              <td>{`${data.dealer}`}</td>
              <td>{`${data.name}`}</td>
              <td>{`${data.price}`}</td>
              <td>
                <div>
                  <LoadScript googleMapsApiKey="AIzaSyDzeU7QqfTOkKg58HQujHzTI8jTaOiDfB0">
                    <GoogleMap
                      mapContainerStyle={containerStyle}
                      center={center}
                      zoom={17}
                    >
                      <Marker position={point}></Marker>
                    </GoogleMap>
                  </LoadScript>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Result;
