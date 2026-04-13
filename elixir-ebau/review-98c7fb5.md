# Code Review: Commit 98c7fb5 ("wip")

**Reviewer:** Claude (automated expert review)
**Date:** 2026-04-14
**Commit:** `98c7fb5b4f` — "wip"
**Scope:** 63 files changed, +1551 / -1206 lines — major architectural refactor

---

## Executive Summary

This commit consolidates the Caluma DSL extension layer. It replaces three
ebau-specific extensions (`Ebau.MasterData.Extensions.MasterData`,
`Ebau.Caluma.Extensions.DocumentBacked`, and the helpers module) with two
generic, reusable Caluma-level extensions (`Caluma.Form.Extensions.Document`
and `Caluma.Workflow.Extensions.Case`). Canton-aware resolution is extracted
into a formal behaviour (`QuestionIdResolver`) with a concrete
implementation (`CantonResolver`).

**Verdict:** Architecturally strong refactor. Moves domain-specific logic
out of the generic layer correctly. Several issues need attention before
merge.

---

## 1. Architectural Findings

### 1.1 GOOD: Clean separation of generic vs domain-specific

The old design conflated two concerns:
- How to read answers from a Caluma document (generic)
- How to resolve canton-specific question IDs (domain-specific)

Now `Caluma.Form.Extensions.Document` and `Caluma.Workflow.Extensions.Case`
are purely generic — they accept any `question_id` (string, list, or
resolver tuple). Canton-awareness lives solely in `CantonResolver`.

This makes the Caluma extensions potentially reusable across projects.

### 1.2 GOOD: Behaviour-based resolver pattern

`QuestionIdResolver` behaviour is a clean seam. Resolvers are passed as
`{module, opts}` tuples — no module-level config, no global state. Testable
in isolation.

### 1.3 GOOD: Entity reuse between Document and Case extensions

`Caluma.Workflow.Extensions.Case` reuses entity definitions from
`Caluma.Form.Extensions.Document` via public accessors (`answer_entity/0`,
etc.). No copy-paste.

### 1.4 CONCERN: `through` option only supports `nil` and `:case`

The `Caluma.Workflow.Extensions.Case.Transformer` hardcodes:

```elixir
defp answers_expr(nil), do: expr(document.answers)
defp answers_expr(:case), do: expr(case.document.answers)
```

Despite `through` being declared as a generic `:atom` in the DSL schema,
only `nil` and `:case` work. Any other atom (e.g. `:parent_case`) crashes
at compile time with a `FunctionClauseError`. Either:
- Restrict the schema type to `{:in, [nil, :case]}`
- Or make it truly generic by building the expression dynamically from
  the atom

### 1.5 CONCERN: Two extensions doing different things under "Case"

`Caluma.Workflow.Extensions.Case` does two unrelated things:
1. Provides `caluma_document` for case-related answer extraction
2. Provides `meta` for case meta JSON access

These could be independent extensions. Currently coupling means a resource
that only needs meta access still gets the document machinery. Minor now,
but worth noting for future.

### 1.6 CONCERN: Large commit scope = high review risk

63 files in a single "wip" commit. This mixes:
- New features (Case extension, QuestionIdResolver, PersonFields)
- Refactors (moving calculations to Caluma namespace)
- Bug fixes (nil guard in CreateRowDocument, validation in SetFormQuestionNaturalKey)
- Config changes (runtime.exs environment guard)
- Policy additions (AnswerDocument)

Should be split into atomic commits before merge.

---

## 2. Correctness Issues

### 2.1 BUG: `DocumentAnswer.init/2` doesn't validate `answers` option

```elixir
# caluma/form/calculations/document_answer.ex
def init(opts) do
  case opts[:question_id] do
    # validates question_id...
  end
end
```

The `answers` option is also accepted but never validated. If someone
passes `answers: "invalid"`, it silently passes init and fails at
expression evaluation time. Add validation or document that `answers`
is internal-only.

### 2.2 BUG: `MappedDocumentAnswer.init/2` delegates to `DocumentAnswer.init/2`

```elixir
defdelegate init(opts), to: DocumentAnswer
```

This only validates `question_id`. The `mapping` option is never validated
— a missing or malformed `mapping` passes init and crashes in
`expression/2`. Add:

```elixir
def init(opts) do
  with {:ok, opts} <- DocumentAnswer.init(opts) do
    if is_map(opts[:mapping]) or match?({_, _}, opts[:mapping]) do
      {:ok, opts}
    else
      {:error, "mapping must be a map or {module, opts} tuple"}
    end
  end
end
```

