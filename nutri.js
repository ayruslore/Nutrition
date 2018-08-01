google.charts.load("current", {packages:["corechart"]});

var header = ["Timestamp", "Name", "Gender", "Age", "How often do you think about your health?", "Do you have any specific health goals?", "If yes, it would be great if you could let us know about them in brief.", "What makes you think about your health? Select all that apply.", "How do you envision a better version of yourself? Select all that apply.", "What are some common ailments that you suffer from? Please select all that apply.", "Do you have any nutritional deficiencies? ", "If yes, can you briefly mention what deficiencies you suffer from (For example: Vitamins (A,B,C,D,E,K), Iron, Calcium, Iodine etc.)", "Do you consume any of the following ?", "Do you take any nutritional supplements (For example: Multivitamins, Biotin, Mineral supplements, etc.)? ", "How did you come to know about these supplements?", "Do you take supplements through the year or intermittently?", "How do you take your supplements?", "Where do you purchase your supplements from?", "What is important for you when you purchase the supplements?" ,  "What types of supplements do you prefer?" , "On a scale of 1-10, how likely are you to undertake a brand switch from your current supplements?", "What do you feel is lacking in the existing supplements in the market?", "What are some lifestyle changes that you would want to make?", "Which factor(s) motivate/influence you to work on improving your health/appearance?", "How would you rate your health/appearance in comparison to people of your age group on a scale of 1 to 5? ", "Who are your role models, key opinion leaders when it comes to health and wellness ?", "Are you interested in consuming nutritional supplements in the future? ", "If you answered 1, 2 or 3 in the previous question, can you briefly state what makes you disinterested in consuming supplements in the future?", "If you answered 4 or 5, can you briefly state what interests you about nutritional supplements?", "Which format of nutritional supplement is attractive to you?", "", "", "", ""];

var data = Answers = [[],[],["Male", "Female"], ["<24", "25-29","30-34", "35-40", "40+"], ["Very Often", "Sometimes", "Rarely", "Never"], ["Yes","No"], [], ["While reading an article/journal on health","While watching Advertisements","Checking myself out in the mirror/selfie/photo","Waking up in the morning","While watching movies/series","While having a meal","Others"] ,["Better Focus, Attention, or Concentration","More Physically Active","Better Immunity","More Stamina","Better Weight Management","Better Stress Management","More Patience","More Self-confident","More Optimistic","Others"], ["Menstrual Cramps","Headache/Fever","Acidity/Indigestion/Constipation","Cold/Cough","Stress","Oral Problems","Muscular Ache","Hair Loss/thinning/damage","Vision Related Problems - Blurry vision, dry eyes, etc.","Skin Problems","Memory or Cognitive Functions","Sleep Related - Insomnia, Difficulty Falling Asleep, etc.","Low Energy","Others"], ["Yes","No"], [], ["Meat", "Dairy products", "None"], ["Yes", "No"], ["Doctor", "Online Research", "Referral", "Nutritionist", "Others"], ["Always", "Intermittently"], ["During/with meals","Before a meal","After a meal","No fixed routine","Others"], ["Offline Store", "Online Store", "Nutritionist's/Doctors Samples","Others"], ["Quality", "Price", "Brand", "Ingredients Sources", "Others"], ["Ayurvedic", "Non-Ayurvedic", "Whatever is available"], ["1","2","3","4","5","6","7","8","9","10"], ["Potency","Activation Time", "Transparency - ingredients and side-effects","Availability","Packaging","Others"], ["Reduce/Quit Smoking","Responsible Drinking","Manage Eating Habits","Exercise more or be more physically active","Maintain better personal hygiene","Get adequate sleep or maintain a better sleep cycle","Spend more time with friends and family","Be more productive at work","Focus more on appearance","Others"], ["Family","Peer Group","Work Place","Media/Advertisements","Others"], ["1","2","3","4","5"], [], ["1","2","3","4","5"],[],[],["Tablets/ Capsules","Powder/ Instant mixes","Gummy bears/ candies (Chewables)","Protein powder ","Drops ","Others"],[],[],[],[]];

var numbers = [2,3,4,5,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,26,29];
for (var i = 0; i < data.length; i++) {
  console.log(data[i].length);
}
var filters = {};
var visualizingcolumn = 0;

function chFunction(id,lis){
  if(id == 'ch'){
    var checkbox = document.getElementById(id+String(lis));
    if(checkbox.checked == true){
      visualizingcolumn = lis;
    }
    else{
      if(visualizingcolumn==lis){ visualizingcolumn = 0 ; }
    }
  }
}

function datFunction(id,num1,num2){
  var checkbox = document.getElementById((id+num1) + num2);
  if(checkbox.checked == true){
      filters[String(num1)] = data[num1][num2];
  }
  else{
    if(filters[String(num1)]==data[num1][num2]){ delete(filters[num1]); }
  }
}

function Showchart(){
  if(visualizingcolumn == 0){
    alert('Please select a column and some filters for visualizing!')
  }
  else{
    $.post('http://0.0.0.0:5000/getfilterdatavisualize_new',{"column":visualizingcolumn,"filters":JSON.stringify(filters)}, function(data,status){
      data = JSON.parse(data);
      console.log(data);
      if(data['chart'] == 1){
        drawpieChart(data['data']);
      }
      if(data['chart'] == 2){
        drawbarChart(data['data']);
      }
    });
  }
}

function drawbarChart(data) {
  var bar_data = google.visualization.arrayToDataTable(data);
  var view = new google.visualization.DataView(bar_data);
  view.setColumns([0, 1,
                   { calc: "stringify",
                     sourceColumn: 1,
                     type: "string",
                     role: "annotation" },
                   2]);
  var options = {
    title: "",
    width: 800,
    height: 800,
    bar: {groupWidth: "80%"},
    legend: { position: "none" },
  };
  var chart = new google.visualization.BarChart(document.getElementById("piechart_3d"));
  chart.draw(view, options);
}

function drawpieChart(dat) {
  var data = google.visualization.arrayToDataTable(dat);
  var options = {
    title: '',
    is3D: true,
  };
  var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
  chart.draw(data, options);
}
