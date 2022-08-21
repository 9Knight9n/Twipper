import React, {useState,useEffect} from 'react';
import { Avatar, List, Space } from 'antd';
import { useNavigate, useParams } from "react-router-dom";
import './collectionAnalysis.css'
import ReactApexChart from "react-apexcharts";
import { Select, Table } from 'antd';
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
    count: 6
  },
};

const columns = [
  {
    title: 'Topic number',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Stability',
    dataIndex: 'stability',
    key: 'stability',
  },
  {
    title: 'Train loss',
    dataIndex: 'train_loss',
    key: 'train_loss',
  },
  {
    title: 'Validation loss',
    dataIndex: 'val_loss',
    key: 'val_loss',
  },
];


function CollectionAnalysis(props) {
    const [series, setSeries] = useState([{ name: "موضوع ", data: [] }]);
    const [stabilities, setStabilities] = useState([]);
    const [tableData, setTableData] = useState([]);
    const [correlation, setCorrelation] = useState([]);
    const [trends, setTrends] = useState([]);
    const [topics, setTopics] = useState([]);
    const [trainLoss, setTrainLoss] = useState(0);
    const [valLoss, setValLoss] = useState(0);
    let params = useParams();


    useEffect(() => {
        getSeries();
        getTable()
    }, []);


  function getSeries() {
    let requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };
    fetch(baseURL + "tweet/get_collection_ARIMA_chart/" + params.collection + "/", requestOptions)
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
        setTrainLoss(temp.train_loss);
        setValLoss(temp.val_loss);
      })
      .catch(error => console.log('error', error));

  }

  function getTable() {
    let requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };
    fetch(baseURL + "tweet/get_table_correlation/" + params.collection + "/", requestOptions)
      .then(response => response.text())
      .then(result => {
        let temp = JSON.parse(result);
        console.log(temp)
        // let series = [];
        // series.push({ data: temp.data });
        setTableData(temp.data);
        setCorrelation(temp.correlation)
      })
      .catch(error => console.log('error', error));
  }


  const handleChange = (value) => {
   getSeries(value)
  };

    return (
        <div className={'main-container-md'}>
            {/*<Menu/>*/}
            {/*<br/>*/}
            {/*<br/>*/}
            <div className={'d-flex flex-column'} dir={"ltr"} id="chart1">
              <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
                <h5 className={'my-auto'}>کلمات احتمالی ترند: </h5>
              </div>
              <div className={'d-flex flex-row mx-auto'} dir={'ltr'}>
                <span>{topics}</span>
              </div>
              <br/>
              <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
                <h5 className={'my-auto'}>کلمات ترند اصلی: </h5>
              </div>
              <div className={'d-flex flex-row mx-auto'} dir={'ltr'}>
                <span>{trends}</span>
              </div>
              <br/>
              <div className={'d-flex flex-row mx-auto'} dir={'rtl'}>
                <h5 className={'my-auto'}>پایداری موضوعات: </h5>
              </div>
              {
                stabilities.map((s) => (
                    <div className={'d-flex flex-row mx-auto'}>
                      <h5 className={'my-auto'}>{s.name}:{s.stability}</h5>
                    </div>
                ))
              }
              <br/>
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
              <div className={'d-flex flex-row mx-auto'}>
                <h5 className={'my-auto'}>train mean abstract error:{trainLoss}</h5>
              </div>
              <div className={'d-flex flex-row mx-auto'}>
                <h5 className={'my-auto'}>validation mean abstract error:{valLoss}</h5>
              </div>
              <br/>
              <Table columns={columns} dataSource={tableData} />
              <br/>
              {
                correlation.map((s) => (
                    <div className={'d-flex flex-row mx-auto'}>
                      <h5 className={'my-auto'}>{s.name}:{s.value}</h5>
                    </div>
                ))
              }
              <br/>
              <br/>
            </div>
        </div>

    );
}

export default CollectionAnalysis;
