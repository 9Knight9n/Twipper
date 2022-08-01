import React from 'react';
import ApexChart from "react-apexcharts";

function Chart(props) {

    // const options= {
    //     chart: {
    //         id: "basic-bar"
    //     },
    //     xaxis: {
    //         categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
    //     }
    // },
    // series= [
    //     {
    //         name: "series-1",
    //         data: [30, 40, 45, 50, 49, 60, 70, 91]
    //     }
    // ]

    const options= {
        chart: {
          type: 'bar',
          height: 350,
          stacked: true,
          stackType: '100%'
        },
        xaxis: {
          categories: ['2011 Q1', '2011 Q2', '2011 Q3', '2011 Q4', '2012 Q1', '2012 Q2',
            '2012 Q3', '2012 Q4'
          ],
        },
        fill: {
          opacity: 1
        },
        legend: {
          position: 'right',
          offsetX: 0,
          offsetY: 50
        },
    },
    series= [
        {
          name: 'PRODUCT A',
          data: [44, 55, 41, 67, 22, 43, 21, 49]
        },
                {
          name: 'PRODUCT D',
          data: [44, 55, 41, 67, 22, 43, 21, 49]
        },
                {
          name: 'PRODUCT g',
          data: [44, 55, 41, 67, 22, 43, 21, 49]
        },
                        {
          name: 'PRODUCT h',
          data: [44, 55, 41, 67, 22, 43, 21, 49]
        },
                        {
          name: 'PRODUCT i',
          data: [44, 55, 41, 67, 22, 43, 21, 49]
        },
                        {
          name: 'PRODUCT j',
          data: [44, 55, 41, 67, 22, 43, 21, 49]
        },
                        {
          name: 'PRODUCT k',
          data: [44, 55, 41, 67, 22, 43, 21, 49]
        },
                        {
          name: 'PRODUCT l',
          data: [44, 55, 41, 67, 22, 43, 21, 49]
        },
                {
          name: 'PRODUCT F',
          data: [44, 55, 41, 67, 22, 43, 21, 49]
        },
        {
          name: 'PRODUCT B',
          data: [13, 23, 20, 8, 13, 27, 33, 12]
        }, {
          name: 'PRODUCT C',
          data: [11, 17, 15, 15, 21, 14, 15, 13]
        }]

    return (
        <div className="mixed-chart">
            <ApexChart
                options={options}
                series={series}
                type="bar"
                width="100%"
            />
        </div>
    );
}

export default Chart;