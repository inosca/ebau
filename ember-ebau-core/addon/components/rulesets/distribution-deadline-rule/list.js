import Component from "@glimmer/component";
import { findAll } from "ember-data-resources";

export default class RulesetsDistributionDeadlineRuleList extends Component {
  rules = findAll(this, "distribution-deadline-rule", () => ({
    include: "target_service",
  }));
}
