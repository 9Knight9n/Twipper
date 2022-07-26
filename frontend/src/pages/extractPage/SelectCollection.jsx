import React, { useState } from 'react';

import { Select, Button, Divider, Input } from 'antd';
import { useNavigate   } from "react-router-dom";



const { Option } = Select;


function SelectCollection() {

    let navigate = useNavigate();

    const [loading, setLoading] = useState(false);


    const onChange = (value: string) => {
        console.log(`selected ${value}`);

    };

    const onSearch = (value: string) => {
        console.log('search:', value);
    };


    return (
        <React.Fragment>
            <div className={'d-flex flex-column h-100'}>
                <h6 className={'lh-lg'}>
                    سلام خوش آمدید
                    <br/>
                    لطفا مجموعه مدنظر خود را انتخاب کنید یا با ورورد نام مجموعه ای ایجاد کنید.
                </h6>
                <div className={'d-flex flex-row h-100'}>
                    <Select showSearch className={'w-50 my-auto'}
                            placeholder="انتخاب مجموعه"
                            optionFilterProp="children"
                            onChange={onChange}
                            onSearch={onSearch}
                            filterOption={(input, option) =>
                                option.children.toLowerCase().includes(input.toLowerCase())
                            }
                            >
                        <Option value="jack">Jack</Option>
                        <Option value="lucy">Lucy</Option>
                        <Option value="tom">Tom</Option>
                    </Select>
                    <Divider type="vertical" className={'h-50 border-secondary mx-4 my-auto'}/>
                    <Input.Group compact className={'w-50 d-flex flex-row my-auto'} style={{height:'fit-content'}}>
                        <Input style={{ height:'fit-content'}} placeholder="نام مجموعه" />
                        <Button type="primary" onClick={()=>navigate('../selectuser')}>ساخت</Button>
                    </Input.Group>
                </div>
            </div>
        </React.Fragment>
    );
}

export default SelectCollection;
