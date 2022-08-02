import { Button, Drawer, Space } from 'antd';
import { Descriptions,List,Avatar } from 'antd';
import React, { useState,useEffect } from 'react';
import TweetCountChart1 from "./charts/tweetCountChart1";

function UserProfile({selectedUserId}) {

    const [userInfo, setUserInfo] = useState({});

    useEffect(()=>{
        getUserInfo(selectedUserId)
    },[selectedUserId]);

    function getUserInfo(id) {

    }

    return (
       <>
        <Descriptions contentStyle={{fontSize:'80%'}} labelStyle={{fontSize:'90%'}}
                      title={<div>
                                  پروفایل کاربر
                                    <List.Item.Meta className={'mt-3'}
                                      avatar={<Avatar src={null} />}
                                      title={"sqsqsq"+"@"}
                                      description={"item.display_name"}
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
            <Descriptions.Item label="نام کاربری">Zhou Maomao</Descriptions.Item>
            <Descriptions.Item label="نام نمایشی">1810000000</Descriptions.Item>
            <Descriptions.Item label="توضیحات">Hangzhou, Zhejiang</Descriptions.Item>
            <Descriptions.Item label="وضعییت تایید شدن">empty</Descriptions.Item>
            <Descriptions.Item label="تاریخ ثبت نام">Hangzhou, Zhejiang</Descriptions.Item>
            <Descriptions.Item label="تعداد دنبال کنندگان">Hangzhou, Zhejiang</Descriptions.Item>
            <Descriptions.Item label="تعداد دوستان">Hangzhou, Zhejiang</Descriptions.Item>
            <Descriptions.Item label="تعداد پیام ها">Hangzhou, Zhejiang</Descriptions.Item>
            <Descriptions.Item label="تعداد پیام های مورد علاقه">Hangzhou, Zhejiang</Descriptions.Item>
            <Descriptions.Item label="آدرس">
              No. 18, Wantang Road, Xihu District, Hangzhou, Zhejiang, China
            </Descriptions.Item>
        </Descriptions>
        <br/>
        <hr/>
        <br/>
        <div className="ant-descriptions-title" style={{marginBottom: '20px'}}>نمودار ها</div>
        <div className="row">
           <div className="col-lg-6 col-md-12"><TweetCountChart1/></div>
           <div className="col-lg-6 col-md-12"><TweetCountChart1/></div>
        </div>
       </>
    );
}

export default UserProfile;