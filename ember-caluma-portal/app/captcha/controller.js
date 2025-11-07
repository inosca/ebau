import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
export default class PublicInstancesCaptchaController extends Controller {
  @service router;
  @service fetch;
  @tracked captchaKey = null;
  @tracked captchaImageUrl = null;
  @tracked captchaChallenge = "";

  constructor(...args) {
    super(...args);
    this.refreshCaptcha();
  }

  @action
  async refreshCaptcha() {
    const captcha = await this.loadCaptchaImage();

    this.captchaKey = captcha.key;
    this.captchaImageUrl = captcha.image_url;
  }

  @action
  async submitCaptcha() {
    let response;
    try {
      response = await this.fetch.fetch(
        `/api/v1/captcha/validate/${this.captchaKey}/`,
        {
          method: "POST",
          headers: {
            "x-requested-with": "XMLHttpRequest",
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({ challenge: this.captchaChallenge }),
        },
      );
    } catch (e) {
      console.error("Captcha validation failed", e);
      this.captchaChallenge = "";
      this.refreshCaptcha();
      return;
    }

    if (!response) {
      console.error("Captcha validation failed", response);
      this.captchaChallenge = "";
      this.refreshCaptcha();
      return;
    }

    const json = await response.json();
    localStorage.setItem("publicCaptchaToken", json.token);

    return this.router.currentRoute.queryParams.nextURL
      ? document.location.replace(this.router.currentRoute.queryParams.nextURL)
      : this.router.transitionTo("public-instances");
  }

  @action
  async loadCaptchaImage() {
    const response = await this.fetch.fetch("/api/v1/captcha/generate/", {
      method: "GET",
      headers: {
        "x-requested-with": "XMLHttpRequest",
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    return await response.json();
  }

  @action
  onKeyDown({ key }) {
    if (key === "Enter") {
      this.submitCaptcha();
    }
  }
}
