defmodule EbauWeb.PageHTML do
  @moduledoc """
  This module contains static pages.

  See the `page_html` directory for all templates available.
  """
  use EbauWeb, :html

  embed_templates "page_html/*"
end
