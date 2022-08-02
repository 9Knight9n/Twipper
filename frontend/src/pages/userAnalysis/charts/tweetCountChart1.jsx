import { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";
import { Select } from 'antd';
import {baseURL} from "../../../components/config";

const { Option } = Select;

let options = {
  chart: {
    type: "line",
    zoom: {
      enabled: true,
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: 7,
    curve: "smooth",
  },

  tooltip: {
    shared: true,
    intersect: false,
    y: {
      formatter: function (y) {
        if (typeof y !== "undefined") {
          return y;
        }
        return y;
      },
    },
    z: {
      title: "بازه زمانی :",
    }
  },
  markers: {
    size: 0,
  },
  noData: {
    text: "اطلاعاتی جهت نمایش وجود ندارد.",
    align: "center",
    verticalAlign: "middle",
    offsetX: 0,
    offsetY: 0,
    style: {
      color: undefined,
      fontSize: "14px",
      fontFamily: undefined,
    },
  },
  yaxis: {
    labels: {
      offsetX: 0,
      offsetY: 0,
      rotate: 0,
    },
    title: {
      text: "تعداد پیام",
      offsetX: 0,
      offsetY: 0,
      style: {
        fontSize: "18px",
        fontWeight: "normal",
        fontFamily: undefined,
        color: "#444444",
      },
    },
  },
  xaxis: {
    type:'datetime',
    // tickAmount: 2,
    title: {
      text: "زمان",
      offsetX: 0,
      offsetY: 0,
      style: {
        fontSize: "18px",
        fontWeight: "normal",
        fontFamily: undefined,
        color: "#444444",
      },
    },
  },
};


const TweetCountChart1 = ({userId}) => {
  const [series, setSeries] = useState([{ name: "تعداد پیام ", data: [] }]);

  useEffect(() => {
    getSeries(7)
  }, []);

  // useEffect(() => {
  //   getSeries(document.getElementById('selectvalue1').valueOf())
  // }, [userId]);


  function getSeries(length) {
    let requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };
    fetch(baseURL + "tweet/get_user_tweet_count_chart1_by_id/" + userId.toString() + "/" + length.toString() + "/", requestOptions)
      .then(response => response.text())
      .then(result => {
        let temp = JSON.parse(result);
        let series = [];
        series.push({ data: temp.data });
        setSeries(series);
      })
      .catch(error => console.log('error', error));

  }

  const handleChange = (value) => {
   getSeries(value)
  };

  return (
    <div className={'d-flex flex-column'} dir={"ltr"} id="chart1">
      <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
        <h6 className={'my-auto'}>نمودار تعداد پیام در هر </h6>
        <Select
          id={'selectvalue1'}
          defaultValue="7"
          bordered={false}
          onChange={handleChange}
        >
          <Option value="1">روز</Option>
          <Option value="7">هفته</Option>
          <Option value="30">ماه</Option>
        </Select>
      </div>
      <ReactApexChart
        options={options}
        series={series}
        type="line"
        height={385}
      />
    </div>
  );
};

export default TweetCountChart1;