### 2.3 BUG: `CaseMeta.Transformer` uses `through` but option name is `:through`

In `Caluma.Workflow.Extensions.Case.Transformer`:

```elixir
{Caluma.Workflow.Calculations.CaseMeta, key: meta.key, through: through}
```

But `CaseMeta` calculation uses `:through` option internally:

```elixir
defp meta_expr(nil, key), do: expr(meta[^key])
defp meta_expr(:case, key), do: expr(case.meta[^key])
```

The option name is `:through` in the transformer but the calculation
reads `opts[:through]`. This works but note that the *Case extension DSL*
option is also named `through`. Verify no confusion between the DSL-level
`:through` (relationship name) and the calculation-level `:through` (path
to meta). Currently correct but fragile naming.

### 2.4 POTENTIAL BUG: `all_question_slugs/1` for resolvers

```elixir
def all_question_slugs({_mod, opts}) do
  opts
  |> extract_all_strings()
  |> Enum.uniq()
end
```

This extracts ALL string values from the opts map, including potentially
non-question-ID strings. For `CantonResolver` with simple maps this works,
but a resolver whose opts contain other string fields (descriptions,
config paths) would incorrectly include those in the filter.

This function is used for table relationship filters — getting it wrong
means rows from unrelated questions would be included. Consider requiring
resolvers to implement a `all_possible_ids/1` callback instead.

### 2.5 BUG: `AnswerDocument` policy allows `:destroy` in defaults but forbids mutations

```elixir
# answer_document.ex
policies do
  policy action_type([:create, :update, :destroy]) do
    forbid_if always()
  end
  policy action_type(:read) do
    authorize_if always()
  end
end

actions do
  defaults [:read, :destroy, create: :*, update: :*]
end
```

`:destroy` is in defaults but forbidden by policy. Either remove it from
defaults or document why it exists but is forbidden.

---

## 3. Ash / Spark Best Practices

### 3.1 `authorizers: Ash.Policy.Authorizer` vs `authorizers: [Ash.Policy.Authorizer]`

Multiple resources changed from list to bare atom. Both forms work in
current Ash, but the list form is the documented convention. The bare atom
form relies on internal coercion. Prefer consistency — pick one form and
use it everywhere.

### 3.2 Answer type always `Caluma.Form.Types.AnswerValue` for Document answers

In `AnswerTransformer.add_answer_calc/2`:

```elixir
Ash.Resource.Builder.build_calculation(
  answer.name,
  Caluma.Form.Types.AnswerValue,  # hardcoded
  ...
)
```

But the DSL entity has a `type` field. The declared type is ignored for
`answer` entities — they always get `AnswerValue`. Meanwhile
`mapped_answer` correctly uses `mapped.type`. This mismatch is confusing.
Either use the declared type or remove the `type` field from the `answer`
entity schema.

### 3.3 Domain annotations needed on cross-domain relationships

Good: Several relationships now have `domain:` annotations:

```elixir
belongs_to :case, Caluma.Workflow.Case, domain: Caluma.Workflow
has_many :instance_acls, Ebau.Permissions.InstanceACL, domain: Ebau.Permissions
```

But the Case extension's transformer builds relationships without domain:

```elixir
# Case.Transformer
Ash.Resource.Builder.build_relationship(:has_many, table.name, table.resource,
  no_attributes?: true,
  sort: [min_answer_document_sort: :asc]
)
```

If `table.resource` lives in a different domain (e.g. `Ebau.MasterData`
resources used from `Ebau.Instances`), this may fail at runtime with
domain resolution errors. The table entity schema should accept an
optional `domain` option.

### 3.4 `GisLink` adds `forbid_if always()` for `:update` but no `:destroy` policy

```elixir
policy action_type(:update) do
  forbid_if always()
end
```

No `:destroy` policy exists. If destroy actions are defined (or inherited),
they'd fall through to the default policy. Intentional? Should document or
add explicit destroy policy.

---

## 4. Elixir Best Practices

### 4.1 Transformer module defined inside extension module

Both `Caluma.Form.Extensions.Document.AnswerTransformer` and
`Caluma.Workflow.Extensions.Case.Transformer` are defined at the bottom of
their parent extension files:

```elixir
defmodule Caluma.Workflow.Extensions.Case.Transformer do
  # at bottom of case.ex
end
```

