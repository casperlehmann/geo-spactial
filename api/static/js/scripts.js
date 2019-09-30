function make_request() {
    var XHR = new XMLHttpRequest();
    var FD  = new FormData();
    FD.append('address', document.getElementById('address').value);
    XHR.open('POST', '/geo_code');
    XHR.send(FD);
  }
