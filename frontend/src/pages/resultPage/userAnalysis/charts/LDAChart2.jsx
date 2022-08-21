import { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";
import { Select } from 'antd';
import {baseURL} from "../../../../components/config";

const { Option } = Select;

let options1 = {
  chart: {
    type: 'line',
    zoom: {
      enabled: false
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'straight'
  },
  grid: {
    borderColor: '#e7e7e7',
    row: {
      colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
      opacity: 0.5
    },
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
      text: "آنتروپی",
    },
  },
  xaxis: {
    title: {
      text: "زمان",
    },
  },
}

let options2 = {
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
};


const LDAChart2 = ({userId}) => {
  const [series, setSeries] = useState([{ name: "موضوع ", data: [] }]);
  const [entropy, setEntropy] = useState('');
  const [entropies, setEntropies] = useState([{ name: "آنتروپی ", data: [] }]);

  useEffect(() => {
    getSeries(30)
  }, []);



  function getSeries(length) {
    let requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };
    fetch(baseURL + "tweet/get_user_LDA_chart2_by_id/" + userId.toString() + "/" + length.toString() + "/", requestOptions)
      .then(response => response.text())
      .then(result => {
        let temp = JSON.parse(result);
        console.log(temp)
        // let series = [];
        // series.push({ data: temp.data });
        setSeries(temp.data);
        setEntropy(temp.entropy_avg);
        setEntropies(temp.entropies);
      })
      .catch(error => console.log('error', error));

  }

  const handleChange = (value) => {
   getSeries(value)
  };

  return (
    <div className={'d-flex flex-column'} dir={"ltr"} id="chart1">
      <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
        <h6 className={'my-auto'}>آنتروپی میانگین کاربر: </h6>
        <span>{entropy}</span>
      </div>
      <ReactApexChart
        options={options1}
        series={entropies}
        height={200}
        // xaxis={}
      />
      <br/>
      <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
        <h6 className={'my-auto'}>نمودار فراوانی موضوع در هر </h6>
        <Select
          id={'selectvalue2'}
          defaultValue="30"
          bordered={false}
          onChange={handleChange}
        >
          <Option value="30">ماه</Option>
          <Option value="7">هفته</Option>
        </Select>
      </div>
      <ReactApexChart
        options={options2}
        series={series}
        height={600}
        // xaxis={}
      />
    </div>
  );
};

export default LDAChart2;
