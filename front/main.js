function initInputs() {
  var allInputs = document.body.querySelectorAll(".bar-input");
 
  for (var i = 0; i < allInputs.length; i++) {
    var input = allInputs[i];
    var barId = input.parentNode.id;
    var styleEl = document.head.appendChild(document.createElement("style"));
 
    if (i == allInputs.length - 1) {
      
      var indicator=input.parentNode.querySelector('.bar .indicator');
      setBarIndicator(barId, input, styleEl, indicator);
      input.oninput = setBarIndicator.bind(this, barId, input, styleEl, indicator);
      input.onchange = setBarIndicator.bind(this, barId, input, styleEl, indicator);
    } else {
      setBar(barId, input, styleEl);
      input.oninput = setBar.bind(this, barId, input, styleEl);
      input.onchange = setBar.bind(this, barId, input, styleEl);
    }
  }
}
 
function setBar(barId, input, styleEl) {
  styleEl.innerHTML =
    "#" + barId + " .bar-face.percentage:before {width:" + input.value + "%;}";

  sendSliderValue(input.value);  
}

function setBarIndicator(barId, input, styleEl, indicatorEl) {
  styleEl.innerHTML =
    "#" + barId + " .bar-face.percentage:before {width:" + input.value + "%;}";
  indicatorEl.style.marginLeft = (input.value - 10) + '%';
  indicatorEl.textContent = input.value + '%';

  sendSliderValue(input.value);  
}

function sendSliderValue(value) {

  let intValue = Math.round(value * 2.54);

  // console.log("nty rak", intValue);

  fetch("http://localhost:8000/send-slider", { 
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({ value: intValue})
  })
  .then(response => response.json())
  .then(data => {
      console.log("Slider value sent successfully:", data);
  })
  .catch(error => {
      console.error("Error sending slider value:", error);
  });
}

initInputs();
