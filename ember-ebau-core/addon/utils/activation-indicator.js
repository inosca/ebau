import { DateTime } from "luxon";

export default function getActivationIndicator(activation) {
  if (!activation) {
    return null;
  }

  const now = DateTime.now();
  if (activation.state === "NFD") {
    return "nfd";
  } else if (activation.state === "OK") {
    return "completed";
  } else if (DateTime.fromISO(activation.deadlineDate) < now) {
    return "expired";
  } else if (
    DateTime.fromISO(activation.deadlineDate).minus({ days: 5 }) < now
  ) {
    return "due-shortly";
  }

  return null;
}
