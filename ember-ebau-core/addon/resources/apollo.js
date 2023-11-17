import { registerDestructor } from "@ember/destroyable";
import { queryManager } from "ember-apollo-client";
import { task, lastValue } from "ember-concurrency";
import { Resource } from "ember-resources";

export class ApolloQuery extends Resource {
  @queryManager apollo;

  get isLoading() {
    return this.fetchData.isRunning;
  }

  constructor(owner) {
    super(owner);

    registerDestructor(this, () => {
      this.fetchData.cancelAll({ resetState: true });
    });
  }

  modify(positional) {
    this.fetchData.perform(...positional);
  }

  async reload(...positional) {
    return await this.fetchData.perform(
      ...(positional.length
        ? positional
        : this.fetchData.lastSuccessful?.args ?? []),
    );
  }

  @lastValue("fetchData") value;
  fetchData = task({ restartable: true }, async (params, path, postProcess) => {
    const queryData = await this.apollo.query(params, path);

    if (postProcess) {
      return await postProcess(queryData);
    }

    return queryData;
  });

  get hasRan() {
    return this.fetchData.lastComplete !== null;
  }
}

export default (context, params, path, postProcess) =>
  ApolloQuery.from(context, () => [params(), path, postProcess]);
