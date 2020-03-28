// Change location to PEESE server later

//var dataFile = "https://cors-anywhere.herokuapp.com/http://akshayajagekar.com/covid19-ny/covid_data.csv";
var dataFile = "https://raw.githubusercontent.com/ajagekarakshay/covid19-ny/master/covid_data.csv";

var start_date = new Date(2020, 2, 2); // March 2
var today = new Date()
var ndays = Math.floor((today.getTime() - start_date.getTime()) / 86400000) ;



var maxValue = 30000; // Update automatically later

  am4core.useTheme(am4themes_animated);

  // main container
  var container = am4core.create("nymap", am4core.Container);
  container.width = am4core.percent(100);
  container.height = am4core.percent(100);
  container.background.fill = am4core.color("#FFFFFF");
  container.background.fillOpacity = 1;

    // Create map instance
    var chart = container.createChild(am4maps.MapChart);
    chart.seriesContainer.draggable = false;
    // Set map definition
    chart.geodata = am4geodata_region_usa_nyLow;
    
    // Set projection
    chart.projection = new am4maps.projections.Miller();
    
    // Create map polygon series
    var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

    // Make map load polygon (like country names) data from GeoJSON
    polygonSeries.useGeodata = true;

    // Configure series
    var polygonTemplate = polygonSeries.mapPolygons.template;
    polygonTemplate.stroke = am4core.color("#999");
    

    polygonTemplate.events.on("hit", function(ev) {
      //console.log(ev.target.dataItem);
      var data = ev.target.dataItem.dataContext;
      //console.log(data)
      lineChart.data = updateCountyData(data);
    });
    
    //polygonTemplate.fill = am4core.color("#999");
    
    // Create hover state and set alternative fill color
    var hs = polygonTemplate.states.create("hover");
    hs.properties.fill = am4core.color("#3498DB");
    

    //Set min/max fill color for each area
    polygonSeries.heatRules.push({
        "property": "fill",
        "target": polygonSeries.mapPolygons.template,
        "min": chart.colors.getIndex(1).lighten(0.8),
        "max": chart.colors.getIndex(1).brighten(-0.2),
        "minValue": 0,
        "maxValue": Math.log10(maxValue)
      });

    //  #2874A6
    //#084d96
    // legend
    var heatLegend = chart.createChild(am4maps.HeatLegend);
    heatLegend.series = polygonSeries;
    heatLegend.width = am4core.percent(100);
    heatLegend.orientation = "vertical";
    heatLegend.align = "left";
    heatLegend.dy = 80;
    heatLegend.dx = 20;

    // Set up custom heat map legend labels using axis ranges
    var minRange = heatLegend.valueAxis.axisRanges.create();
    minRange.label.VerticalCenter = "bottom";

    var maxRange = heatLegend.valueAxis.axisRanges.create();
    maxRange.label.VerticalCenter = "top";

    // Blank out internal heat legend value axis labels
    heatLegend.valueAxis.renderer.labels.template.adapter.add("text", function(labelText) {
      return "";
    });

    // Update heat legend value labels
