import React, { useEffect, useState } from 'react';
import WeatherCard from './WeatherCard';

const Dashboard = () => {
  const [weatherStationData, setWeatherStationData] = useState(null);
  const [localData, setLocalData] = useState(null);
  const [predictedData, setPredictedData] = useState(null);

  // Fetching data on component mount
  useEffect(() => {
    fetchWeatherStationData();
    fetchLocalWeatherData();
    fetchPredictedWeatherData();
  }, []);

  // Fetch Weather Station Data
  const fetchWeatherStationData = async () => {
    try {
      const apiKey = "c763cc19dd77c522caa714fa9779cd9a";
      const city = "Kolkata";
      const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

      const response = await fetch(url);
      const data = await response.json();

      const formatted = {
        temperature: data.main.temp,
        humidity: data.main.humidity,
        rain: data.rain ? data.rain["1h"] || 0 : 0,
        timestamp: new Date().toLocaleString(),
      };

      setWeatherStationData(formatted);
    } catch (err) {
      console.error("Error fetching weather station data:", err);
    }
  };

  // Fetch Local Weather Data
  const fetchLocalWeatherData = async () => {
    try {
      const response = await fetch('/api/local-weather');
      const data = await response.json();

      setLocalData(data);
    } catch (err) {
      console.error("Error fetching local weather data:", err);
    }
  };

  // Fetch Predicted Weather Data
  const fetchPredictedWeatherData = async () => {
    try {
      const response = await fetch('/api/predicted-weather');
      const data = await response.json();

      setPredictedData(data);
    } catch (err) {
      console.error("Error fetching predicted weather data:", err);
    }
  };

  return (
    <div className="flex flex-col md:flex-row justify-center gap-6 p-8 bg-gray-50">
      <WeatherCard title="Weather Station" data={weatherStationData} />
      <WeatherCard title="Weather Station" data={weatherStationData} />
      <WeatherCard title="Weather Station" data={weatherStationData} />
      <WeatherCard title="Local Weather" data={localData} />
      <WeatherCard title="Predicted Weather" data={predictedData} />
    </div>
  );
};

export default Dashboard;
