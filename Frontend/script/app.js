'use strict';

//#region *** Globabele variabelen
const drawChartTemperatuur = function (labels, data) {
  var options = {
    chart: {
      id: 'myChart',
      type: 'area',
      toolbar: {
        show: false
      },
      width: '90%',
      background: '#FFFFFF'
    },
    stroke: {
      curve: 'smooth',
    },
    dataLabels: {
      enabled: false,
    },
    series: [
      {
        name: 'Temperatuur',
        data: data,
      },
    ],
    labels: labels,
    noData: {
      text: 'Loading...',
    },
    xaxis: {
      labels : {
        show: false,
      },
      axisTicks: {
        show: false
      },
      axisBorder: {
        show: true,
        color: '#000000',
        height: 2,
        offsetX: 0,
        offsetY: 0
      }
    },
    yaxis: {
      labels : {
        show: false ,
      },
      axisBorder: {
        show: true,
        color: '#000000',
        height: 2,
        offsetX: -3,
        offsetY: 0
      },
      title: {
        text: 'Graden Celcius',
        rotate: -90,
      }
    },
    zoom: {
      show : false
    },
    grid: {
      show: false
    },
    
  };

  var chart = new ApexCharts(document.querySelector('.js-chartTemperatuur'), options);
  chart.render();
};

const drawChartVerbruik = function (labels, data) {
  var options = {
    chart: {
      id: 'myChart',
      type: 'area',
      toolbar: {
        show: false
      },
      width: '90%',
      background: '#FFFFFF'
    },
    stroke: {
      curve: 'smooth',
    },
    dataLabels: {
      enabled: false,
    },
    series: [
      {
        name: 'Verbruik',
        data: data,
      },
    ],
    labels: labels,
    noData: {
      text: 'Loading...',
    },
    xaxis: {
      labels : {
        show: false,
      },
      axisTicks: {
        show: false
      },
      axisBorder: {
        show: true,
        color: '#000000',
        height: 2,
        offsetX: 0,
        offsetY: 0,
      }
    },
    yaxis: {
      labels : {
        show: false,
      },
      axisBorder: {
        show: true,
        color: '#000000',
        height: 2,
        offsetX: -3,
        offsetY: 0
      },
      title: {
        text: 'Wattage',
        rotate: -90,
      }
    },
    zoom: {
      show : false
    },
    grid: {
      show: false
    }
  };

  var chart = new ApexCharts(document.querySelector('.js-chartVerbruik'), options);
  chart.render();
}

const drawChartVerbruikFull = function (labels, data) {
  var options = {
    chart: {
      id: 'myChart',
      type: 'area',
      toolbar: {
        show: true,
        offsetX: 0,
        offsetY: 0,
        tools: {
          download: true,
          selection: true,
          zoom: true,
          zoomin: true,
          zoomout: true,
          pan: true,
        }
      },
      width: '90%',
      background: '#FFFFFF'
    },
    stroke: {
      curve: 'smooth',
    },
    dataLabels: {
      enabled: false,
    },
    series: [
      {
        name: 'Verbruik',
        data: data,
      },
    ],
    labels: labels,
    noData: {
      text: 'Loading...',
    },
    xaxis: {
      labels : {
        show: true,
        maxHeight: 250
      },
      axisTicks: {
        show: false
      },
      axisBorder: {
        show: true,
        color: '#000000',
        height: 2,
        offsetX: 0,
        offsetY: 0,
      },
    },
    yaxis: {
      labels : {
        show: true
      },
      axisBorder: {
        show: true,
        color: '#000000',
        height: 2,
        offsetX: -3,
        offsetY: 0
      },
      title: {
        text: 'Wattage',
        rotate: -90,
      }
    },
    zoom: {
      show : false
    },
    grid: {
      show: false
    }
  };

  var chart = new ApexCharts(document.querySelector('.js-chart--verbruik'), options);
  chart.render();
}

