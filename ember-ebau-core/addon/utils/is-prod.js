import mainConfig from "ember-ebau-core/config/main";

export default function isProd() {
  return window.location.hostname === mainConfig.prodUrl;
}
