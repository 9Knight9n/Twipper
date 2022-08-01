import { UserOutlined, TeamOutlined, SettingOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Menu as AntdMenu} from 'antd';
import React, { useState } from 'react';
import { useNavigate, useParams } from "react-router-dom";


const Menu: React.FC = () => {
  const [current, setCurrent] = useState('per_user');
  let navigate = useNavigate();

  const items: MenuProps['items'] = [
    {
      label: 'تحلیل هر کاربر',
      key: 'per_user',
      icon: <UserOutlined />,
    },
    {
      label: 'تحلیل گروهی',
      key: 'per_collection',
      icon: <TeamOutlined />,
      disabled: true,
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

  return <AntdMenu onClick={onClick} selectedKeys={[current]} mode="horizontal" items={items} />;
};

export default Menu;