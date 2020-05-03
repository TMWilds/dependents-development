# Dependents Visualisation and UI (Deprecated)

This service forms the frontend of the system. It provides user controls to select a project for analysis, view dependent projects, and explore dependent visualisations.

The UI is built using Javascript framework VueJS, as a single page application. This enables stateful front end components, which are modular and re-usable. Routing is handled through Vue Router which enables data to be passed to components, and seamless transitions between views.

Visualisations can be found under the [components](./src/components/) directory. All visualisations are self-contained and rely only on the D3.js library.

This visualisation can be built into a Docker container, to be served with an Nginx server. To do this, run `./build.sh`.

Alternatively, for rapid development, use Vue's server feature to run a local web server that will respond to changes as you make them. Note, you may need to change the api_url mixin in [main.js](./src/main.js) to do this, as the URL from which the api address is inferred will change.  