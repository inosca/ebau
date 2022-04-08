function instanceReductor(all, workItem) {
  return [
    ...all,
    workItem.case.parentWorkItem?.case.meta["camac-instance-id"] ||
      workItem.case.meta["camac-instance-id"],
  ];
}

function usernameReductor(all, workItem) {
  return [
    ...all,
    ...workItem.assignedUsers,
    workItem.createdByUser,
    workItem.closedByUser,
  ];
}

function serviceReductor(all, workItem) {
  return [
    ...all,
    ...workItem.addressedGroups,
    workItem.createdByGroup,
    workItem.closedByGroup,
  ];
}

export default function getProcessData(workItems) {
  const instanceIds = [...new Set(workItems.reduce(instanceReductor, []))];
  const usernames = [...new Set(workItems.reduce(usernameReductor, []))];
  const serviceIds = [...new Set(workItems.reduce(serviceReductor, []))];

  return {
    instanceIds: instanceIds.filter(Boolean),
    usernames: usernames.filter(Boolean),
    serviceIds: serviceIds.filter((s) => parseInt(s)),
  };
}
