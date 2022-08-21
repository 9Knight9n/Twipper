import { UserOutlined, TeamOutlined, SettingOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Menu as AntdMenu} from 'antd';
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from "react-router-dom";


const Menu: React.FC = () => {
  const [current, setCurrent] = useState(
      window.location.pathname.includes("useranalysis")?"per_user":'per_collection'
  );
  let navigate = useNavigate();
  let params = useParams();



  const items: MenuProps['items'] = [
    {
      label: <span onClick={()=> {navigate('/result/useranalysis/'+params.collection)}}>
            تحلیل هر کاربر
          </span>,
      key: 'per_user',
      icon: <UserOutlined />,
    },
    {
      label: <span onClick={()=> {navigate('/result/collectionanalysis/'+params.collection)}}>
            تحلیل گروهی
          </span>,
      key: 'per_collection',
      icon: <TeamOutlined />,
      // disabled: true,
    },
    {
      label:
          <button className={'btn btn-sm btn-primary me-auto'} onClick={()=> {navigate('/extract')}}>
            انتخاب مجموعه دیگر
          </button>,
      key: 'select_collection',
    },
  ];

  const onClick: MenuProps['onClick'] = e => {
    console.log('click ', e);
    setCurrent(e.key);
  };

  return (
      <>
          <AntdMenu onClick={onClick} selectedKeys={[current]} mode="horizontal" items={items} />
      </>
  );
};

export default Menu;