polygonSeries.events.on("datavalidated", function(ev) {
  //var heatLegend = ev.target.map.getKey("heatLegend");

  var min = -2;
  var minRange = heatLegend.valueAxis.axisRanges.getIndex(0);
  minRange.value = min;
  minRange.label.text = "" + heatLegend.numberFormatter.format(0);

  var max = heatLegend.series.dataItem.values.value.high;
  var maxRange = heatLegend.valueAxis.axisRanges.getIndex(1);
  maxRange.value = max;
  maxRange.label.text = "" + heatLegend.numberFormatter.format(30000);
});
    // var minValue = 0;
    // minRange.value = minValue;
    // minRange.label.text = "" + heatLegend.numberFormatter.format(minValue);

    // maxRange.value = maxValue;
    // maxRange.label.text = "" + heatLegend.numberFormatter.format(Math.pow(10,maxValue));
    //heatLegend.markerCount = 3;
    
    //heatLegend.valueAxis.logarithmic = true;
    

    // polygonSeries.mapPolygons.template.events.on("over", function(ev) {
    //     if (!isNaN(ev.target.dataItem.value)) {
    //       heatLegend.valueAxis.tooltipText = 5;
    //       heatLegend.valueAxis.showTooltipAt(ev.target.dataItem.value);
          
    //     }
    //     else {
    //       heatLegend.valueAxis.hideTooltip();
    //     }
    //   });
      
    //   polygonSeries.mapPolygons.template.events.on("out", function(ev) {
    //     heatLegend.valueAxis.hideTooltip();
    //   });

  // buttons & chart container
  var buttonsAndChartContainer = container.createChild(am4core.Container);
  buttonsAndChartContainer.layout = "vertical";
  buttonsAndChartContainer.height = am4core.percent(3); // make this bigger if you want more space for the chart
  buttonsAndChartContainer.width = am4core.percent(100);
  buttonsAndChartContainer.valign = "top";

  // Chart & slider container
  var chartAndSliderContainer = buttonsAndChartContainer.createChild(am4core.Container);
  chartAndSliderContainer.layout = "vertical";
  chartAndSliderContainer.height = am4core.percent(100);
  chartAndSliderContainer.width = am4core.percent(100);
  chartAndSliderContainer.background.fill = am4core.color("#ffffff");
  chartAndSliderContainer.background = new am4core.RoundedRectangle();
  chartAndSliderContainer.background.cornerRadius(30, 30, 30, 30)
  chartAndSliderContainer.background.fillOpacity = 0.15;
  chartAndSliderContainer.background.fill = am4core.color("#ffffff");
  chartAndSliderContainer.paddingTop = 10;
  chartAndSliderContainer.paddingBottom = 0;

  // Slider container
  var sliderContainer = chartAndSliderContainer.createChild(am4core.Container);
  sliderContainer.width = am4core.percent(50);
  sliderContainer.padding(0, 15, 15, 10);
  sliderContainer.layout = "horizontal";
  sliderContainer.align = "center"
  

  var slider = sliderContainer.createChild(am4core.Slider);
  slider.width = am4core.percent(100);
  slider.valign = "middle";
  slider.background.opacity = 0.4;
  slider.opacity = 1;
  slider.background.fill = am4core.color("#000000");
  slider.marginLeft = 20;
  slider.marginRight = 35;
  slider.height = 15;
  slider.start = 0.5;
  slider.dy = 8;
  // slider.layout = "grid";
  // slider.fixedWidthGrid = true;
  // slider.maxColumns = 4;

  var sliderAnimation;
  // stop animation if dragged
  slider.startGrip.events.on("drag", () => {
    stop();
    if (sliderAnimation) {
      sliderAnimation.setProgress(slider.start);
    }
  });

  // play button
  var playButton = sliderContainer.createChild(am4core.PlayButton);
  playButton.valign = "middle";
  playButton.dx = -450;
  playButton.dy = 6;
  // play button behavior
  playButton.events.on("toggled", function(event) {
    if (event.target.isActive) {
      play();
    } else {
      stop();
    }
  })
  // make slider grip look like play button
  slider.startGrip.background.fill = playButton.background.fill;
  slider.startGrip.background.strokeOpacity = 0;
  slider.startGrip.icon.stroke = am4core.color("#ffffff");
  slider.startGrip.background.states.copyFrom(playButton.background.states)

  // play behavior
  function play() {
    if (!sliderAnimation) {
      sliderAnimation = slider.animate({ property: "start", to: 1, from: 0 }, 9000, am4core.ease.linear).pause();
      sliderAnimation.events.on("animationended", () => {
        playButton.isActive = false;
      })
    }

    if (slider.start >= 1) {
      slider.start = 0;
      sliderAnimation.start();
    }
    sliderAnimation.resume();
    playButton.isActive = true;
  }

  // stop behavior
  function stop() {
    if (sliderAnimation) {
      sliderAnimation.pause();
    }
    playButton.isActive = false;
  }

  var label = sliderContainer.createChild(am4core.Label);

  label.dy = -6;
  label.dx = 150;
  label.isMeasured = false;
  
  // var label2 = sliderContainer.createChild(am4core.Label);
  //   label2.dy =35;
  //   label2.dx = -225;
  //   label2.isMeasured = false;
  //   label2.text = "Log (N)"


  // Initialize
  var previousDate = start_date;
  var currentDay = Math.floor(slider.start * ndays);
  var currentDate = new Date(start_date.getTime() + currentDay*86400000);
  label.text = currentDate.toDateString().substring(4);

  //parseData();
  updateSeries(previousDate, currentDate);
  //heatLegend.valueAxis.max = Math.pow(10, heatLegend.valueAxis.max);
  
