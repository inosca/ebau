# Housing stat proxy

This is a simple python proxy that sits between our frontend and the housing stat
API. It is needed because the API doesn't set the `Access-Control-Allow-Origin`
header, leading to CORS errors when trying to call it directly. This proxy is
meant to be used as an alternative to the nginx-based solution in k8s environments.
