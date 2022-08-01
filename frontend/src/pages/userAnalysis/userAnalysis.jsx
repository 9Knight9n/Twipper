import React, {useState,useEffect} from 'react';
import { Avatar, List, Space } from 'antd';
import Menu from "./menu";
import './userAnalysis.css'
import UserList from "./userList";



function UserAnalysis(props) {

    return (
        <div className={'main-container-md'}>
            <div className={'d-flex flex-row mb-3'}>
                <h6 className={'my-auto ms-3'}>
                    مجموعه انتخاب شده:
                </h6>
                <h5 className={'my-auto'}>
                    مجموعه اول
                </h5>
            </div>

            <Menu/>
            <br/>
            <br/>
            <br/>
            <UserList/>
        </div>

    );
}

export default UserAnalysis;
