import { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";
import { Select } from 'antd';
import {baseURL} from "../../../../components/config";

const { Option } = Select;

let options = {
  colors : ['#C62828', '#AD1457','#4E342E', '#558B2F', '#4DB6AC', '#616161', '#6A1B9A','#D84315', '#4527A0', '#283593', '#1565C0', '#18FFFF', '#00838F', '#00695C',
    '#2E7D32', '#9E9D24', '#F9A825', '#FF8F00', '#EF6C00', '#37474F','#D84315'],
  chart: {
    stacked: true,
    stackType: '100%',
    // zoom: {
    //   enabled: true,
    // },
  },
  plotOptions: {
    bar: {
      horizontal: true,
    },
  },
  dataLabels: {
    enabled: true,
  },
  stroke: {
    width: 3,
    colors: ['#fff']
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
    // z: {
    //   title: "بازه زمانی :",
    // }
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
      text: "زمان",
      offsetX: 10,
      offsetY: 0,
      style: {
        fontSize: "18px",
        fontWeight: "normal",
        fontFamily: undefined,
        color: "#444444",
      },
    },
  },
  fill: {
    opacity: 1
  },
  xaxis: {
    categories: ['ماه قبل', 'دو ماه قبل', 'سه ماه قبل', 'چهار ماه قبل', 'پنج ماه قبل', 'شش ماه قبل'],
    // type:'datetime',
    // tickAmount: 2,
    title: {
      text: "فراوانی (درصد)",
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


const LDAChart1 = ({userId}) => {
  const [series, setSeries] = useState([{ name: "تعداد پیام ", data: [] }]);

  useEffect(() => {
    getSeries(30)
  }, []);



  function getSeries(length) {
    let requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };
    fetch(baseURL + "tweet/get_user_LDA_chart1_by_id/" + userId.toString() + "/" + length.toString() + "/", requestOptions)
      .then(response => response.text())
      .then(result => {
        let temp = JSON.parse(result);
        console.log(temp)
        // let series = [];
        // series.push({ data: temp.data });
        setSeries(temp.data);
      })
      .catch(error => console.log('error', error));

  }

  const handleChange = (value) => {
   getSeries(value)
  };

  return (
    <div className={'d-flex flex-column'} dir={"ltr"} id="chart1">
      <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
        <h6 className={'my-auto'}>نمودار فراوانی موضوع در هر </h6>
        <Select
          id={'selectvalue1'}
          defaultValue="30"
          bordered={false}
          onChange={handleChange}
        >
          {/*<Option value="7">هفته</Option>*/}
          <Option value="30">ماه</Option>
        </Select>
      </div>
      <ReactApexChart
        options={options}
        series={series}
        type='bar'
        height={385}
        // xaxis={}
      />
    </div>
  );
};

export default LDAChart1;
