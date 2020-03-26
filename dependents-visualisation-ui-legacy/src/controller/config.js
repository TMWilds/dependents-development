// var api_url = "https://dependents.dev/api/v1";
// var site_url = "https://dependents.dev";

// var api_url = "http://localhost:8080/api/v1";
// var site_url = "http://localhost:8080";

var api_url = window.location.protocol + '//' + window.location.hostname + ':' +  window.location.port + '/legacy/api/v1';
var site_url = window.location.protocol + '//' + window.location.hostname + ':' +  window.location.port + '/legacy/';

var project_page_url = `${site_url}/project-dependents-view.html`;
var comparison_url = `${site_url}/project-dependent-comparison-view.html`;
var parse_waiting_loop_url = `${site_url}/parse-waiting-loop.html`;