// Can use grid layout for slider (UPdate later or NOT)
slider.events.on("rangechanged", function(event) {
  previousDate = currentDate;
  currentDay = Math.floor(slider.start * ndays);
  currentDate = new Date(start_date.getTime() + currentDay*86400000);
  
  label.text = currentDate.toDateString().substring(4);

  updateSeries(previousDate, currentDate);

  //heatLegend.valueAxis.max = Math.pow(10, heatLegend.valueAxis.max);
  
})


function updateSeries(previousDate, currentDate) {
  if (previousDate.getTime() != currentDate.getTime()){

    Papa.parse(dataFile, {
    header: true,
    download:true,
    complete: function(results) {
    //console.log(JSON.stringify(results.data))

    var currentIndex = currentDate.getMonth()+1 + "/" + currentDate.getDate() + "/" + currentDate.getFullYear();

    // Set data from CSV file
    polygonSeries.data = results.data;
    polygonSeries.dataFields.value = currentIndex + "/ls";

    polygonTemplate.tooltipText = "[bold]{county}[/] (" + currentDate.toDateString().substring(4,10) + ")\nConfirmed Cases: {"+ currentIndex + "}";
    
    }
  });
}
}



var lineChart = am4core.create("countywise", am4charts.XYChart);

  lineChart.width = am4core.percent(100);
  lineChart.height = am4core.percent(100);
  lineChart.background.fill = am4core.color("#FFFFFF");
  lineChart.background.fillOpacity = 1;

    // Create xy chart instance
    lineChart.fontSize = "0.8em";
    lineChart.paddingRight = 30;
    lineChart.paddingLeft = 30;
    lineChart.paddingBottom=10;
    lineChart.paddingTop = 50;
    lineChart.maskBullets = false;
    lineChart.zoomOutButton.disabled = true;
  
    // date axis
    // https://www.amcharts.com/docs/v4/concepts/axes/date-axis/
    var dateAxis = lineChart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;
    // dateAxis.renderer.grid.template.stroke = am4core.color("#000000");
    // dateAxis.renderer.grid.template.strokeOpacity = 0.25;
    // dateAxis.tooltip.label.fontSize = "0.8em";
    // dateAxis.tooltip.background.fill = activeColor;
    // dateAxis.tooltip.background.stroke = activeColor;
    // dateAxis.renderer.labels.template.fill = am4core.color("#ffffff");
  
    // // value axis
    // // https://www.amcharts.com/docs/v4/concepts/axes/value-axis/
    var valueAxis = lineChart.yAxes.push(new am4charts.ValueAxis());
    // valueAxis.interpolationDuration = 3000;
    // valueAxis.renderer.grid.template.stroke = am4core.color("#000000");
    // valueAxis.renderer.grid.template.strokeOpacity = 0.25;
    // valueAxis.renderer.baseGrid.disabled = true;
    valueAxis.tooltip.disabled = true;
    valueAxis.title.text = "COVID Cases";
    valueAxis.title.fontSize = 15;
    // valueAxis.renderer.minGridDistance = 20;
    // valueAxis.extraMax = 0.05;
    // valueAxis.maxPrecision = 0;
    // valueAxis.renderer.inside = true;
    // valueAxis.renderer.labels.template.verticalCenter = "bottom";
    // valueAxis.renderer.labels.template.fill = am4core.color("#ffffff");
    // valueAxis.renderer.labels.template.padding(2, 2, 2, 2); 

    // Create series
    var series = createSeries(lineChart, "valueY", "Confirmed cases");
    // Create cursor
    lineChart.cursor = new am4charts.XYCursor();
    //lineChart.cursor.lineY.disabled = true;
    //Title
    var title = lineChart.titles.create();
    title.text = "Tompkins county";
    title.fontSize = 20;
    title.marginBottom = 10;
    title.stroke = am4core.color("#808080");
    // Bullets
    // series bullet
    var bullet = series.bullets.push(new am4charts.CircleBullet());

    // only needed to pass it to circle
    var bulletHoverState = bullet.states.create("hover");
    bullet.setStateOnChildren = true;

    bullet.circle.fillOpacity = 1;
    //bullet.circle.fill = backgroundColor;
    bullet.circle.radius = 4;
    // default - Tompkins
    initializeData();

    


