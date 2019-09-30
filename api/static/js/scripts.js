function make_request() {
  var XHR = new XMLHttpRequest();
  var FD  = new FormData();
  FD.append('address', document.getElementById('address').value);
  FD.append('lat', document.getElementById('lat').value);
  FD.append('lng', document.getElementById('lng').value);

  XHR.addEventListener('load', function(event) {
    document.getElementById('response').value = JSON.stringify(JSON.parse(event.currentTarget.response));
  });
  XHR.addEventListener('error', function(event) {
    document.getElementById('response').value = 'Error.';
  });

  XHR.open('POST', '/geo_code');
  XHR.send(FD);
}

function random_choice(choices) {
  let chosen_index = Math.floor(Math.random()*choices.length);
  return choices[chosen_index];
}

function clear_fields() {
  document.getElementById('address').value = '';
  document.getElementById('lat').value = '';
  document.getElementById('lng').value = '';
  document.getElementById('response').value = '';
}

function example() {
  clear_fields();
  if(Math.random() > .5) {
      document.getElementById('address').value = random_choice([
          'New York City',
          'London',
          'Copenhagen',
          'Istanbul',
          'Beijing',
          'Tokyo',
          'H. C. Andersens Blvd. 27, 1553 København, Denmark',
          'H.C. Andersens Boulevard 27, 1553 København, Danmark'
      ]);
  } else {
      [(document.getElementById('lat').value), (document.getElementById('lng').value)] = random_choice([
          [40.7127281, -74.0060152],
          [55.674136, 12.571782],
          [41.0096334, 28.9651646],
          [39.906217, 116.3912757],
          [35.6828387,139.7594549]
      ]);
  }
}
