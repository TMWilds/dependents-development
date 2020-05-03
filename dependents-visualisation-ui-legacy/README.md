# Dependents Visualisation and UI (Deprecated)

####Note: This is a legacy version of the UI and has been deprecated in favour of the "dependents-ui-service". The UI can still be accessed under the /legacy/ troute, but visualisations may not be appear correctly.

This service provides the front end to the analysis system. It includes a homepage (`index.html`) where a user can initiate analysis, an analysis progress page `parse-waiting-loop.html` and multiple visualisation pages.

The UI has been written in HTML and Javascript, using Bootstrap for formatting, and D3.js to render visualisations.

This visualisation can be built into a Docker container, to be served with an Nginx server. To do this, run `./build.sh`.

