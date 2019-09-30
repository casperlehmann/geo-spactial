function make_request() {
  var XHR = new XMLHttpRequest();
  var FD  = new FormData();
  FD.append('address', document.getElementById('address').value);

  XHR.addEventListener('load', function(event) {
    document.getElementById('response').value = event.currentTarget.response;
  });
  XHR.addEventListener('error', function(event) {
    document.getElementById('response').value = 'Error.';
  });

  XHR.open('POST', '/geo_code');
  XHR.send(FD);
}
