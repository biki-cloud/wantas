import React, { useState, useContext } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";
import styles from "./Post.module.css";
import { useForm } from "react-hook-form";
import { useSetData, useSetPlace, DataContext } from "../context/dataContext";

const Post: React.FC = () => {
  const data = useContext(DataContext).data;
  const position = useContext(DataContext).place;
  const setData = useSetData();
  const setPlace = useSetPlace();
  const [addresses, setAddresses] = useState(["address.0"]); // 複数検索する場合のinput用
  const [update, setUpdate] = useState<boolean>(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const addAddress = () => {
    //inputを増やす
    const c = addresses.slice();
    c.push(`address.${addresses.length}`);
    setAddresses(c);
  };
  const removeAddress = () => {
    //inputを減らす
    const c = addresses.slice();
    c.pop();
    setAddresses(c);
    setUpdate(update ? false : true); //inputを削除した際に強制的にレンダリングさせる
  };

  const getPlacePosition = (place) => {
    //入力した場所のlat,lngをgeocodeのapiでとる
    let p = { userLat: 0, userLon: 0 };
    const res = axios
      .get("https://maps.googleapis.com/maps/api/geocode/json", {
        params: {
          address: place,
          sensor: false,
          key: "AIzaSyDzeU7QqfTOkKg58HQujHzTI8jTaOiDfB0",
        },
      })
      .then((res) => {
        setPlace({
          userLat: res.data.results[0].geometry.location.lat,
          userLon: res.data.results[0].geometry.location.lng,
        });
        p = {
          userLat: res.data.results[0].geometry.location.lat,
          userLon: res.data.results[0].geometry.location.lng,
        };
      })
      .catch((err) => {});
    return p;
  };
  const getPosition = () => {
    //位置情報からlat,lngをとる
    let startPos;
    const showNudgeBanner = function () {
      //位置情報がoffの場合の処理
    };
    const hideNudgeBanner = function () {
      //位置情報がonの場合の処理
    };
    const nudgeTimeoutId = setTimeout(showNudgeBanner, 5000);

    const geoSuccess = function (position) {
      hideNudgeBanner();
      clearTimeout(nudgeTimeoutId);
      startPos = position;
      setPlace({
        userLat: startPos.coords.latitude,
        userLon: startPos.coords.longitude,
      });
    };
    const geoError = function (error) {
      //位置情報が取れなかった
      switch (error.code) {
        case error.TIMEOUT:
          showNudgeBanner();
          break;
      }
    };
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
    return {
      userLat: startPos.coords.latitude,
      userLon: startPos.coords.longitude,
    };
  };

  const onSubmit = async (e) => {
    let place = { userLat: 0, userLon: 0 };
    if (e.place) {
      //場所を入力していればlat,lonをapiで取りに行く
      place = await getPlacePosition(e.place);
    } else {
      // 入力してない場合、位置情報を取得する
      place = await getPosition();
    }
    const submitData = new FormData();
    addresses.map((address, index) => {
      submitData.append("productName", e.address);
    });
    submitData.append("userLat", `${place.userLat}`);
    submitData.append("userLon", `${place.userLon}`);
    await axios
      .post("/search", submitData)
      .then((response) => {
        console.log(response.data);
        response.data.map((datum) => {
          console.log(datum.dealer);
        });
        setData(
          response.data.map((datum) => {
            return {
              dealer: datum.dealer,
              name: datum.productName,
              price: datum.price,
              lat: datum.lat,
              lon: datum.lon,
            };
          })
        );
      })
      .catch((error) => {
        alert(error);
      });
  };
  return (
    <div className={styles.post}>
      <div className={styles.wrapper}>
        <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
          <label className={styles.label}>現在地</label>
          <input className={styles.input} {...register("place")} />
          <label className={styles.label}>商品名</label>
          {addresses.map((address) => {
            return (
              <div key={address}>
                <input
                  className={styles.input}
                  {...register(`${address}`, { required: true, maxLength: 30 })}
                />
              </div>
            );
          })}
          {errors.name && errors.name.type === "required" && (
            <span>This is required</span>
          )}
          {errors.name && errors.name.type === "maxLength" && (
            <span>Max length exceeded</span>
          )}
          <button className={styles.button}>検索 </button>
        </form>
        <button className={styles.button} onClick={addAddress}>
          +
        </button>
        <button className={styles.button} onClick={removeAddress}>
          -
        </button>
      </div>
    </div>
  );
};

export default Post;
