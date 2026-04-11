defmodule Ebau.Legacy.ConfigLoader do
  @moduledoc """
  Loads selected legacy JSON fixture files into current database.

  This module is explicit fixture-loading layer for Elixir tests and setup tasks.
  It reads JSON files from configured legacy fixture root, defaulting to
  `../django/<application>/config` and `../django/<application>/data`,
  filters down to supported Django models, then bulk-inserts those rows into legacy and Caluma
  tables owned by Elixir app.

  Main use cases:

  - bootstrap selected canton/application config in tests
  - load real production-like Caluma forms and workflows for integration tests
  - support explicit `mix ebau.load_config` task

  This loader does **not** aim to be full replacement for Django `loaddata` or
  `camac_load.py`. It currently supports only subset of models needed by Elixir app.

  Typical usage:

      Ebau.Legacy.ConfigLoader.load_application_config!("kt_so")

      Ebau.Legacy.ConfigLoader.load_application_config!("kt_so", scope: :all)

      Ebau.Legacy.ConfigLoader.load_files!([
        "/abs/path/to/django/kt_so/config/user.json",
        "/abs/path/to/django/kt_so/config/caluma_workflow.json",
        "/abs/path/to/django/kt_so/config/caluma_form.json"
      ])

  Import order matters. Rows are inserted in dependency-safe order:

  1. `user.role`
  2. `user.servicegroup`
  3. `caluma_form.form`
  4. `caluma_form.question`
  5. `caluma_workflow.workflow`
  6. `caluma_form.formquestion`
  """

  alias Ebau.Repo

  @type application :: String.t()
  @type scope :: :config | :all
  @type fixture_path :: String.t()
  @type model :: String.t()

  @supported_models [
    "caluma_form.form",
    "caluma_form.question",
    "caluma_form.formquestion",
    "caluma_workflow.workflow",
    "user.role",
    "user.servicegroup"
  ]

  @doc """
  Loads fixture files for given Django application into current database.

  By default this loads `config/*.json`. Pass `scope: :all` to include
  `data/*.json`, and `include_init?: true` to append `init.json` when present.

  ## Examples

      iex> Ebau.Legacy.ConfigLoader.load_application_config!("kt_so")
      :ok

      iex> Ebau.Legacy.ConfigLoader.load_application_config!("kt_so", scope: :all)
      :ok
  """
  @spec load_application_config!(application(), keyword()) :: :ok
  def load_application_config!(application, opts \\ []) do
    scope = Keyword.get(opts, :scope, :config)
    include_init? = Keyword.get(opts, :include_init?, false)

    application
    |> application_files!(scope, include_init?)
    |> load_files!()
  end

  @doc """
  Returns fixture files for given Django application.

  `scope` controls whether only `config/*.json` or both `config/*.json` and
  `data/*.json` are returned. `include_init?` appends `init.json` when present.
  """
  @spec application_files!(application(), scope(), boolean()) :: [fixture_path()]
  def application_files!(application, scope \\ :config, include_init? \\ false) do
    application_dir = Path.join(django_root(), application)

    patterns =
      case scope do
        :config -> ["config/*.json"]
        :all -> ["config/*.json", "data/*.json"]
      end

    files =
      patterns
      |> Enum.flat_map(fn pattern ->
        application_dir
        |> Path.join(pattern)
        |> Path.wildcard()
      end)
      |> Enum.sort()

    files =
      if include_init? do
        init_path = Path.join(application_dir, "init.json")

        if File.exists?(init_path) do
          files ++ [init_path]
        else
          files
        end
      else
        files
      end

    if files == [] do
      raise ArgumentError,
            "no fixture files found for application #{inspect(application)} with scope #{inspect(scope)}"
    end

    files
  end

  @doc """
  Returns currently supported Django fixture model names.
  """
  @spec supported_models() :: [model()]
  def supported_models, do: @supported_models

  @doc """
  Loads explicit list of JSON fixture files.

  Files are decoded, filtered to supported models, then inserted into current database.

  ## Examples

      iex> Ebau.Legacy.ConfigLoader.load_files!([
      ...>   "/abs/path/to/django/kt_so/config/user.json",
      ...>   "/abs/path/to/django/kt_so/config/caluma_workflow.json"
      ...> ])
      :ok
  """
  @spec load_files!([fixture_path()]) :: :ok
  def load_files!(paths) do
    entries =
      paths
      |> Enum.flat_map(&read_entries!/1)
      |> Enum.filter(&(&1["model"] in @supported_models))

    {:ok, _result} =
      Repo.transaction(fn ->
        entries
        |> Enum.filter(&(&1["model"] == "user.role"))
        |> import_roles!()

        entries
        |> Enum.filter(&(&1["model"] == "user.servicegroup"))
        |> import_service_groups!()

        entries
        |> Enum.filter(&(&1["model"] == "caluma_form.form"))
        |> import_forms!()

        entries
        |> Enum.filter(&(&1["model"] == "caluma_form.question"))
        |> import_questions!()

        entries
        |> Enum.filter(&(&1["model"] == "caluma_workflow.workflow"))
        |> import_workflows!()

        entries
        |> Enum.filter(&(&1["model"] == "caluma_form.formquestion"))
        |> import_form_questions!()
      end)

    :ok
  end

  defp read_entries!(path) do
    path
    |> File.read!()
    |> JSON.decode!()
  end

  defp django_root do
    System.get_env("LEGACY_FIXTURE_ROOT") ||
      Application.get_env(:ebau, :legacy_fixture_root) ||
      default_django_root()
  end

  defp default_django_root do
    Mix.Project.project_file()
    |> Path.dirname()
    |> Path.join("../django")
    |> Path.expand()
  end

  defp import_roles!([]), do: :ok

  defp import_roles!(entries) do
    Repo.insert_all(
      "ROLE",
      Enum.map(entries, &role_row/1),
      on_conflict: :nothing,
      conflict_target: [:ROLE_ID]
    )

    :ok
  end

  defp import_service_groups!([]), do: :ok

  defp import_service_groups!(entries) do
    Repo.insert_all(
      "SERVICE_GROUP",
      Enum.map(entries, &service_group_row/1),
      on_conflict: :nothing,
      conflict_target: [:SERVICE_GROUP_ID]
    )

    :ok
  end

  defp import_forms!([]), do: :ok

  defp import_forms!(entries) do
    Repo.insert_all(
      "caluma_form_form",
      Enum.map(entries, &form_row/1),
      on_conflict: :nothing,
      conflict_target: [:slug]
    )

    :ok
  end

  defp import_questions!([]), do: :ok

  defp import_questions!(entries) do
    Repo.insert_all(
      "caluma_form_question",
      Enum.map(entries, &question_row/1),
      on_conflict: :nothing,
      conflict_target: [:slug]
    )

    :ok
  end

  defp import_workflows!([]), do: :ok

  defp import_workflows!(entries) do
    Repo.insert_all(
      "caluma_workflow_workflow",
      Enum.map(entries, &workflow_row/1),
      on_conflict: :nothing,
      conflict_target: [:slug]
    )

    :ok
  end

  defp import_form_questions!([]), do: :ok

  defp import_form_questions!(entries) do
    Repo.insert_all(
      "caluma_form_formquestion",
      Enum.map(entries, &form_question_row/1),
      on_conflict: :nothing,
      conflict_target: [:id]
    )

    :ok
  end

  defp role_row(%{"pk" => id, "fields" => fields}) do
    %{
      ROLE_ID: id,
      NAME: fields["name"],
      GROUP_PREFIX: fields["group_prefix"],
      SLUG: fields["slug"],
      ROLE_PARENT_ID: fields["role_parent"]
    }
  end

  defp service_group_row(%{"pk" => id, "fields" => fields}) do
    %{
      SERVICE_GROUP_ID: id,
      NAME: fields["name"],
      sort: fields["sort"],
      slug: fields["slug"]
    }
  end

  defp form_row(%{"pk" => slug, "fields" => fields}) do
    %{
      created_at: timestamp!(fields["created_at"]),
      modified_at: timestamp!(fields["modified_at"]),
      created_by_user: fields["created_by_user"],
      created_by_group: fields["created_by_group"],
      modified_by_user: fields["modified_by_user"],
      modified_by_group: fields["modified_by_group"],
      slug: slug,
      name: json_map!(fields["name"]),
      description: json_map(fields["description"]),
      meta: fields["meta"] || %{},
      is_published: fields["is_published"] || false,
      is_archived: fields["is_archived"] || false,
      source_id: fields["source"]
    }
  end

  defp question_row(%{"pk" => slug, "fields" => fields}) do
    %{
      created_at: timestamp!(fields["created_at"]),
      modified_at: timestamp!(fields["modified_at"]),
      created_by_user: fields["created_by_user"],
      created_by_group: fields["created_by_group"],
      modified_by_user: fields["modified_by_user"],
      modified_by_group: fields["modified_by_group"],
      slug: slug,
      label: json_map!(fields["label"]),
      type: fields["type"],
      is_required: fields["is_required"] || "false",
      is_hidden: fields["is_hidden"] || "false",
      is_archived: fields["is_archived"] || false,
      configuration: fields["configuration"] || %{},
      meta: fields["meta"] || %{},
      row_form_id: fields["row_form"],
      sub_form_id: fields["sub_form"],
      source_id: fields["source"],
      info_text: json_map(fields["info_text"]),
      placeholder: json_map(fields["placeholder"]),
      data_source: fields["data_source"],
      static_content: json_map(fields["static_content"]),
      format_validators: json_list(fields["format_validators"]),
      default_answer_id: uuid(fields["default_answer"]),
      calc_dependents: json_list(fields["calc_dependents"]),
      calc_expression: fields["calc_expression"],
      hint_text: json_map(fields["hint_text"])
    }
  end

  defp workflow_row(%{"pk" => slug, "fields" => fields}) do
    %{
      created_at: timestamp!(fields["created_at"]),
      modified_at: timestamp!(fields["modified_at"]),
      created_by_user: fields["created_by_user"],
      created_by_group: fields["created_by_group"],
      modified_by_user: fields["modified_by_user"],
      modified_by_group: fields["modified_by_group"],
      slug: slug,
      name: json_map!(fields["name"]),
      description: json_map(fields["description"]),
      meta: fields["meta"] || %{},
      is_published: fields["is_published"] || false,
      is_archived: fields["is_archived"] || false,
      allow_all_forms: fields["allow_all_forms"] || false
    }
  end

  defp form_question_row(%{"pk" => id, "fields" => fields}) do
    %{
      created_at: timestamp!(fields["created_at"]),
      modified_at: timestamp!(fields["modified_at"]),
      created_by_user: fields["created_by_user"],
      created_by_group: fields["created_by_group"],
      modified_by_user: fields["modified_by_user"],
      modified_by_group: fields["modified_by_group"],
      id: id,
      sort: fields["sort"] || 0,
      form_id: fields["form"],
      question_id: fields["question"]
    }
  end

  defp timestamp!(nil), do: nil

  defp timestamp!(value) do
    case DateTime.from_iso8601(value) do
      {:ok, datetime, _offset} ->
        datetime

      {:error, reason} ->
        raise ArgumentError, "invalid timestamp #{inspect(value)}: #{inspect(reason)}"
    end
  end

  defp json_map(nil), do: nil
  defp json_map(value) when is_map(value), do: value
  defp json_map(value) when is_binary(value), do: JSON.decode!(value)

  defp json_map!(value) do
    case json_map(value) do
      nil -> raise ArgumentError, "expected JSON map, got nil"
      map -> map
    end
  end

  defp json_list(nil), do: []
  defp json_list(value) when is_list(value), do: value
  defp json_list(value) when is_binary(value), do: JSON.decode!(value)

  defp uuid(nil), do: nil
  defp uuid(value), do: Ecto.UUID.dump!(value)
end