function createSeries(xychart, field, name){
  var series = xychart.series.push(new am4charts.LineSeries());
  series.tensionX = 1;
  series.dataFields.valueY = field;
  series.dataFields.dateX = "date";
  series.name = name;
  series.tooltipText = "{dateX}: [bold]{valueY}[/] confirmed cases";
  series.strokeWidth = 2;
  series.stacked = true;
  series.fillOpacity = 0.2;
  
  return series;
}

function updateCountyData(data) {
    
  var countyData = [];
    for(var day=0; day<ndays+1; day++){
      var date = new Date(start_date.getTime() + day*86400000);
      var dateIndex = date.getMonth()+1 + "/" + date.getDate() + "/" + date.getFullYear();
      countyData.push({"date":date, "valueY":data[dateIndex]});
    }
  if (data["county"] != "New York City"){
  title.text = data["county"] + " county";}
  else {title.text = data["county"] ;};
  
  var maxIndex = countyData.length;
  while (countyData[maxIndex-1]["valueY"] == undefined) {maxIndex = maxIndex-1};

  var lastCountyTotal = countyData[maxIndex-2]["valueY"];
  var recentCountyDate = countyData[maxIndex-1].date.toDateString().substring(4,10) + ", "+countyData[maxIndex-1].date.getFullYear();
  var recentCountyTotal = countyData[maxIndex-1]["valueY"];
  var newCountyCases = recentCountyTotal-lastCountyTotal;
  //var increaseCountyPercent = (recentCountyTotal - lastCountyTotal) / lastCountyTotal * 100;

  document.getElementById("currentCounty").innerText = title.text;
  document.getElementById("recentCountyTotal").innerText = recentCountyTotal.toLocaleString();
  document.getElementById("newCountyCases").innerText = newCountyCases.toLocaleString();
  document.getElementById("recentCountyDate").innerText = recentCountyDate;
  //document.getElementById("increaseCountyPercent").innerText = increaseCountyPercent.toFixed(2);
  return countyData;
}

function initializeData(){
  Papa.parse(dataFile, {
    header: true,
    download:true,
    complete: function(results) {

      var data = results.data[54];
      var countyData = [];
    for(var day=0; day<ndays+1; day++){
      var date = new Date(start_date.getTime() + day*86400000);
      var dateIndex = date.getMonth()+1 + "/" + date.getDate() + "/" + date.getFullYear();
      countyData.push({"date":date, "valueY":data[dateIndex]});
    }
  
  lineChart.data = countyData;

  var maxIndex = countyData.length;
  while (countyData[maxIndex-1]["valueY"] == undefined) {maxIndex = maxIndex-1};

  var lastCountyTotal = countyData[maxIndex-2]["valueY"];
  var recentCountyDate = countyData[maxIndex-1].date.toDateString().substring(4,10) + ", "+countyData[maxIndex-1].date.getFullYear();
  var recentCountyTotal = countyData[maxIndex-1]["valueY"];
  var newCountyCases = recentCountyTotal-lastCountyTotal;
  //var increaseCountyPercent = (recentCountyTotal - lastCountyTotal) / lastCountyTotal * 100;

  document.getElementById("currentCounty").innerText = title.text;
  document.getElementById("recentCountyTotal").innerText = recentCountyTotal.toLocaleString();
  document.getElementById("newCountyCases").innerText = newCountyCases.toLocaleString();
  document.getElementById("recentCountyDate").innerText = recentCountyDate;
    }
  });
}

