import React, { useState, useEffect } from 'react';
import { Select, Button, Divider, Input, Empty, notification } from 'antd';
import { useNavigate   } from "react-router-dom";


import {baseURL} from "../../components/config";



const { Option } = Select;


function SelectCollection() {

    let navigate = useNavigate();

    const [collections, setCollections] = useState([]);
    const [collection, setCollection] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        let requestOptions = {
            method: 'GET',
            redirect: 'follow'
        };
        fetch(baseURL+'tweet/collection/api/', requestOptions)
            .then(response => response.text())
            .then(result => {
                setCollections(JSON.parse(result))
            })
            .catch(error => console.log('error', error));
    }, []);


    const onChange = (value: string) => {
        // console.log(`selected ${value}`);
        navigate('/extract/extractprogress/'+value)
    };

    const onInputChange = (e) => {
        // console.log('Change:', e.target.value);
        setCollection(e.target.value)
    };

    const onSubmit = (e) => {
        let trimmed = collection.trim();
        if( trimmed === '' )
        {
            return notification.error({
                message: 'خطا',
                duration: 2,
                description: 'نام مجموعه نمی تواند خالی باشد.',
            });
        }
        for (let item of collections)
        {
            if(item.name === trimmed)
            {
                return notification.error({
                    message: 'خطا',
                    duration: 2,
                    description: 'مجموعه ای به این نام وجود دارد.',
                });
            }
        }

        navigate('/extract/selectuser/'+trimmed)
    };


    return (
        <React.Fragment>
            <div className={'d-flex flex-column h-100'}>
                <h6 className={'lh-lg'}>
                    سلام خوش آمدید
                    <br/>
                    لطفا مجموعه مدنظر خود را انتخاب کنید یا با ورود نام مجموعه ای ایجاد کنید.
                </h6>
                <div className={'d-flex flex-row h-100 mt-2'}>
                    <Select showSearch className={'w-50 my-auto'}
                            placeholder="انتخاب مجموعه"
                            optionFilterProp="children"
                            onChange={onChange}
                            notFoundContent={<Empty description={'مجموعه ای یافت نشد.'} />}
                            filterOption={(input, option) =>
                                option.children.toLowerCase().includes(input.toLowerCase())
                            }
                            >
                        {collections.map((collection)=>
                            <Option key={collection.id} value={collection.id}>{collection.name}</Option>
                        )}
                    </Select>
                    <Divider type="vertical" style={{height:'50px'}} className={'border-secondary mx-4 my-auto'}/>
                    <Input.Group compact className={'w-50 d-flex flex-row my-auto'} style={{height:'fit-content'}}>
                        <Input style={{ height:'fit-content'}} onChange={onInputChange} placeholder="نام مجموعه" />
                        <Button type="primary" onClick={onSubmit}>ساخت</Button>
                    </Input.Group>
                </div>
            </div>
        </React.Fragment>
    );
}

export default SelectCollection;
