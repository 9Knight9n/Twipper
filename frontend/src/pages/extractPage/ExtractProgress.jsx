import React, { useState } from 'react';

import { Select, Button, Divider, Input, Progress, ConfigProvider } from 'antd';
import { useNavigate   } from "react-router-dom";





function ExtractProgress() {

    const [progress, setProgress] = useState([{'name':'user1','progress':100},{'name':'user2','progress':50},{'name':'user3','progress':0}]);

    let navigate = useNavigate();


    return (
        <React.Fragment>
            <h6 className={'lh-lg'}>
                درحال دریافت پیام های هر کاربر ...
                <br/>
                پس از اتمام به صفحه نتایج انتقال خواهید یافت.
            </h6>
            {progress.map((item)=>
                <ConfigProvider direction="ltr">
                <div className={'d-flex flex-row my-2'} dir="ltr">
                    {item.name}
                    <Progress dir={'ltr'} className={'ms-3'} percent={item.progress} size="small" status={item.progress===100?'success':'active'} />
                </div>
                </ConfigProvider>
            )}
        </React.Fragment>
    );
}

export default ExtractProgress;
