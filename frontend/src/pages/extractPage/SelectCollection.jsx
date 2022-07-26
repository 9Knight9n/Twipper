import React, { useState } from 'react';

import { Modal, Button, Divider, Input } from 'antd';


function SelectCollection() {

    const [loading, setLoading] = useState(false);


    return (
        <React.Fragment>
            <div className={'d-flex flex-row h-100'}>
                <Input placeholder="Basic usage" />
                <Divider type="vertical" className={'h-100 mx-4'}/>
                <Input.Group compact className={'w-100 d-flex flex-row my-auto'} style={{height:'fit-content'}}>
                    <Input style={{ height:'fit-content'}} placeholder="نام مجموعه" />
                    <Button type="primary">ساخت</Button>
                </Input.Group>
            </div>
        </React.Fragment>
    );
}

export default SelectCollection;
