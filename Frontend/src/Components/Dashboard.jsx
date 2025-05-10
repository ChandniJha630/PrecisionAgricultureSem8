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
      Temperature: data.main.temp,
      Humidity: data.main.humidity,
      Rain: data.rain ? data.rain["1h"] || 0 : 0,
      CreatedAt: new Date().toISOString(), // Match WeatherCard's expected field
    };

    setWeatherStationData(formatted); // Ensure this function is defined in your component
  } catch (err) {
    console.error("Error fetching weather station data:", err);
  }
};


  // Fetch Local Weather Data
  const fetchLocalWeatherData = async () => {
    try {
      const response = await fetch('http://localhost:5000/local-weather');
      const data = await response.json();
      console.log('Weather:', data);
  
      const formatted = {
        Temperature: data.Temperature,
        Humidity: data.Humidity,
        Rain: data.Rain,
        CreatedAt: data.CreatedAt,
      };
  
      setLocalData(formatted);
    } catch (error) {
      console.error('Error fetching local weather data:', error);
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
    <div className="flex flex-row md:flex-row justify-left gap-1 p-2">
      <WeatherCard title="Weather Station" data={weatherStationData} />
      <WeatherCard title="Local Weather" data={localData} />
      {/* <WeatherCard title="Predicted Weather" data={predictedData} /> */}
    </div>
  );
};

export default Dashboard;
