function make_request() {
  var XHR = new XMLHttpRequest();
  var FD  = new FormData();
  FD.append('address', document.getElementById('address').value);
  FD.append('lat', document.getElementById('lat').value);
  FD.append('lng', document.getElementById('lng').value);

  XHR.addEventListener('load', function(event) {
    document.getElementById('response').value = event.currentTarget.response;
  });
  XHR.addEventListener('error', function(event) {
    document.getElementById('response').value = 'Error.';
  });

  XHR.open('POST', '/geo_code');
  XHR.send(FD);
}
