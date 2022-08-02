import React, {useState,useEffect} from 'react';
import { Avatar, List, Space,Drawer } from 'antd';
import Menu from "./menu";
import './userAnalysis.css'
import UserProfile from "./userProfile";


const data = Array.from({ length: 23 }).map((_, i) => ({
  href: 'https://ant.design',
  title: `ant design part ${i}`,
  avatar: 'https://joeschmoe.io/api/v1/random',
  description:
    'Ant Design, a design language .',
  content:
    'We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.',
}));


function UserList({userList}) {

    const [selectedUserId, setSelectedUserId] = useState(null);

    const [visible, setVisible] = useState(false);

    const size = useWindowSize();

    function getListSize(size) {
        if(size.width >= 1600)
            return 8
        if(size.width >= 1200)
            return 6
        if(size.width >= 992)
            return 4
        if(size.width >= 768)
            return 4
        if(size.width >= 576)
            return 2
        return 1
    }

    function openUserProfile(id) {
        setVisible(true)
        setSelectedUserId(id)
    }

    return (
        <>
            <List
            // bordered={true}
            itemLayout="horizontal"
            // loading={true}
            size="large"
            pagination={{
              onChange: page => {
                console.log(page);
              },
              pageSize: getListSize(size)
            }}
            grid={{
              gutter: 16,
              xs: 1,
              sm: 2,
              md: 4,
              lg: 4,
              xl: 6,
              xxl: 8,
            }}
            dataSource={userList}
            renderItem={item => (
              <List.Item
                key={item.id}
              >
                <List.Item.Meta onClick={()=>{openUserProfile(item.id)}}
                  style={{cursor:'pointer'}}
                  avatar={<Avatar src={item.avatar} />}
                  title={item.username+"@"}
                  description={item.display_name}
                />
                {/*{item.content}*/}
              </List.Item>
            )}
          />
            <Drawer
                destroyOnClose={true}
                title={`تحلیل کاربر`}
                placement="left"
                width={'75vw'}
                onClose={()=>{setVisible(false)}}
                closable={false}
                visible={visible}
              >

                <UserProfile selectedUserId={selectedUserId}/>
            </Drawer>
        </>
    );
}

export default UserList;


// Hook
function useWindowSize() {
  // Initialize state with undefined width/height so server and client renders match
  // Learn more here: https://joshwcomeau.com/react/the-perils-of-rehydration/
  const [windowSize, setWindowSize] = useState({
    width: undefined,
    height: undefined,
  });
  useEffect(() => {
    // Handler to call on window resize
    function handleResize() {
      // Set window width/height to state
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }
    // Add event listener
    window.addEventListener("resize", handleResize);
    // Call handler right away so state gets updated with initial window size
    handleResize();
    // Remove event listener on cleanup
    return () => window.removeEventListener("resize", handleResize);
  }, []); // Empty array ensures that effect is only run on mount
  return windowSize;
}
