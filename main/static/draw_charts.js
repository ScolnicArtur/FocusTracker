
let xValues = [];
let yValues = [];
function get_data(){
    const requestObject = new XMLHttpRequest();
    requestObject.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            const obj = JSON.parse(this.responseText)
            Object.keys(obj).forEach(function(key) {
              let val = JSON.parse("[" + obj[key] + "]")
              const average = val.reduce((a, b) => a + b, 0) / val.length;
              xValues.push(String(key));
              yValues.push(Number(average));
              draw_chart();
            });
        }
    }
    
    requestObject.open("POST", "");
    const filename = document.getElementById('filename').value;
    const subject = document.getElementById('subject').value;
    const data = subject.concat("\\").concat(filename);
    console.log(data);
    requestObject.send(data);
}

function draw_chart(){
  console.log(xValues);
  console.log(yValues);
    new Chart("myChart", {
      type: "line",
      data: {
        labels: xValues,
        datasets: [{
          backgroundColor:"rgba(0,0,255,1.0)",
          borderColor: "rgba(0,0,255,0.1)",
          data: yValues,
          label: 'Attentiveness'
        }]
      },
      options: {}
    });
}

function init(){
    get_data();
}