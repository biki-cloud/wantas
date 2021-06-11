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
  const SetPlace = useSetPlace();
  const [addresses, setAddresses] = useState(["address.0"]);
  const [update, setUpdata] = useState<boolean>(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const addAddress = () => {
    const c = addresses.slice();
    c.push(`address.${addresses.length}`);
    setAddresses(c);
  };
  const removeAddress = () => {
    const c = addresses.slice();
    c.pop();
    setAddresses(c);
    setUpdata(update ? false : true);
  };

  const getPlacePosition = (place) => {
    let p = {};
    const res = axios
      .get("https://maps.googleapis.com/maps/api/geocode/json", {
        params: {
          address: place,
          sensor: false,
          key: "AIzaSyDzeU7QqfTOkKg58HQujHzTI8jTaOiDfB0",
        },
      })
      .then(/*(res) => {
        console.log(res);
        SetPlace({
          userLat: res.data.resullts[0].geometry.location.lat,
          userLon: res.data.results[0].geometry.location.lng,
        });
        p = {
          userLat: res.data.results[0].geometry.location.lat,
          userLon: res.data.results[0].geometry.location.lng,
        };
      }*/)
      .catch((err) => {});
    return p;
  };
  //位置情報で検索する場合
  const getPosition = () => {
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
      SetPlace({
        userLat: startPos.coords.latitude,
        userLon: startPos.coords.longitude,
      });
    };
    const geoError = function (error) {
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
    let place = {};
    if (e.place) {
      //場所を入力していればlat,lonをapiで取りに行く
      place = await getPlacePosition(e.place);
    } else {
      // 入力してない場合、位置情報を取得する
      place = await getPosition();
    }
    const submitData = new FormData();
    //addresses.map((address, index) => {
    //複数検索出来る
    submitData.append("productName", e.address);
    submitData.append("userLat", "33.2488525");
    submitData.append("userLon", "129.6930912");
    //});
    await axios
      .post("/search", submitData)
      .then((response) => {
        console.log(response.data);
        const data = response.data;
        setData(
          /*response.data.map(() => (*/ {
            dealer: data.dealer,
            name: data.name,
            price: data.price,
            lat: data.lat,
            lon: data.lon,
          } //))
        );
      })
      .catch((error) => {
        alert(error);
      });
  };
  return (
    <div className={styles.post}>
      <h1>検索フォーム</h1>
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