const drawChartTemperatuurFull = function (labels, data) {
  var options = {
    chart: {
      id: 'myChart',
      type: 'area',
      toolbar: {
        show: true,
        offsetX: 0,
        offsetY: 0,
        tools: {
          download: true,
          selection: true,
          zoom: true,
          zoomin: true,
          zoomout: true,
          pan: true,
        }
      },
      width: '90%',
      background: '#FFFFFF'
    },
    stroke: {
      curve: 'smooth',
    },
    dataLabels: {
      enabled: false,
    },
    series: [
      {
        name: 'Temperatuur',
        data: data,
      },
    ],
    labels: labels,
    noData: {
      text: 'Loading...',
    },
    xaxis: {
      labels : {
        show: true,
        maxHeight: 250,
      },
      axisTicks: {
        show: false
      },
      axisBorder: {
        show: true,
        color: '#000000',
        height: 2,
        offsetX: 0,
        offsetY: 0
      }
    },
    yaxis: {
      labels : {
        show: true
      },
      axisBorder: {
        show: true,
        color: '#000000',
        height: 2,
        offsetX: -3,
        offsetY: 0
      },
      title: {
        text: 'Graden Celcius',
        rotate: -90,
      }
    },
    zoom: {
      show : false
    },
    grid: {
      show: false
    },
    
  };

  var chart = new ApexCharts(document.querySelector('.js-chart--Temperatuur'), options);
  chart.render();
};

//#endregion

//#region *** DOM References

let htmlIndex, htmlTemperatuur, htmlLuchtkwaliteit, htmlVerbruik;
let htmlStopcontacten;

let htmlHistoriek;

let htmlHistoriekVerbruik;
let htmlHistoriekVerbruikStart, htmlHistoriekVerbruikStop, htmlHistoriekVerbruikButton;

let htmlHistoriekTemperatuur;
let htmlHistoriekTemperatuurStart, htmlHistoriekTemperatuurStop, htmlHistoriekTemperatuurButton;

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
//#endregion

//#region ***  Callback-Visualisation - show___         ***********

const showTemperature = function(jsonObject){
  console.log(jsonObject)
  htmlTemperatuur.innerHTML = `${jsonObject.temp} °C`
}

const showAirquality = function(jsonObject){
  console.log(jsonObject)
  htmlLuchtkwaliteit.innerHTML = `${jsonObject.air_quality}`
}

const showStopcontacten = function(jsonObject){
  console.log("show stopcontacten")
  console.log(jsonObject)

  for (let stopcontact of jsonObject){
    console.log(`stopcontact: ${stopcontact.actuatorId}      status: ${stopcontact.status_actuator}`)
    const stopcontact_html = document.querySelector(`.js-stopcontact[data-idstopcontact="${stopcontact.actuatorId}"]`)
    if (stopcontact_html)
    {
      const knop = stopcontact_html.querySelector(`.js-power-btn`)
      knop.dataset.statusstopcontact = stopcontact.status_actuator

      if (stopcontact.status_actuator == 0){
        let svgAan = stopcontact_html.querySelector('.js-stopcontact--aan')
        if (svgAan.classList.contains("c-show__stopcontact"))
        {
          svgAan.classList.remove("c-show__stopcontact")
        }
        let svgUit = stopcontact_html.querySelector('.js-stopcontact--uit')
        svgUit.classList.add("c-show__stopcontact")
        
        
        knop.classList.remove("c-power-btn--on")
      }
      else if (stopcontact.status_actuator == 1){
        let svgUit = stopcontact_html.querySelector('.js-stopcontact--uit')
        if (svgUit.classList.contains("c-show__stopcontact")){
          svgUit.classList.remove("c-show__stopcontact")
        }
        let svgAan = stopcontact_html.querySelector('.js-stopcontact--aan')
        svgAan.classList.add("c-show__stopcontact")
        
        

        knop.classList.add("c-power-btn--on")
      }
    }
  }
  
}

const showHisTemperatuur = function(jsonObject){
  console.log(jsonObject)

  let converted_labels = []
  let converted_data = []
  for (let info of jsonObject)
  {
    console.log(info)
    converted_labels.push(info.datum)
    converted_data.push(info.waarde_sensor)
  }
  drawChartTemperatuur(converted_labels, converted_data)
}

