import { helper } from "@ember/component/helper";

export default helper(([acl, instance]) => {
  const applicant = instance.involvedApplicants.find(
    (applicant) => applicant.invitee.id === acl.user.id,
  );
  return applicant.roleName;
});
