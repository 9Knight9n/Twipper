import {PlusOutlined} from '@ant-design/icons';
import {Input, Tag} from 'antd';
import React, {useEffect, useRef, useState} from 'react';

const maxListSize = 5;

const SelectUser = () => {
  const [tags, setTags] = useState([]);
  const [inputVisible, setInputVisible] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [editInputIndex, setEditInputIndex] = useState(-1);
  const [editInputValue, setEditInputValue] = useState('');
  const inputRef = useRef(null);
  const editInputRef = useRef(null);
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

  const handleInputConfirm = () => {
    if (inputValue && tags.indexOf(inputValue) === -1) {
      setTags([...tags, inputValue]);
    }

    setInputVisible(false);
    setInputValue('');
  };

  const handleEditInputChange = (e) => {
    setEditInputValue(e.target.value);
  };

  const handleEditInputConfirm = () => {
    const newTags = [...tags];
    newTags[editInputIndex] = editInputValue;
    setTags(newTags);
    setEditInputIndex(-1);
    setInputValue('');
  };

  return (
    <div className={'d-flex flex-column h-100'}>
      <h6 className={'lh-lg'}>
          لطفا نام کاربری کاربران مدنظر خود را اضافه کنید.
      </h6>
      <div className={'my-auto'}>
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
    </div>
  );
};

export default SelectUser;