const showVerbruik = function(jsonObject){
  console.log(jsonObject.verbruik[0].waarde_sensor)
  htmlVerbruik.innerHTML = `${Math.round(jsonObject.verbruik[0].waarde_sensor) } W`
}

const showHisVerbruik = function(jsonObject){
  console.log(jsonObject)

  let converted_labels = []
  let converted_data = []
  for (let info of jsonObject)
  {
    console.log(info)
    converted_labels.push(info.datum)
    converted_data.push(info.waarde_sensor)
  }
  drawChartVerbruik(converted_labels, converted_data)
}

const showGrafiekVerbruik = function(jsonObject){

  let converted_labels = []
  let converted_data = []

  for (let info of jsonObject)
  {
    converted_labels.push(info.datum)
    converted_data.push(info.waarde_sensor)
  }
  drawChartVerbruikFull(converted_labels, converted_data)
}

const showGrafiekTemperatuur = function(jsonObject){

  let converted_labels = []
  let converted_data = []

  for (let info of jsonObject)
  {
    converted_labels.push(info.datum)
    converted_data.push(info.waarde_sensor)
  }
  drawChartTemperatuurFull(converted_labels, converted_data)
}
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***********
//#endregion

//#region ***  Data Access - get___                     ***********

const getTemperature = function() {
  handleData(`http://${lanIP}/api/v1/read_temperature`, showTemperature)
}

const getAirquality = function() {
  handleData(`http://${lanIP}/api/v1/read_airquality`, showAirquality)
}

const getStopcontacten = function() {
  handleData(`http://${lanIP}/api/v1/read_stopcontacten`, showStopcontacten)
}

const getHisTemperatuur = function() {
  handleData(`http://${lanIP}/api/v1/historiek_last_day/2`, showHisTemperatuur)
}

const getHisVerbruik = function() {
  handleData(`http://${lanIP}/api/v1/historiek_last_day/3`, showHisVerbruik)
}

const getVerbruik = function() {
  handleData(`http://${lanIP}/api/v1/read_verbruik`, showVerbruik)
}
//#endregion


//#region ***  Event Listeners - listenTo___            ***********
const listenToUI = function () {
  const knoppen = document.querySelectorAll('.js-power-btn')
  for (const knop of knoppen){
    knop.addEventListener("click", function(){
      console.log("Er is geklikt")
      const id = this.dataset.idstopcontact
      let nieuweStatus;
      if (this.dataset.statusstopcontact == 0){
        nieuweStatus = 1
      }
      else {
        nieuweStatus = 0
      }
      console.log("Er is geklikt")
      console.log(id)
      console.log(this.dataset.statusstopcontact)
      document.querySelector(`.js-stopcontact[data-idstopcontact="${id}"]`).classList.add("c-room--wait");
      socket.emit("F2B_switch_stopcontact", { relay_id: id, new_status: nieuweStatus });
    })
  }

};

const listenToSocket = function () {
  socket.on('B2F_information_temp', function(msg) {
    console.log(msg)
    console.log(msg.temp)
    htmlTemperatuur.innerHTML = `${msg.temp} ° C`

  })

  socket.on('B2F_information_air_quality', function(msg){
    console.log(msg)
    console.log(msg.air_quality)
    htmlLuchtkwaliteit.innerHTML = `${msg.air_quality}`
  })

  socket.on('B2F_verandering_stopcontact', function (msg) {
    console.log("Er is een status van een stopcontact veranderd");
    console.log(msg.relayid);
    console.log(msg.relaystatus)

    const stopcontact = document.querySelector(`.js-stopcontact[data-idstopcontact="${msg.relayid}"]`);
    if (stopcontact) {
      const knop = stopcontact.querySelector(".js-power-btn"); //spreek de stopcontact, als start. Zodat je enkel knop krijgt die in de stopcontanct staat
      knop.dataset.statusstopcontact = msg.relaystatus;

      if (msg.relaystatus == 0){
        let svgAan = stopcontact.querySelector('.js-stopcontact--aan')
        svgAan.classList.remove("c-show__stopcontact")
        let svgUit = stopcontact.querySelector('.js-stopcontact--uit')
        svgUit.classList.add("c-show__stopcontact")

        knop.classList.remove("c-power-btn--on")
      }
      else if (msg.relaystatus == 1){
        let svgAan = stopcontact.querySelector('.js-stopcontact--aan')
        svgAan.classList.add("c-show__stopcontact")
        let svgUit = stopcontact.querySelector('.js-stopcontact--uit')
        svgUit.classList.remove("c-show__stopcontact")

        knop.classList.add("c-power-btn--on")
      }
    }
  });

  socket.on('B2F_information_verbruik', function(msg){
    console.log(msg)

    htmlVerbruik.innerHTML = `${msg.verbruik } W`
  })
};

