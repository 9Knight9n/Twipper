import React, { useState } from 'react';

import { Modal, Button, Divider, Input } from 'antd';

import './ExtractPage.css';

function ExtractPage() {

    const [visible, setVisible] = useState(true);
    const [loading, setLoading] = useState(false);
    const [modalText, setModalText] = useState('سلام وققتون بخیر');


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
            <Modal className={'no-header-modal'} onCancel={()=>{}}
                   centered
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
                <div>
                    <Input placeholder="Basic usage" />
                    <Divider type="vertical"/>
                    <Input placeholder="Basic usage" />
                </div>
            </Modal>
        </React.Fragment>
    );
}

export default ExtractPage;
