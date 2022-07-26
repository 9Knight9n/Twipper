import React, { useState, useEffect } from 'react';

import { Modal, Button, Divider, Input } from 'antd';
import { BrowserRouter,Routes, Route, useMatch,Outlet, useLocation, useNavigate } from "react-router-dom";

import './ExtractPage.css';
import SelectCollection from "./SelectCollection";

function ExtractPage() {

    let navigate = useNavigate();
    const [visible, setVisible] = useState(true);
    const [showFooter, setShowFooter] = useState(false);
    const [nextButtonText, setNextButtonText] = useState('');
    const [nextButtonFunc, setNextButtonFunc] = useState(() => () =>{});
    const [preButtonText, setPreButtonText] = useState('');
    const [preButtonFunc, setPreButtonFunc] = useState(() => () =>{});
    const [loading, setLoading] = useState(false);
    const location = useLocation();


    useEffect(() => {
        setShowFooter(!window.location.pathname.includes('selectcollection'));
        if(window.location.pathname.includes('selectuser'))
        {
            setNextButtonText('شروع پردازش')
            setPreButtonText('بازگشت')
            setNextButtonFunc(() => () => {navigate('/extract/extractprogress');})
            setPreButtonFunc(() => () => {navigate('/extract/selectcollection');})
        }
        else if(window.location.pathname.includes('extractprogress'))
        {
            setNextButtonText(false)
            setPreButtonText('شروع مجدد')
            setPreButtonFunc(() => () => {navigate('/extract/selectcollection');})
            setNextButtonFunc(() => () => {})
        }
    }, [location])


    const handleOk = () => {
        setLoading(true);
        setTimeout(() => {
            setVisible(false);
            setLoading(false);
        }, 2000);
    };

    const handleCancel = () => {
        console.log('Clicked cancel button');
        // setVisible(false);
        console.log(window.location.pathname)
    };

    return (
        <React.Fragment>
            <Modal className={'no-header-modal'.concat(!showFooter?" no-footer-modal":"")}
                   onCancel={()=>{}}
                   centered
                   bodyStyle={{
                       height:'fit-content',
                   }}
                    visible={visible}
                    footer={[
                        <div className={'d-flex flex-row w-100'}>
                            <Button className={'ms-auto'} key="back" onClick={preButtonFunc}>
                                {preButtonText}
                            </Button>
                            {nextButtonText?
                            <Button className={'me-auto'} key="submit" type="primary" loading={loading} onClick={nextButtonFunc}>
                                {nextButtonText}
                            </Button>:""}
                        </div>
                    ]}>
                <Outlet/>
            </Modal>
        </React.Fragment>
    );
}

export default ExtractPage;