const ListenToEventsVerbruik = function (){
  htmlHistoriekVerbruikButton.addEventListener('click', function(){
    console.log("Er is geklikt")
    const start_datum = htmlHistoriekVerbruikStart.value
    const stop_datum = htmlHistoriekVerbruikStop.value
    
    console.log(start_datum)

    handleData(`http://${lanIP}/api/v1/historiek_time/3/${start_datum}/${stop_datum}`, showGrafiekVerbruik)

  })
}

const ListenToEventsTemperatuur = function (){
  htmlHistoriekTemperatuurButton.addEventListener('click', function(){
    console.log("Er is geklikt")
    const start_datum = htmlHistoriekTemperatuurStart.value
    const stop_datum = htmlHistoriekTemperatuurStop.value

    handleData(`http://${lanIP}/api/v1/historiek_time/2/${start_datum}/${stop_datum}`, showGrafiekTemperatuur)

  })
}
//#endregion

//#region *** Toggle Nav ************
const toggleNav = function(){
  let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
  for (let i = 0; i < toggleTrigger.length; i++) {
    toggleTrigger[i].addEventListener("click", function() {
    console.log("ei");
    document.querySelector("body").classList.toggle("has-mobile-nav");
    })
  }
}
//#endregion

//#region ***  Init / DOMContentLoaded                  ***********
const init = function () {
  htmlIndex = document.querySelector('.js-index');
  htmlTemperatuur = document.querySelector('.js-temperatuur');
  htmlLuchtkwaliteit = document.querySelector('.js-luchtkwaliteit');
  htmlStopcontacten = document.querySelectorAll('.js-stopcontact')
  htmlVerbruik = document.querySelector('.js-verbruik')
  htmlHistoriek = document.querySelector('.js-historiek')
  htmlHistoriekVerbruik = document.querySelector('.js-pagina--verbruik')
  htmlHistoriekVerbruikStop = document.querySelector('.js-verbruik-stop')
  htmlHistoriekVerbruikStart = document.querySelector('.js-verbruik-start')
  htmlHistoriekVerbruikButton = document.querySelector('.js-verbruik-btn')
  htmlHistoriekTemperatuur = document.querySelector('.js-pagina--temperatuur')
  htmlHistoriekTemperatuurStop = document.querySelector('.js-temperatuur-stop')
  htmlHistoriekTemperatuurStart = document.querySelector('.js-temperatuur-start')
  htmlHistoriekTemperatuurButton = document.querySelector('.js-temperatuur-btn')

  if(htmlIndex){
    getTemperature();
    getAirquality();
    getVerbruik();
    getStopcontacten();
    listenToSocket();
  }

  if(htmlHistoriek){
    getHisTemperatuur();
    getHisVerbruik();
  }

  if(htmlHistoriekVerbruik){
    htmlHistoriekVerbruikButton.disabled = false

    ListenToEventsVerbruik()
  }
  if(htmlHistoriekTemperatuur){
    htmlHistoriekTemperatuurButton.disabled = false

    ListenToEventsTemperatuur()
  }

  listenToUI();
  
  toggleNav();
  
};

document.addEventListener('DOMContentLoaded', function () {
  console.log('Dom content loaded');
  console.log(lanIP)
  init();
});
//#endregion