var totalChart = am4core.create("cumulativetotal", am4charts.XYChart);
  totalChart.width = am4core.percent(100);
  totalChart.height = am4core.percent(100);
  totalChart.background.fill = am4core.color("#FFFFFF");
  totalChart.background.fillOpacity = 1;

    // Create xy chart instance
    totalChart.fontSize = "0.8em";
    totalChart.paddingRight = 30;
    totalChart.paddingLeft = 30;
    totalChart.paddingBottom=10;
    totalChart.paddingTop = 50;
    totalChart.maskBullets = false;
    totalChart.zoomOutButton.disabled = true;
  
    // date axis
    // https://www.amcharts.com/docs/v4/concepts/axes/date-axis/
    var dateAxis2 = totalChart.xAxes.push(new am4charts.DateAxis());
    dateAxis2.renderer.minGridDistance = 50;
    // dateAxis.renderer.grid.template.stroke = am4core.color("#000000");
    // dateAxis.renderer.grid.template.strokeOpacity = 0.25;
    // dateAxis.tooltip.label.fontSize = "0.8em";
    // dateAxis.tooltip.background.fill = activeColor;
    // dateAxis.tooltip.background.stroke = activeColor;
    // dateAxis.renderer.labels.template.fill = am4core.color("#ffffff");
  
    // // value axis
    // // https://www.amcharts.com/docs/v4/concepts/axes/value-axis/
    var valueAxis2 = totalChart.yAxes.push(new am4charts.ValueAxis());
    // valueAxis.interpolationDuration = 3000;
    // valueAxis.renderer.grid.template.stroke = am4core.color("#000000");
    // valueAxis.renderer.grid.template.strokeOpacity = 0.25;
    // valueAxis.renderer.baseGrid.disabled = true;
    valueAxis2.tooltip.disabled = true;
    valueAxis2.title.text = "COVID Cases";
    valueAxis2.title.fontSize = 15;
    // valueAxis.renderer.minGridDistance = 20;
    // valueAxis.extraMax = 0.05;
    // valueAxis.maxPrecision = 0;
    // valueAxis.renderer.inside = true;
    // valueAxis.renderer.labels.template.verticalCenter = "bottom";
    // valueAxis.renderer.labels.template.fill = am4core.color("#ffffff");
    // valueAxis.renderer.labels.template.padding(2, 2, 2, 2); 

    // Create series
    var series2 = createSeries(totalChart, "valueY", "Total cases")
    series2.tensionX = 1;
    // Create cursor
    totalChart.cursor = new am4charts.XYCursor();
    //lineChart.cursor.lineY.disabled = true;
    //Title
    var title2 = totalChart.titles.create();
    title2.text = "Total Cases in New York";
    title2.fontSize = 20;
    title2.marginBottom = 10;
    title2.stroke = am4core.color("#808080")
    // Bullets
    // series bullet
    var bullet2 = series2.bullets.push(new am4charts.CircleBullet());

    // only needed to pass it to circle
    var bulletHoverState = bullet2.states.create("hover");
    bullet2.setStateOnChildren = true;

    bullet2.circle.fillOpacity = 1;
    //bullet.circle.fill = backgroundColor;
    bullet2.circle.radius = 4;


    
    parseTotal();
    


function parseTotal(){
  var totalData = [];
  Papa.parse(dataFile, {
    header: true,
    download:true,
    complete: function(results) {

      var data = results.data;
    
    
    for(var day=0; day<ndays+1; day++){
      var sum = 0;
      var diffNYC;
      for(var cnt=0; cnt<62; cnt++){
      var date = new Date(start_date.getTime() + day*86400000);
      var dateIndex = date.getMonth()+1 + "/" + date.getDate() + "/" + date.getFullYear();
      var temp = data[cnt][dateIndex];
      
      if(temp != undefined){
      sum = sum + parseInt(temp); 
      };

      if(data[cnt]["county"] == "New York City"){diffNYC = parseInt(temp);};
  
    }
  
    if(sum!=0){ totalData.push({"date":date, "valueY":sum-4*diffNYC}); }
   
    }
  
    totalChart.data = totalData;

    var recentTotal, recentDate, lastTotal, increase;
    lastTotal = totalData[totalData.length-2].valueY;
    recentTotal = totalData[totalData.length-1].valueY;
    recentDate = totalData[totalData.length-1].date.toDateString().substring(4,10)+", "+totalData[totalData.length-1].date.getFullYear();
    increase = recentTotal-lastTotal;
    var increasePercent = increase/lastTotal * 100;

    document.getElementById("newCases").innerText = increase.toLocaleString();
    document.getElementById("recentTotal").innerText = recentTotal.toLocaleString();
    document.getElementById("recentDate").innerText = recentDate;
    document.getElementById("increasePercent").innerText = increasePercent.toFixed(2);

  }
  });
  return totalChart.data;
}

