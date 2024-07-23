# Frontend API

## Handlebars

### Helpers

- `has-any-permission` to check whether we have at least one of the requested permissions on the passed instance
- `has-all-permissions` to check whether we have all of the requested permissions on the passed instance

```hbs
{{#if (has-any-permission this.instanceId "form-read" "foo" "bar")}}
  Permission to read the form!
{{else}}
  No permission to read the form...
{{/if}}
```

### Component (not implemented yet)

```hbs
<HasAnyPermission
  @instanceId={{this.instanceId}}
  @permissions={{array "foo" "bar"}}
>
  <:loading>
    loading
  </:loading>
  <:default>
    has permissions
  </:default>
  <:no-permission>
    no permissions
  </:no-permission>
</HasPermission>
```

## JS

### Service

- `hasAny` to check whether we have at least one of the requested permissions on the passed instance
- `hasAll` to check whether we have all of the requested permissions on the passed instance

```js
export default class FooComponent extends Component {
  @service permissions;

  async doSomething() {
    if (
      !(await this.permissions.hasAny(this.instanceId, [
        "form-read",
        "foo",
        "bar",
      ]))
    ) {
      // no permission
      return;
    }
  }
}
```

### Testing

```js
module("foo", function (hooks) {
  setupPermissions(hooks, 1, ["foo", "bar"]); // Pass in initial permissions

  test("foo", async function (assert) {
    this.permissions.grant(this.instance.id, ["baz"]);
    this.permissions.revoke(this.instance.id, ["bar"]);
    this.permissions.getAll(this.instance.id); // Output: ["foo", "baz"]
  });
});
```
