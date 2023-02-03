import { registerDestructor } from "@ember/destroyable";
import { inject as service } from "@ember/service";
import { task, lastValue } from "ember-concurrency";
import { Resource } from "ember-resources";

const shouldResetPage = ([oldModel, oldQuery] = [], [newModel, newQuery]) =>
  parseInt(newQuery.page.number) === 1 ||
  oldModel !== newModel ||
  // Compare all keys in the old and new query to see if we have changes which would require a fresh data array.
  Array.from(new Set([...Object.keys(newQuery), ...Object.keys(oldQuery)]))
    .filter((key) => key !== "page")
    .some((key) => newQuery[key] !== oldQuery[key]);

export class PaginatedQuery extends Resource {
  @service store;

  get records() {
    return this.data?.records ?? [];
  }

  get isLoading() {
    return this.fetchData.isRunning;
  }

  get hasMore() {
    return this.data?.hasMore;
  }

  get error() {
    return this.data.error;
  }

  get isError() {
    return Boolean(this.error);
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

  @lastValue("fetchData") data;
  fetchData = task({ restartable: true }, async (model, query) => {
    await Promise.resolve();
    try {
      const data = await this.store.query(model, query);

      return {
        records: shouldResetPage(this.fetchData.lastSuccessful?.args, [
          model,
          query,
        ])
          ? data.toArray()
          : [...this.data.records, ...data.toArray()],
        hasMore: query.page.number < data.meta?.pagination?.pages,
      };
    } catch (error) {
      console.error(error);
      return { isError: true, error };
    }
  });
}

export default (context, modelName, query) =>
  PaginatedQuery.from(context, () => [modelName, query()]);