var watermark = new am4core.Image();
watermark.href = "https://www.peese.org/wp-content/uploads/2018/01/logo-min-1.jpg";
container.children.push(watermark);
watermark.align = "left";
watermark.valign = "bottom";
watermark.opacity = 0.5;
watermark.marginLeft = 10;
watermark.marginBottom = 100;


function findMax(max){
  Papa.parse(dataFile, {
    header: true,
    download:true,
    complete: function(results) {
      
      // Finish later to automatically update maximum of legend (Currently set to 31,000 (ls - 4.5))
    }
    
  });

}


function setTrendData(){
  //data = polygonSeries.data;
  var days = ndays;
  var maxDate = new Date(start_date.getTime() + 86400000*days);
  var maxIndex = maxDate.getMonth()+1 + "/" + maxDate.getDate() + "/" + maxDate.getFullYear();
  Papa.parse(dataFile, {
    header: true,
    download:true,
    complete: function(results) {
      var data = results.data;
      var trendData = [];

      while (data[0][maxIndex] == undefined) {
        days = days - 1;
        maxDate = new Date(start_date.getTime() + 86400000*days);
        maxIndex = maxDate.getMonth()+1 + "/" + maxDate.getDate() + "/" + maxDate.getFullYear();
      };

      var lastDate = new Date(start_date.getTime() + 86400000*(days-1));
      var lastIndex = lastDate.getMonth()+1 + "/" + lastDate.getDate() + "/" + lastDate.getFullYear();

      for(var cnt=61; cnt>=0; cnt--){

        var lastTotal = data[cnt][lastIndex];
        var increase = data[cnt][maxIndex]-data[cnt][lastIndex];
        if(lastTotal!=0 && increase!=0){  trendData.push( {county:data[cnt].county, lastTotal:lastTotal, increase:increase} ); }
       
      }

      trendCounty.data = trendData;
    }
    
  });
 
}

// Consider only sixe counties
var countyIndices = [0, 1, 2, 3, 4, 5]

var trendCounty = am4core.create("trendCounty", am4charts.XYChart);
setTrendData();

// Create axes
var categoryAxis = trendCounty.xAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "county";
categoryAxis.renderer.grid.template.opacity = 0;
categoryAxis.renderer.labels.template.rotation = -60;
categoryAxis.renderer.minGridDistance = 20;
categoryAxis.renderer.labels.template.horizontalCenter = "middle";



var valueAxis3 = trendCounty.yAxes.push(new am4charts.ValueAxis());
valueAxis3.min = 1;
valueAxis3.max = maxValue;
valueAxis3.renderer.grid.template.opacity = 0;
valueAxis3.renderer.ticks.template.strokeOpacity = 0.5;
valueAxis3.renderer.ticks.template.stroke = am4core.color("#495C43");
valueAxis3.renderer.ticks.template.length = 10;
valueAxis3.renderer.line.strokeOpacity = 0.5;
valueAxis3.renderer.baseGrid.disabled = true;
valueAxis3.renderer.minGridDistance = 40;
valueAxis3.logarithmic = true;

// Create series

var series = trendCounty.series.push(new am4charts.ColumnSeries());
  series.dataFields.valueY = "lastTotal";
  series.dataFields.categoryX = "county";
  series.stacked = true;
  series.name = "Past Cases";
  var columnTemplate = series.columns.template;
  columnTemplate.tooltipText = "{categoryX}: [bold]{valueY}[/]";
  columnTemplate.fillOpacity = .8;
  columnTemplate.strokeOpacity = 0;
  columnTemplate.fill = am4core.color("grey");


  var series = trendCounty.series.push(new am4charts.ColumnSeries());
  series.dataFields.valueY = "increase";
  series.dataFields.categoryX = "county";
  series.stacked = true;
  series.name = "New Cases";
  var columnTemplate = series.columns.template;
  columnTemplate.tooltipText = "{categoryX}: [bold]{valueY}[/]";
  columnTemplate.fillOpacity = .8;
  columnTemplate.strokeOpacity = 0;
  columnTemplate.fill = am4core.color("#C0392B");

  var labelBullet = series.bullets.push(new am4charts.LabelBullet());
  labelBullet.locationY = -2;
  labelBullet.label.text = "{valueY}";
  labelBullet.label.fill = am4core.color("red");


// Legend
trendCounty.legend = new am4charts.Legend();
trendCounty.legend.position = "top";