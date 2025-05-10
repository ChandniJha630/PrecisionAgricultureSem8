import React from 'react';
import { FaTemperatureHigh, FaTint, FaCloudRain } from 'react-icons/fa';

const WeatherCard = ({ title, data }) => {
  if (!data) return <div>Loading...</div>;

  return (
    <div className="card bg-base-100 w-96 shadow-sm">
      <div className="card-body">
        <h2 className="card-title">{title}</h2>
        <p><FaTemperatureHigh /> Temperature: {data.temperature}°C</p>
        <p><FaTint /> Humidity: {data.humidity}%</p>
        <p><FaCloudRain /> Rain: {data.rain} mm</p>
      </div>
    </div>
  );
};

export default WeatherCard;
