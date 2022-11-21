import ENV from "camac-ng/config/environment";

export default function isProd() {
  return window.location.hostname === ENV.APPLICATION.prodUrl;
}
