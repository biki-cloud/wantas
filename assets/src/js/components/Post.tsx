import React, { useState, useContext } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";
import styles from "./Post.module.css";
import { useForm } from "react-hook-form";
import { useSetData, useSetPlace, DataContext } from "../context/dataContext";

type PLACE = { userLat: any; userLon: any } | any;

const Post: React.FC = () => {
  const data = useContext(DataContext).data;
  const position = useContext(DataContext).place;
  const setData = useSetData();
  const setPlace = useSetPlace();
  const [addresses, setAddresses] = useState(["address.0"]); // 複数検索する場合のinput用
  const [update, setUpdate] = useState<boolean>(false);
  const [geo, setGeo] = useState(false);
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

  const getPosition = () => {
    //位置情報からlat,lngをとる
    let startPos;
    const showNudgeBanner = function () {
      //位置情報がoffの場合の処理
      setGeo(true);
    };
    const hideNudgeBanner = function () {
      //位置情報がonの場合の処理
      setGeo(false);
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
      return {
        userLat: startPos.coords.latitude,
        userLon: startPos.coords.longitude,
      };
    };
    console.log(() => );
    const geoError = function (error) {
      //位置情報が取れなかった
      switch (error.code) {
        case error.TIMEOUT:
          showNudgeBanner();
          break;
      }
    };
    const nav = navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
    console.log(nav);
    return 
  };

  const onSubmit = async (e) => {
    let place: PLACE = { userLat: 0, userLon: 0 };

    // 入力してない場合、位置情報を取得する
    place = await getPosition();
    const submitData = new FormData();
    addresses.map((address, index) => {
      submitData.append("productName", e.address);
    });
    submitData.append("userLat", `${place.userLat}`);
    submitData.append("userLon", `${place.userLon}`);
    await axios
      .post("/search", submitData)
      .then((response) => {
        response.data.map((datum) => {});
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
          <label className={styles.label}>商品名</label>
          {addresses.map((address) => {
            return (
              <div key={address} className={styles.textBox}>
                <input
                  className={styles.text}
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
          <button className={styles.submit}>検索 </button>
        </form>
        <button className={styles.button} onClick={addAddress}>
          +
        </button>
        <button className={styles.button} onClick={removeAddress}>
          -
        </button>
        {geo && (
          <div>
            <h1>位置情報を有効にしてください</h1>
          </div>
        )}
      </div>
    </div>
  );
};

export default Post;
