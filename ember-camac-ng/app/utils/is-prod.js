import ENV from "camac-ng/config/environment";

export default function isProd() {
  return window.location.origin.includes(ENV.APPLICATION.prodUrl);
}
