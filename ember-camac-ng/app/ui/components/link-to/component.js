import LinkComponent from "@ember/routing/link-component";

export default class CustomLinkComponent extends LinkComponent {
  classNames = ["no-loading"];
}
