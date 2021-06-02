import React,{useEffect} from "react";
import axios from "axios"
import styles from "Result.module.css"
import {DATA} from "../app"

const Result:React.FC<DATA>= ({data}) => {
    return (
        <>
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
                        <td>{`${data.dealer}`}</td>
                        <td>{`${data.name}`}</td>
                        <td>{`${data.price}`}</td>
                        <td>{`${data.lat+"/"+data.lon}`}</td>
                    </tr>
                </tbody>
            </table>

        </>
    );
}

export default Result