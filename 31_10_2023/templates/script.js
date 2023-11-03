// Lấy dữ liệu từ API
function fetchData() {
  fetch("/get_all_data")
      .then(response => response.json())
      .then(data => {
          // Lấy các phần tử HTML cần thay đổi
          const lampStatus = document.getElementById("lamp-status");
          const sirenStatus = document.getElementById("siren-status");
          const vibrationStatus = document.getElementById("vibration-status");
          const relayStatus = document.getElementById("relay-status");
          const led1Status = document.getElementById("led1-status");
          const led2Status = document.getElementById("led2-status");
          const temperature = document.getElementById("temperature");
          const humidity = document.getElementById("humidity");
          const LightSensor = document.getElementById("light-sensor");
          const DistanceSensor = document.getElementById("distance-sensor");
          const current_time = document.getElementById("current-time");

          // Cập nhật các phần tử dựa trên dữ liệu từ API
          lampStatus.className = data.lamp ? "lamp-on" : "lamp-off";
          sirenStatus.className = data.siren ? "siren-on" : "siren-off";
          vibrationStatus.style.backgroundColor = data.vibration ? "green" : "#c8c8c8";
          relayStatus.style.backgroundColor = data.relay ? "green" : "#c8c8c8";
          led1Status.style.backgroundColor = data.led1_status ? "green" : "#c8c8c8";
          led2Status.style.backgroundColor = data.led2_status ? "green" : "#c8c8c8";
          temperature.textContent =  `${data.temp}`;
          humidity.textContent = ` ${data.humi}`;
          LightSensor.textContent = ` ${data.Light_Sensor}`;
          DistanceSensor.textContent = ` ${data.Distance_Sensor}`;
          current_time.textContent = ` ${data.timestamp}`;
      });
}

fetchData();
setInterval(fetchData, 1000);
