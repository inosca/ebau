import Component from "@glimmer/component";

const STATUS_MAP = {
  pending: { icon: "clock", color: "muted" },
  confirmed: { icon: "circle-check", color: "success" },
  invalidated: { icon: "circle-exclamation", color: "warning" },
  canceled: { icon: "circle-xmark", color: "danger" },
};

export default class ApplicantConfirmationsConfirmation extends Component {
  get statusConfig() {
    return STATUS_MAP[this.args.confirmation.status];
  }
}
