import { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";
import { Select } from 'antd';
import {baseURL} from "../../../components/config";

const { Option } = Select;

let options = {
  colors : ['#C62828', '#AD1457','#4E342E', '#558B2F', '#4DB6AC', '#616161', '#6A1B9A','#D84315', '#4527A0', '#283593', '#1565C0', '#18FFFF', '#00838F', '#00695C',
    '#2E7D32', '#9E9D24', '#F9A825', '#FF8F00', '#EF6C00', '#37474F','#D84315'],
  chart: {
    type: 'line',
    dropShadow: {
      enabled: true,
      color: '#000',
      top: 18,
      left: 7,
      blur: 10,
      opacity: 0.2
    },
    toolbar: {
      show: false
    }
  },
  grid: {
    borderColor: '#e7e7e7',
    row: {
      colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
      opacity: 0.5
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth'
  },
  legend: {
    position: 'top',
    horizontalAlign: 'left',
    offsetX: 40
  },
  tooltip: {
    // shared: true,
    // intersect: false,
    y: {
      formatter: function (y) {
        if (typeof y !== "undefined") {
          return y + "%";
        }
        return y;
      },
    },
  },
  markers: {
    size: 0,
  },
  fill: {
    opacity: 1
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
    title: {
      text: "فراوانی موضوع",
    },
    min:0,
    },
  xaxis: {
    // categories: ['ماه قبل', 'دو ماه قبل', 'سه ماه قبل', 'چهار ماه قبل', 'پنج ماه قبل', 'شش ماه قبل'],
    // type:'datetime',
    // tickAmount: 2,
    title: {
      text: "زمان",
    },
  },
  forecastDataPoints: {
    count: 4
  },
};


const CollectionARIMAChart = ({userId}) => {
  const [series, setSeries] = useState([{ name: "موضوع ", data: [] }]);
  const [stabilities, setStabilities] = useState([]);
  const [trends, setTrends] = useState([]);
  const [topics, setTopics] = useState([]);
  useEffect(() => {
    getSeries(7)
  }, []);



  function getSeries(length) {
    let requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };
    fetch(baseURL + "tweet/get_collection_ARIMA_chart/" + length.toString() + "/", requestOptions)
      .then(response => response.text())
      .then(result => {
        let temp = JSON.parse(result);
        console.log(temp)
        // let series = [];
        // series.push({ data: temp.data });
        setSeries(temp.data);
        setStabilities(temp.stabilities);
        setTopics(temp.important_topics);
        setTrends(temp.trends);
      })
      .catch(error => console.log('error', error));

  }

  const handleChange = (value) => {
   getSeries(value)
  };

  return (
    <div className={'d-flex flex-column'} dir={"ltr"} id="chart1">
      <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
        <span>{stabilities}</span>
      </div>
      <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
        <h6 className={'my-auto'}>کلمات احتمالی ترند: </h6>
        <span>{topics}</span>
      </div>
      <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
        <h6 className={'my-auto'}>کلمات ترند اصلی: </h6>
        <span>{trends}</span>
      </div>
      <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
        <h6 className={'my-auto'}>نمودار فراوانی موضوعات در هر </h6>
        <Select
          id={'selectvalue3'}
          defaultValue="7"
          bordered={false}
          onChange={handleChange}
        >
          {/*<Option value="1">روز</Option>*/}
          <Option value="7">هفته</Option>
        </Select>
      </div>
      <ReactApexChart
        options={options}
        series={series}
        height={600}
        // xaxis={}
      />
    </div>
  );
};

export default CollectionARIMAChart;
