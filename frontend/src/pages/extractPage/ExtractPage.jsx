import React, { useState } from 'react';

import { Modal, Button, Divider, Input } from 'antd';
import { BrowserRouter,Routes, Route, useMatch,Outlet  } from "react-router-dom";

import './ExtractPage.css';
import SelectCollection from "./SelectCollection";

function ExtractPage() {

    const [visible, setVisible] = useState(true);
    const [loading, setLoading] = useState(false);
    const [modalText, setModalText] = useState('سلام وققتون بخیر');
    // let { path, url } = useMatch();


    const handleOk = () => {
        setModalText('The modal will be closed after two seconds');
        setLoading(true);
        setTimeout(() => {
            setVisible(false);
            setLoading(false);
        }, 2000);
    };

    const handleCancel = () => {
        console.log('Clicked cancel button');
        setVisible(false);
    };

    return (
        <React.Fragment>
            <Modal className={'no-header-modal no-footer-modal'} onCancel={()=>{}}
                   centered
                   bodyStyle={{
                       height:'50vh',
                   }}
                    visible={visible}
                    footer={[
                        <Button key="back" onClick={handleCancel}>
                            Return
                        </Button>,
                        <Button key="submit" type="primary" loading={loading} onClick={handleOk}>
                            Submit
                        </Button>,
                        <Button key="link"
                                href="https://google.com"
                                type="primary"
                                loading={loading}
                                onClick={handleOk}>
                            Search on Google
                        </Button>,
                    ]}>
                <Outlet/>
            </Modal>
        </React.Fragment>
    );
}

export default ExtractPage;
