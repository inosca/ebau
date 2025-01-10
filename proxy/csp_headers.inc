# WARNING: THIS INCLUDE IS SHARED ACROSS MULTIPLE REPOSITORIES.
# =============================================================
#
# Any change needs to be shared and compatible with the other locations.
# TODO: figure out a better way to share / keep them in sync
#
# PLEASE KEEP UPSTREAM IN SYNC:
# https://git.adfinis.com/camac-ng/camac-ng/proxy/csp_headers.inc
#
# CSP header definitions
# ======================
#
# Define a few CSP header fragments and pre-defined
# headers to be used in the corresponding "location" blocks.
#
# Note: This is intended to be reusable across many places: Local dev envs,
# Production (docker-compose) envs, K8s
#
# REQUIRES the following variables to be defined before the include:
# - set $csp_keycloak_url "http://ebau-keycloak.local" (required)
# - set $csp_use_google_fonts "true" | "false" (optional; defaults to "false")
# - set $csp_use_font_data_url "true" | "false" (optional; defaults to "false")
# - set $csp_portal_allow_inline_style "true" | "false" (optional; defaults to "false")
# - set $csp_php_allow_unsafe_eval "true" | "false"  (optional; defaults to "false")
# - set $csp_php_allow_localhost_scripts "true" | "false"  (optional; defaults to "false")
# - set $csp_external_connect_sources "space-separated-list-of-urls" (optional; defaults to empty)
# - set $csp_external_img_sources "space-separated-list-of-urls" (optional; defaults to empty)
# - set $csp_external_style_sources "space-separated-list-of-urls" (optional; defaults to empty)
# IN RETURN, you get the following variables:
# - $csp_header_keycloak     - Keycloak
# - $csp_header_portal       - Portal (applicant-facing)
# - $csp_header_api          - ANY Django API endpoints (dms, camac, alexandria...)
# - $csp_header_php          - PHP parts of the application, if used
# - $csp_header_django       - Django with UI (django admin, graphql)
# - $csp_header_internal     - Internal area (canton/municipality/etc)
# - $csp_header_restricted   - Fully restricted (file downloads / minio etc)

# Define optional variables
# =========================
if ($csp_portal_allow_inline_style ~ "^$")   { set $csp_portal_allow_inline_style "false"; }
if ($csp_use_google_fonts ~ "^$")            { set $csp_use_google_fonts "false"; }
if ($csp_use_font_data_url ~ "^$")           { set $csp_use_font_data_url "false"; }
if ($csp_php_allow_unsafe_eval ~ "^$")       { set $csp_php_allow_unsafe_eval "false"; }
if ($csp_php_allow_localhost_scripts ~ "^$") { set $csp_php_allow_localhost_scripts "false"; }
if ($csp_external_connect_sources ~ "^$")    { set $csp_external_connect_sources ""; }
if ($csp_external_img_sources ~ "^$")        { set $csp_external_img_sources ""; }
if ($csp_external_style_sources ~ "^$")      { set $csp_external_style_sources ""; }

# Intermediates
# =============
# Do not use directly - those are only used to build up the above
# mentioned "result" variables.

set $csp_default_self   "default-src 'self'";
set $csp_script_default "script-src 'self'";
set $csp_script_inline  "script-src 'self' 'unsafe-inline'";
set $csp_img_default    "img-src 'self' data: ${csp_external_img_sources}";
set $csp_connect_src    "connect-src 'self' ${csp_external_connect_sources}";
set $csp_object_src     "object-src 'self' ${csp_external_img_sources}";

# Connect: We need to be able to connect to KC from anywhere for login / token
# fetch
set $csp_connect_src "${csp_connect_src} ${csp_keycloak_url}";
# Creating documents from templates does not work if data is not allowed
set $csp_connect_src "${csp_connect_src} data:";

# fonts: Depending on whether we use google
set $csp_fonts_src "font-src 'self'";
if ($csp_use_google_fonts = "true") {
  set $csp_fonts_src "${csp_fonts_src} https://fonts.gstatic.com";
}
if ($csp_use_font_data_url = "true") {
  # fonts embedded in "data:" URL
  set $csp_fonts_src "${csp_fonts_src} data:";
}

