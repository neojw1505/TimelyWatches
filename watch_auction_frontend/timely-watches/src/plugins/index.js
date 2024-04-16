/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import vuetify from "./vuetify";
import pinia from "../store";
import router from "../router";
import piniaPersist from "pinia-plugin-persist";

pinia.use(piniaPersist);

export function registerPlugins(app) {
  app.config.globalProperties.$RC = 0;
  app.use(vuetify)
  app.use(router)
  app.use(pinia);
}
