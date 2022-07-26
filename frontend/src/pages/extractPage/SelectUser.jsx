import {PlusOutlined} from '@ant-design/icons';
import {Input, Tag, notification, Button } from 'antd';
import React, {useEffect, useRef, useState} from 'react';
import { useNavigate, useParams } from "react-router-dom";
import {baseURL} from "../../components/config";

const maxListSize = 5;

const SelectUser = () => {

  let navigate = useNavigate();
  let params = useParams();
  const [tags, setTags] = useState([]);
  const [inputVisible, setInputVisible] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef(null);
  const editInputRef = useRef(null);


  const isUserValid = async (username) => {
    let requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };
    return await fetch(baseURL + "tweet/twitteruser/api/" + username + "/", requestOptions)
        .then(response => response.status === 200)
        .catch(error => console.log('error', error));
  }

  useEffect(() => {
    if (inputVisible) {
      inputRef.current?.focus();
    }
  }, [inputVisible]);
  useEffect(() => {
    editInputRef.current?.focus();
  }, [inputValue]);

  const handleClose = (removedTag) => {
    const newTags = tags.filter((tag) => tag !== removedTag);
    console.log(newTags);
    setTags(newTags);
  };

  const showInput = () => {
    setInputVisible(true);
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleInputConfirm = async () => {
    let error = null;
    let trimmed = inputValue.trim();
    if (trimmed === '')
        error = 'empty'
    else if (tags.indexOf(inputValue) !== -1)
      error = "نام کاربری تکراری است."
    else if(!(await isUserValid(inputValue)))
      error = 'نام کاربری نامعتبر است.'
    if(error)
    {
      if (error !== 'empty')
      {
        notification.error({
          message: 'خطا',
          duration: 2,
          description: error,
        });
      }
    }
    else {
      setTags([...tags, inputValue]);
    }
    setInputVisible(false);
    setInputValue('');
  };

  const onSubmit = () => {
    if(tags.length < 1)
      return notification.error({
          message: 'خطا',
          duration: 2,
          description: 'حداقل یک نام کاربری وارد کنید.',
      });
    console.log(params)
    let myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    let raw = JSON.stringify({
      "name": params.collection,
      "twitter_usernames": tags
    });
    let requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };

    fetch(baseURL+"tweet/collection/api/", requestOptions)
      .then(response => {
        if(response.status === 201)
        {
          navigate('/extract/extractprogress/'+params.collection);
        }
      })
      .catch(error => console.log('error', error));
  };

  return (
    <div className={'d-flex flex-column h-100'}>
      <h6 className={'lh-lg'}>
          لطفا نام کاربری کاربران مدنظر خود را اضافه کنید.
      </h6>
      <div className={'my-auto pb-3'}>
        {tags.map((tag, index) => {
          return (
              <Tag
                  className="edit-tag my-1"
                  key={tag}
                  closable={true}
                  onClose={() => handleClose(tag)}
              >
              <span>
                {tag}
              </span>
              </Tag>
          );
        })}
        {inputVisible && tags.length < maxListSize && (
          <Input
            ref={inputRef}
            type="text"
            size="small"
            className="tag-input"
            value={inputValue}
            onChange={handleInputChange}
            onBlur={handleInputConfirm}
            onPressEnter={handleInputConfirm}
          />
        )}
        {!inputVisible && tags.length < maxListSize && (
          <Tag className="site-tag-plus" onClick={showInput}>
            ورود نام کاربری جدید
            <PlusOutlined className={'me-1'}/>
          </Tag>
        )}
      </div>
      <div className={'d-flex flex-row w-100 pt-3 border-top'}>
        <Button className={'ms-auto'} key="back" onClick={() => {navigate('/extract/selectcollection');}}>
            بازگشت
        </Button>
        <Button className={'me-auto'} key="submit" type="primary" loading={false}
                onClick={onSubmit}>
            شروع پردازش
        </Button>
      </div>
    </div>
  );
};

export default SelectUser;