import axios from 'axios';
import { Chart } from 'react-google-charts';
import { useState, useEffect } from 'react';


const StockChart = ({ symbol }) => {

  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (symbol !== '$CASH') getChartData();
  }, []);

  const getChartData = async () => {
    const response = await axios.get(`/stock/chart/${symbol}`);
    const data = response.data.map((point) => {
      const date = new Date(point.date);
      const dateString = `${date.getMonth() + 1}/${date.getDate()}`;
      return [dateString, point.volume / 1000000, point.close];
    });
    setChartData([['Date', 'Volume', 'Closing Price'], ...data]);
  }

  const chartOptions = {
    title: `${symbol} 3-month Closing Price Chart`,
    series: {
      0: { type: "bars", axis: "Volume", targetAxisIndex: 0 },
      1: { type: "line", axis: "Price", targetAxisIndex: 1 }
    },
    vAxes: {
      0: { logScale: false, title: "Volume (millions)" },
      1: { logScale: false, title: "Price", minValue: 0 }
    },
    legend: { position: "none" },
  };

  return (
    <Chart
      chartType="ComboChart"
      width="450px"
      height="100%"
      data={chartData}
      options={chartOptions}
    />
  );
}

export default StockChart;