import { service } from "@ember/service";
import Component from "@glimmer/component";
import { trackedFunction } from "reactiveweb/function";

export default class MilestoneValues extends Component {
  @service milestones;

  milestone = trackedFunction(this, async () => {
    return await this.milestones.getMilestone(
      this.args.field.question.raw.meta.milestone,
    );
  });
}