This works but can cause confusing compilation order issues in Elixir.
The inner module must be compiled *after* the outer module's `use
Spark.Dsl.Extension` has been evaluated. Currently correct because they're
at the bottom, but fragile — moving the `defmodule` up would break
compilation. Consider separate files.

### 4.2 `CantonResolver.resolve/2` can return `nil`

```elixir
def resolve(mapping, context) do
  canton = get_canton(context)
  if canton do
    mapping[canton] || mapping[:default]
  else
    mapping[:default]
  end
end
```

If `mapping` has no `:default` key, this returns `nil`. Downstream,
`DocumentAnswer.answer_expr/2` would crash on `nil`:

```elixir
def answer_expr(answers, id) when is_binary(id) do ...
def answer_expr(answers, ids) when is_list(ids) do ...
# no clause for nil
```

Add a guard or raise a clear error in the resolver.

### 4.3 Repeated `resolve_mapping/2` pattern

Both `MappedDocumentAnswer` and `MappedListDocumentAnswer` define:

```elixir
defp resolve_mapping(mapping, _context) when is_map(mapping), do: mapping
defp resolve_mapping({mod, opts}, context), do: mod.resolve(opts, context)
```

Extract to a shared function in `DocumentAnswer` or a helper, like
`resolve_question_id` already is.

### 4.4 Redundant nil check simplification possible in `CreateRowDocument`

```elixir
{question, next_sort} =
  case Caluma.Form.get_answer_by_document_and_question(...) do
    {:ok, answer} -> {answer.question, (answer.max_sort || 0) + 1}
    _ -> {Caluma.Form.get_question_by_slug!(slug, action_opts), 1}
  end
```

The `|| 0` guard is good but the wildcard `_` match swallows errors.
Should match `{:error, %Ash.Error.Query.NotFound{}}` specifically.

---

## 5. Testing

### 5.1 GOOD: Tests updated to match new API

All tests migrated from `question_ids:` to `question_id:`, from
`Ebau.MasterData.Calculations.*` to `Caluma.Form.Calculations.*`. Test
structure mirrors the production code changes.

### 5.2 GOOD: PersonFields gets its own test

`PersonFieldsTest` verifies all 24 fields are injected with correct
calculation module and resolver.

### 5.3 MISSING: No tests for `CantonResolver` returning `nil`

The `canton_resolver_test.exs` should test behavior when mapping has no
`:default` key and no matching canton. Currently this is an unhandled case
that would crash downstream.

### 5.4 MISSING: No tests for Document extension's `answer` entity type mismatch

No test verifies that declared types on `answer` entities are (or aren't)
used. The current code ignores them (see 3.2).

### 5.5 MISSING: No integration test for Case extension with `through: nil`

Tests only cover `through: :case`. The `through: nil` path (resource IS
the case) is untested.

---

## 6. Config / Deployment

### 6.1 BREAKING: `runtime.exs` repo config changed from `!= :test` to `== :dev`

```elixir
-if config_env() != :test do
+if config_env() == :dev do
```

This means **production** no longer gets database config from environment
variables via this block. If prod config is handled elsewhere (e.g.
releases config), this is fine. If not, **this is a production-breaking
change**. Verify prod deployment strategy.

### 6.2 Aggregate rename: `row_sort` -> `min_answer_document_sort`

```elixir
-:row_sort,
+:min_answer_document_sort,
```

And sort references updated in table relationship builders. Good rename
for clarity, but verify no external code references `row_sort` by name
(e.g. in JSON API sort parameters or frontend code).

---

## 7. Summary of Action Items

| Priority | Item | Section |
|----------|------|---------|
| **P0** | Verify prod DB config after runtime.exs change | 6.1 |
| **P0** | Handle `nil` return from `CantonResolver.resolve/2` | 4.2 |
| **P1** | Restrict `through` to supported values or make generic | 1.4 |
| **P1** | Validate `mapping` option in `MappedDocumentAnswer.init/2` | 2.2 |
| **P1** | Fix `answer` type being ignored (always AnswerValue) | 3.2 |
| **P1** | Add domain option to table entity for cross-domain use | 3.3 |
| **P1** | Split into atomic commits before merge | 1.6 |
| **P2** | Add nil-return test for CantonResolver | 5.3 |
| **P2** | Test `through: nil` path in Case extension | 5.5 |
| **P2** | Extract duplicated `resolve_mapping/2` | 4.3 |
| **P2** | Match specific error in CreateRowDocument, not wildcard | 4.4 |
| **P3** | Consider splitting Case extension into Document + Meta | 1.5 |
| **P3** | Clean up AnswerDocument defaults vs policy conflict | 2.5 |
| **P3** | Move transformers to own files to avoid ordering fragility | 4.1 |
| **P3** | Standardize `authorizers` to list or bare form | 3.1 |
