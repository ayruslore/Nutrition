google.charts.load("current", {packages:["corechart"]});

var header = ["Timestamp", "Name", "Gender", "Age", "How often do you think about your health?", "Do you have any specific health goals?", "If yes, it would be great if you could let us know about them in brief.", "What makes you think about your health? Select all that apply.", "How do you envision a better version of yourself? Select all that apply.", "What are some common ailments that you suffer from? Please select all that apply.", "Do you have any nutritional deficiencies? ", "If yes, can you briefly mention what deficiencies you suffer from (For example: Vitamins (A,B,C,D,E,K), Iron, Calcium, Iodine etc.)", "Do you consume any of the following ?", "Do you take any nutritional supplements (For example: Multivitamins, Biotin, Mineral supplements, etc.)? ", "How did you come to know about these supplements?", "Do you take supplements through the year or intermittently?", "How do you take your supplements?", "Where do you purchase your supplements from?", "What is important for you when you purchase the supplements?" ,  "What types of supplements do you prefer?" , "On a scale of 1-10, how likely are you to undertake a brand switch from your current supplements?", "What do you feel is lacking in the existing supplements in the market?", "What are some lifestyle changes that you would want to make?", "Which factor(s) motivate/influence you to work on improving your health/appearance?", "How would you rate your health/appearance in comparison to people of your age group on a scale of 1 to 5? ", "Who are your role models, key opinion leaders when it comes to health and wellness ?", "Are you interested in consuming nutritional supplements in the future? ", "If you answered 1, 2 or 3 in the previous question, can you briefly state what makes you disinterested in consuming supplements in the future?", "If you answered 4 or 5, can you briefly state what interests you about nutritional supplements?", "Which format of nutritional supplement is attractive to you?", "", "", "", ""];

var data = [[],[],["Male", "Female"], ["24", "25-29","30-34", "35-40", "40"], ["Very Often", "Sometimes", "Rarely", "Never"], ["Yes","No"], [], [] ,[], [], ["Yes","No"], [], ["Meat", "Dairy products", "None"], ["Yes", "No"], ["Doctor", "Online", "Referral", "Nutritionist"], ["Always", "Intermittently"], [], ["Offline Store", "Online Store", "Nutritionist/Doctor Samples"], ["Quality", "Price", "Brand", "Accessibility", "Doctor/Nutritionist Recommended"], ["Ayurvedic", "Non-Ayurvedic", "Whatever"], [1,2,3,4,5,6,7,8,9,10], [], [], [], [1,2,3,4,5], [], [1,2,3,4,5]];

var numbers = [2,3,4,5,10,12,13,14,15,17,18,19,20,24,26];

var filters = {};
var visualizingcolumn = 0;

function myFunction(id,num){
  var checkbox = document.getElementById(id+num);
  if(checkbox.checked == true){
    if(id == 'dat'){
      var i = String(num).slice(-1);
      var j = String(num).slice(0, (String(num).length - 1));
      filters[String(j)] = data[j][i];
    }
    else{
      visualizingcolumn = num;
    }
  }
  else{
    if(id == 'dat'){
      var i = String(num).slice(-1);
      var j = String(num).slice(0, (String(num).length -1));
      filters.remove(j);
    }
    else{
      if(visualizingcolumn==num){
        visualizingcolumn = 0;
      }
    }
  }
  console.log(filters);
  console.log(visualizingcolumn);
}

function Showchart(){
  if(visualizingcolumn == 0){
    alert('Please select a column and some filters for visualizing!')
  }
  else{
    $.get('http://35.154.42.243:5000/getfilterdatavisualize/' + JSON.stringify(filters) +"/"+ visualizingcolumn, function(data,status){
      data = JSON.parse(data);
      console.log(data);
      drawChart(data);
    });
  }
}

function drawChart(dat) {
  var data = google.visualization.arrayToDataTable(dat);
  var options = {
    title: '',
    is3D: true,
  };
  var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
  chart.draw(data, options);
}
