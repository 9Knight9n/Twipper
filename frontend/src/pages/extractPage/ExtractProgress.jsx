import React, { useState, useEffect } from 'react';

import { Select, Button, Divider, Input, Progress, ConfigProvider, notification } from 'antd';
import { useNavigate, useParams } from "react-router-dom";
import {baseURL} from "../../components/config";





function ExtractProgress() {

    const [progress, setProgress] = useState([]);
    const [done, setDone] = useState(false);
    const [interval, setInterval] = useState([{'name':'user1','progress':100},{'name':'user2','progress':50},{'name':'user3','progress':0}]);

    let navigate = useNavigate();
    let params = useParams();

    const getProgress = async () => {
        console.log('ran')
        let requestOptions = {
            method: 'GET',
            redirect: 'follow'
        };
        fetch(baseURL + "tweet/collection/api/" + params.collection + "/", requestOptions)
            .then(response => response.text())
            .then(async result => {
                let temp = JSON.parse(result);
                setProgress(temp.twitter_user_percentage)
                if (temp.done) {
                    notification.success({
                        key: 'done',
                        message: 'موفق',
                        duration: 6,
                        description: 'مجموعه مدنظر اضافه شد.',
                    });
                    await new Promise(r => setTimeout(r, 2000));
                    return navigate('/useranalysis/' + params.collection)
                }
            })
            .catch(error => console.log('error', error));
    };

    const loop = async () => {
        await getProgress()
        if (window.location.pathname.includes("extract/extractprogress")) setTimeout(loop, 2000);
    }

    useEffect(() => {
        setTimeout(loop, 10)
    }, []);


    return (
        <React.Fragment>
            <h6 className={'lh-lg'}>
                درحال دریافت پیام های هر کاربر ...
                <br/>
                پس از اتمام به صفحه نتایج انتقال خواهید یافت.
            </h6>
            {progress.map((item)=>
                <div key={item.name}>
                    <ConfigProvider direction="ltr">
                    <div className={'d-flex flex-row my-2'} dir="ltr">
                        {item.name}
                        <Progress style={{width:'calc(100% - 9rem)'}} dir={'ltr'} className={'ms-3'} percent={item.progress} size="small" status={item.progress===100?'success':'active'} />
                    </div>
                    </ConfigProvider>
                </div>
            )}
            <div className={'d-flex flex-row w-100 pt-3 border-top'}>
                <Button className={'ms-auto'} key="back" onClick={() => {navigate('/extract/selectcollection');}}>
                    شروع مجدد
                </Button>
            </div>
        </React.Fragment>
    );
}

export default ExtractProgress;
