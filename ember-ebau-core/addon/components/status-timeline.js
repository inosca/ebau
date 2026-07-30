import { service } from "@ember/service";
import Component from "@glimmer/component";
import { trackedFunction } from "reactiveweb/function";

const ICON_MAPPING = {
  pending: "ellipsis",
  running: "play",
  done: "check",
};

export default class StatusTimeline extends Component {
  @service fetch;

  // Number of placeholder steps to render while loading, matching the usual
  // amount of configured steps.
  //
  // If another cantons starts using this feature and happens to have a
  // different count of steps, this **needs** to be moved to the main config.
  skeletonStepCount = 6;

  statusTimeline = trackedFunction(this, async () => {
    const response = await this.fetch.fetch(
      `/api/v1/status-timeline/${this.args.instanceId}`,
      { headers: { accept: "application/json" } },
    );

    return await response.json();
  });

  getIcon = (status) => ICON_MAPPING[status];
}
