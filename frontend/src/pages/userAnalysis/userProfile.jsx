import { Button, Drawer, Space } from 'antd';
import type { DrawerProps } from 'antd/es/drawer';
import { Descriptions } from 'antd';
import React, { useState } from 'react';
import Chart from "../../components/chart";

function UserProfile(props) {
    const [visible, setVisible] = useState(true);
    const [size, setSize] = useState();

    const showDefaultDrawer = () => {
        setSize('default');
        setVisible(true);
      };

      const showLargeDrawer = () => {
        setSize('large');
        setVisible(true);
      };

      const onClose = () => {
        setVisible(false);
      };



    return (
       <Drawer
        title={`تحلیل کاربر`}
        placement="left"
        width={'75vw'}
        onClose={onClose}
        closable={false}
        visible={visible}
      >
        <Descriptions contentStyle={{fontSize:'80%'}} labelStyle={{fontSize:'90%'}}
                      title="پروفایل کاربر"
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
        <Chart/>
      </Drawer>
    );
}

export default UserProfile;