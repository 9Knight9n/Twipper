import { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";

const TweetCountChart1 = (parameters) => {
  const [options, setOptions] = useState({});
  const [series, setSeries] = useState([{ name: "z-score", data: [] }]);

  useEffect(() => {
    let series = [];
    let data = [{x:1996,y:25},{x:1997,y:29},{x:1998,y:19},{x:1999,y:24},{x:2000,y:25},{x:2001,y:23},{x:2002,y:25},]
    series.push({ data: data });
    setSeries(series);
    let options = {
      chart: {
        type: "line",
        zoom: {
          enabled: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        curve: "straight",
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
        // z: {
        //   title: "سرعت: ",
        // },
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
      title: {
        text: "مقایسه سرعت راننده با سرعت معمول او",
        align: "center",
        margin: 0,
        offsetX: 0,
        offsetY: 0,
        floating: false,
        style: {
          fontSize: "20px",
          fontWeight: "normal",
          fontFamily: undefined,
          color: "#444444",
        },
      },
      yaxis: {
        labels: {
          offsetX: 0,
          offsetY: 0,
          rotate: 0,
        },
        title: {
          text: "z-score",
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
        tickAmount: 2,
        title: {
          text: "z-score",
          offsetX: 0,
          offsetY: 0,
          style: {
            fontSize: "18px",
            fontWeight: "normal",
            fontFamily: undefined,
            color: "#444444",
          },
        },
        // categories: labels,
      },
    };

    setOptions(options);
  }, []);
  return (
    <div dir={"ltr"} id="chart">
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
