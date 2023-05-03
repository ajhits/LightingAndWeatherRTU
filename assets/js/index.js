



const weather = function(){
    console.log("clicekc")
      $.ajax({
        url: "https://api.openweathermap.org/data/2.5/weather?lat=14.57&lon=121.08&appid=75f672498b1c1b9c3a0d06f08247ff2c", // Replace with the URL of your Flask route
        //url: "static/weather.json",
        type: "GET", // Replace with the HTTP method of your Flask route
        data: { /* Replace with any data you need to send to the server */ },
            success: function(response) {
            
            // Today's Date
            const day = new Date(response.dt * 1000);
            const formattedDate = day.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
            
            document.getElementById("DateNow").innerHTML = formattedDate
            
          
            // humidity
            const Humidity = response.main.humidity;
            document.getElementById("Humid").innerHTML = Humidity + "%"
    
            // temperature
            const kelvin = response.main.temp;
            const temperature = (kelvin - 273.15).toFixed(1);
            document.getElementById("Temp").innerHTML = temperature + "°C"
        },
        error: function(xhr) {
            console.log(xhr.responseText); // Handle any errors that occur
        }
        });
    
    }
    
    
    // for porediction weather in the following hours
    const forecast  = function(){
    
      $.ajax({
        url: "https://api.openweathermap.org/data/2.5/forecast?lat=14.57&lon=121.08&appid=75f672498b1c1b9c3a0d06f08247ff2c", // Replace with the URL of your Flask route
        // url: "static/forecast.json",
        type: "GET", // Replace with the HTTP method of your Flask route
        data: { /* Replace with any data you need to send to the server */ },
            success: function(response) {
            
            
            const ids = ["1time","2time","3time","4time","5time","6time"];
    
            for (let i = 0; i < 6; i++) {
    
              // date
              const dt = response.list[i].dt;
              const formattedTime = new Date(dt * 1000)
                                    .toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })
                                    .replace(':00', '')
                                    .replace(/\s+/g, '')
                                    .toLowerCase();
    
              // weather
              const weatherDescripton = response.list[i].weather[0].description;
    
    
              // Temperature
              const kelvin = response.list[i].main.temp
              const temperature = (kelvin - 273.15).toFixed(1)
    
              // todays weather
              const todays = formattedTime + ": " + weatherDescripton + ", " + temperature + "°C"
    
              document.getElementById(ids[i]).innerHTML = todays
    
            }
    
        },
        error: function(xhr) {
            console.log(xhr.responseText); // Handle any errors that occur
        }
        });
    
    }
    
    // onload function
    window.onload = function() { 
      forecast();
      weather();
    }
    
    
    // var intervalId = setInterval(
    //     function() {
    
    //     $.ajax({
    //         url: "https://api.openweathermap.org/data/2.5/weather?lat=14.57&lon=121.08&appid=75f672498b1c1b9c3a0d06f08247ff2c", // Replace with the URL of your Flask route
    //         type: "GET", // Replace with the HTTP method of your Flask route
    //         data: { /* Replace with any data you need to send to the server */ },
    //             success: function(response) {
    //               console.log(response[0])
    //               //checkCapture(); //call this function in order to run routing
    //         },
    //         error: function(xhr) {
    //             console.log(xhr.responseText); // Handle any errors that occur
    //         }
    //     });
    
    
    //   }, 2000); // Check every 2 seconds
        