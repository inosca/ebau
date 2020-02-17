import { run } from "@ember/runloop";
import { getContext } from "@ember/test-helpers";
import { all } from "rsvp";

export default async function loadQuestions(names, instanceId) {
  const { owner } = getContext();

  const qstore = owner.lookup("service:question-store");
  const store = owner.lookup("service:store");

  await run(
    async () =>
      await store.findRecord("instance", instanceId, { include: "form" })
  );
  await run(
    async () => await store.query("form-field", { instance: instanceId })
  );
  await run(
    async () => await store.query("attachment", { instance: instanceId })
  );

  const qs = [
    ...store.peekAll("form-field").toArray(),
    ...store.peekAll("attachment").toArray()
  ];

  qstore._store.pushObjects(
    await all(
      names.map(
        async n =>
          await qstore.buildQuestion(
            n,
            instanceId,
            qs.find(({ name }) =>
              names.includes(name.replace(/\.(png|pdf|jp(e)?g)$/, ""))
            )
          )
      )
    )
  );
}
