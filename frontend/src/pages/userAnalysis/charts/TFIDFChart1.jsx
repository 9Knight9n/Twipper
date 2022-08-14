import { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";
import { DatePicker,ConfigProvider } from 'antd';
import {baseURL} from "../../../components/config";
import locale from 'antd/es/locale/fa_IR';
import moment from 'moment';

const { RangePicker } = DatePicker;


let options = {
  chart: {
    // type: "treemap",
  },
  dataLabels: {
    enabled: true,
    style: {
      fontSize: '12px',
    },
    formatter: function(text, op) {
      return [text, op.value.toString()+"%"]
    },
    offsetY: -4
  },

  tooltip: {
    shared: true,
    intersect: false,
    x:{
      show: true,
      // formatter: function (x) {
      //   if (typeof x !== "undefined") {
      //     return x + "wdw%";
      //   }
      //   return x;
      // },
    },
    y: {
      title: {
          formatter: (seriesName) => "TF :",
      },
      formatter: function (y) {
        if (typeof y !== "undefined") {
          return y + "%";
        }
        return y;
      },
    },
    z: {
      title: "فراوانی :",
    }
  },
  // markers: {
  //   size: 0,
  // },
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
};


const TFIDFChart1 = ({userId}) => {
  const [series, setSeries] = useState([{ unique:0, data: [] }]);

  useEffect(() => {
    getSeries(moment().subtract(6, 'months').format('DD-MM-YY'),moment().format('DD-MM-YY'))
  }, []);

  // useEffect(() => {
  //   getSeries(document.getElementById('selectvalue1').valueOf())
  // }, [userId]);


  function getSeries(start,stop) {
    let requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };
    fetch(baseURL + "tweet/get_user_TF_chart1_by_id/" + userId.toString() + "/" + start + "/" + stop + "/", requestOptions)
      .then(response => response.text())
      .then(result => {
        let temp = JSON.parse(result);
        console.log(temp)
        let series = [];
        series.push({ data: temp.data, unique: temp.unique });
        setSeries(series);
      })
      .catch(error => console.log('error', error));

  }

  const handleChange = ([value1,value2]) => {
   getSeries(value1.format('DD-MM-YY'),value2.format('DD-MM-YY'))
  };

  return (
    <div className={'d-flex flex-column'} dir={"ltr"} id="chart1">
      <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
        <h6 className={'my-auto'}>میزان فراوانی کلمات در بازه </h6>
        <ConfigProvider locale={locale} direction={'rtl'}>
          <RangePicker
              // defaultPickerValue={[moment().subtract(6, 'months'),moment()]}
              defaultValue={[moment(),moment().subtract(6, 'months')]}
              placement={'bottomLeft'}
              onChange={handleChange}
              bordered={false}/>
        </ConfigProvider>
      </div>
      <ReactApexChart
        options={options}
        series={series}
        type={'treemap'}
        height={385}
      />
      <h6 className={'m-auto'} dir={'rtl'}>
        تعداد کلمات متمایز در بازه انتخاب شده
        {"  "+series[0].unique.toString()+"  "}
        می باشد
        .
      </h6>
    </div>
  );
};

export default TFIDFChart1;