# Styles: Also depends on google fonts usage
set $csp_style_src "style-src 'self' ${csp_external_style_sources}";
if ($csp_use_google_fonts = "true") {
  set $csp_style_src "${csp_style_src} https://fonts.googleapis.com";
}

set $csp_portal_styles "";
if ($csp_portal_allow_inline_style = "true") {
  set $csp_portal_styles "'unsafe-inline'";
}

# Scripting: Vue components may need unsafe eval
set $csp_php_script_eval "";
if ($csp_php_allow_unsafe_eval = "true") {
  set $csp_php_script_eval "'unsafe-eval'";
}

# Scripting: Localhost components may need unsafe eval
set $csp_php_style_src "";
if ($csp_php_allow_localhost_scripts = "true") {
  set $csp_php_style_src "http://localhost:4200 http://localhost:4300";
  # ebau.local:4300 is required for Ember live reload
  set $csp_php_script_eval "${csp_php_script_eval} http://localhost:4200 http://localhost:4300 http://ebau.local:4300";
  set $csp_connect_src "${csp_connect_src} ws://ebau.local:4300";
}


# Final assembly
# ==============
# Note: In some places, "stacked buildup" is used (multiple assignment of the
# same variable). This is primarily for readability, as we'd get rather long
# lines otherwise

set $csp_header_restricted "default-src 'none'";

# API is also fully restricted. For easier understanding and possible future
# changes, we use two variables
set $csp_header_api "${csp_header_restricted}";

# Keycloak: Sadly needs to allow quite a bit
set $csp_header_keycloak "${csp_default_self}; ${csp_style_src} 'unsafe-inline'";
set $csp_header_keycloak "${csp_header_keycloak}; ${csp_fonts_src}";
set $csp_header_keycloak "${csp_header_keycloak}; ${csp_script_inline}";

# PHP: PHP uses tons of inline styles and inline scripts, too many to reliably
# fix. Therefore we need to allow quite a bit of unsafe-inline stuff.
set $csp_header_php "${csp_default_self}";
set $csp_header_php "${csp_header_php}; ${csp_script_inline} ${csp_php_script_eval}";
set $csp_header_php "${csp_header_php}; ${csp_style_src} ${csp_php_style_src} 'unsafe-inline'";
set $csp_header_php "${csp_header_php}; ${csp_fonts_src}";
set $csp_header_php "${csp_header_php}; ${csp_img_default}";
set $csp_header_php "${csp_header_php}; ${csp_connect_src}";

# Portal
set $csp_header_portal "${csp_default_self}";
set $csp_header_portal "${csp_header_portal}; ${csp_script_default}";
set $csp_header_portal "${csp_header_portal}; ${csp_style_src} ${csp_portal_styles}";
set $csp_header_portal "${csp_header_portal}; ${csp_fonts_src}";
set $csp_header_portal "${csp_header_portal}; ${csp_img_default}";
set $csp_header_portal "${csp_header_portal}; ${csp_connect_src}";
set $csp_header_portal "${csp_header_portal}; ${csp_object_src}";

# Internal
set $csp_header_internal "${csp_default_self}";
set $csp_header_internal "${csp_header_internal}; ${csp_script_default}";
set $csp_header_internal "${csp_header_internal}; ${csp_style_src}";
set $csp_header_internal "${csp_header_internal}; ${csp_fonts_src}";
set $csp_header_internal "${csp_header_internal}; ${csp_img_default}";
set $csp_header_internal "${csp_header_internal}; ${csp_connect_src}";
set $csp_header_internal "${csp_header_internal}; ${csp_object_src}";

# Django
set $csp_header_django "${csp_default_self}";
# Django admin sadly also requires some inline CSS and inline scripting to work
set $csp_header_django "${csp_header_django}; ${csp_script_default} 'unsafe-inline'";
set $csp_header_django "${csp_header_django}; ${csp_style_src} 'unsafe-inline'";
set $csp_header_django "${csp_header_django}; ${csp_img_default}";
