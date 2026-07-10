defmodule EbauWeb.Gettext do
  @moduledoc """
  A module providing Internationalization with a gettext-based API.

  By using [Gettext](https://hexdocs.pm/gettext), your module compiles translations
  that you can use in your application. To use this Gettext backend module,
  call `use Gettext` and pass it as an option:

      use Gettext, backend: EbauWeb.Gettext

      # Simple translation
      gettext("Here is the string to translate")

      # Plural translation
      ngettext("Here is the string to translate",
               "Here are the strings to translate",
               3)

      # Domain-based translation
      dgettext("errors", "Here is the error message to translate")

  See the [Gettext Docs](https://hexdocs.pm/gettext) for detailed usage.
  """
  use Gettext.Backend, otp_app: :ebau

  def supported_languages do
    canton = Application.get_env(:ebau, :canton)

    languages = %{
      ag: ["de"],
      be: ["de", "fr"],
      gr: ["de", "it"],
      lu: ["de"],
      sg: ["de"],
      so: ["de"],
      sz: ["de"],
      ur: ["de"]
    }

    Map.get(languages, canton)
  end
end
