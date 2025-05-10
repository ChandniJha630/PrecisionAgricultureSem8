import React from 'react';
import { FaTemperatureHigh, FaTint, FaCloudRain } from 'react-icons/fa';

const WeatherCard = ({ title, data }) => {
  if (!data) return <div>Loading...</div>;

  const formattedDate = new Date(data.CreatedAt).toLocaleString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  });

  return (
    <div className="card bg-base-100 w-96 shadow-sm">
      <div className="card-body">
        <h2 className="card-title">{title}</h2>
        <p><FaTemperatureHigh /> Temperature: {data.Temperature}°C</p>
        <p><FaTint /> Humidity: {data.Humidity}%</p>
        <p><FaCloudRain /> Rain: {data.Rain} mm</p>
        <p><strong>Recorded At:</strong> {formattedDate}</p>
      </div>
    </div>
  );
};

export default WeatherCard;
