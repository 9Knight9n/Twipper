import React from 'react';
import ApexChart from "react-apexcharts";

function TweetCountChart2(props) {

    const options= {
        chart: {
          // height: 350,
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
        title: {
          text: 'Product Trends by Month',
          align: 'left'
        },
        grid: {
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
        xaxis: {
            categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
        }
    },
    series= [
        {
            name: "series-1",
            data: [30, 40, 45, 50, 49, 60, 70, 91]
        }
    ]


    return (
        <div className="mixed-chart" dir={'ltr'}>
            <ApexChart
                options={options}
                series={series}
                type="line"
                width="100%"
            />
        </div>
    );
}

export default TweetCountChart2;