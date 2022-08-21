import React, {useState,useEffect} from 'react';
import { Avatar, List, Space } from 'antd';
import { useNavigate, useParams, useOutletContext  } from "react-router-dom";
import './userAnalysis.css'
import UserList from "./userList";
import {baseURL} from "../../../components/config";



function UserAnalysis(props) {


    const userList = useOutletContext();



    return (
        <>
            <h6>
                برای مشاهده تحلیل برروی کاربر مدنظر کلیک کنید.
            </h6>
            <br/>
            <UserList userList={userList}/>
        </>
    );
}

export default UserAnalysis;
