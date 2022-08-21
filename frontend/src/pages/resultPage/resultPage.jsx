import React, {useState,useEffect} from 'react';
import Menu from "./menu";
import { Outlet , useParams } from "react-router-dom";
import {baseURL} from "../../components/config";

function ResultPage(props) {

    const [collection, setCollection] = useState('');
    const [userList, setUserList] = useState([]);
    let params = useParams();
    useEffect(() => {
        loadCollection()
    }, []);

    const loadCollection = () => {
        let requestOptions = {
            method: 'GET',
            redirect: 'follow'
        };
        fetch(baseURL + "tweet/get_users_by_collection/" + params.collection + "/", requestOptions)
            .then(response => response.text())
            .then(result => {
                let temp = JSON.parse(result);
                console.log(temp)
                setCollection(temp.name)
                setUserList(temp.twitter_user_list)
            })
            .catch(error => console.log('error', error));
    };


    return (
        <div className={'main-container-md'}>
            <div className={'d-flex flex-row mb-3'}>
                <h6 className={'my-auto ms-3'}>
                    مجموعه انتخاب شده:
                </h6>
                <h5 className={'my-auto'}>
                    {collection}
                </h5>
            </div>

            <Menu/>
            <br/>
            <br/>
            <Outlet context={userList}/>
        </div>
    );
}

export default ResultPage;