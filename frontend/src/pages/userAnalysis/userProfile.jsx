import { Button, Drawer, Space } from 'antd';
import { Descriptions,List,Avatar } from 'antd';
import {CheckCircleOutlined,CloseCircleOutlined} from '@ant-design/icons';
import React, { useState,useEffect } from 'react';
import { Collapse } from 'antd';
import TweetCountChart1 from "./charts/tweetCountChart1";
import {baseURL} from "../../components/config";
import TweetCountChart2 from "./charts/tweetCountChart2";
import TFIDFChart1 from "./charts/TFIDFChart1";
import LDAChart1 from "./charts/LDAChart1";
import LDAChart2 from "./charts/LDAChart2";

const { Panel } = Collapse;

function UserProfile({selectedUserId}) {

    const [userInfo, setUserInfo] = useState({'username':null,'id':null,'display_name':null,'description':null,
        'verified':null,'created':null,'followers_count':null,'friends_count':null,
        'statuses_count':null,'favourites_count':null,'location':null,'profile_image_url':null});

    useEffect(()=>{
        getUserInfo(selectedUserId)
    },[selectedUserId]);

    function getUserInfo(id) {
        let requestOptions = {
            method: 'GET',
            redirect: 'follow'
        };
        fetch(baseURL + "tweet/get_user_info_by_id/" + selectedUserId + "/", requestOptions)
            .then(response => response.text())
            .then(result => {
                let temp = JSON.parse(result);
                console.log(temp)
                setUserInfo(temp)
                // setCollection(temp.name)
                // setUserList(temp.twitter_user_list)
            })
            .catch(error => console.log('error', error));
    }

    return (
       <Collapse bordered={true} defaultActiveKey={['1']} >
        <Panel header="پروفایل کاربر" key="1">
            <Descriptions contentStyle={{fontSize:'80%'}} labelStyle={{fontSize:'90%'}}
                          title={<div>
                                    <List.Item.Meta className={'mt-3'}
                                      avatar={<Avatar src={userInfo.profile_image_url} />}
                                      title={userInfo.username+"@"}
                                      description={userInfo.display_name}
                                    />
                                </div>}
                          column={{
                            xxl: 4,
                            xl: 3,
                            lg: 3,
                            md: 2,
                            sm: 1,
                            xs: 1,
                          }}>
                <Descriptions.Item label="نام کاربری">{userInfo.username}</Descriptions.Item>
                <Descriptions.Item label="نام نمایشی">{userInfo.display_name}</Descriptions.Item>
                <Descriptions.Item label="توضیحات">{userInfo.description}</Descriptions.Item>
                <Descriptions.Item label="وضعییت تایید شدن">{userInfo.verified?<CheckCircleOutlined />:<CloseCircleOutlined />}</Descriptions.Item>
                <Descriptions.Item label="تاریخ ثبت نام">{userInfo.created}</Descriptions.Item>
                <Descriptions.Item label="تعداد دنبال کنندگان">{userInfo.followers_count}</Descriptions.Item>
                <Descriptions.Item label="تعداد دوستان">{userInfo.friends_count}</Descriptions.Item>
                <Descriptions.Item label="تعداد پیام ها">{userInfo.statuses_count}</Descriptions.Item>
                <Descriptions.Item label="تعداد پیام های مورد علاقه">{userInfo.favourites_count}</Descriptions.Item>
                <Descriptions.Item label="آدرس">
                    {userInfo.location}
                </Descriptions.Item>
            </Descriptions>
        </Panel>
        <Panel header="فراوانی پیام ها" key="2">
            <div className="row">
               <div className="col-lg-6 col-md-12"><TweetCountChart1 userId={selectedUserId}/></div>
               <div className="col-lg-6 col-md-12"><TweetCountChart2 userId={selectedUserId}/></div>
            </div>
        </Panel>
        <Panel header="ابرواژگان" key="3">
            <div className="row">
                <div className="col-12"><TFIDFChart1 userId={selectedUserId}/></div>
            </div>
        </Panel>
        <Panel header="تحلیل موضوعات کاربر" key="4">
            <div className="row">
               {/*<div className="col-lg-6 col-md-12"><TweetCountChart1 userId={selectedUserId}/></div>*/}
               <div className="col-lg-12 col-md-12"><LDAChart1 userId={selectedUserId}/></div>
            </div>
        </Panel>
        <Panel header="تحلیل روند موضوعات" key="5">
            <div className="row">
               <div className="col-lg-12 col-md-12"><LDAChart2 userId={selectedUserId}/></div>
            </div>
        </Panel>
        {/*<div className="ant-descriptions-title" style={{marginBottom: '20px'}}></div>*/}

       </Collapse>
    );
}

export default UserProfile;