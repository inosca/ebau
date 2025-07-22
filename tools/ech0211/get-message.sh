#!/bin/bash
source ./config.sh

# Check if a last_message_id is provided as the first argument
if [ -n "$1" ]; then
  last_message_id_param="?last=$1"
  echo "Using provided last_message_id: $1"
else
  # Default last_message_id if no argument is given
  last_message_id_param=""
  echo "Reading the first message"
fi

echo "---------------------------"
echo "eCH0211 - GET message"
echo "---------------------------"

for i in "${!ech0211_credentials[@]}"
do
  ech0211_login "$i" "${ech0211_credentials[$i]}"
  echo " > perform request[message] for client_id: $i"
  echo -e "\n---------------------------"
  
  # Construct the full URL
  request_url="${ech0211_endpoint}/ech/v1/message/${last_message_id_param}"
  echo "Request URL: $request_url" # Optional: print the URL for debugging

  # Perform the curl request and store the output in a variable
  # Added -s to curl to make it silent and not show progress meter
  xml_response=$(curl -s -X GET "${request_url}" \
  -H "Authorization: Bearer $token" \
  -H 'accept: application/xml' \
  -H "x-camac-group: ${camac_group_id}" \
  -H 'Content-Type: application/xml')
  
  # Check if curl command was successful and response is not empty
  if [ -n "$xml_response" ]; then
    echo "Formatted XML Response:"
    # Pretty-print the XML using xmllint
    # The '-' as the last argument means read from stdin
    echo "$xml_response" | xmllint --format -
    echo -e "\n---------------------------"

    # Extract messageId and messageType using xmllint with XPath
    # We use local-name() to ignore namespaces in the XPath query for simplicity,
    # or you would need to declare them with xmllint.
    
    # Define namespaces for XPath query with xmllint
    # The provided XML uses ns2 for eCH-0058 elements
    message_id=$(echo "$xml_response" | xmllint --xpath "string(//*[local-name()='deliveryHeader']/*[local-name()='messageId' and namespace-uri()='http://www.ech.ch/xmlns/eCH-0058/5']/text())" -)
    message_type=$(echo "$xml_response" | xmllint --xpath "string(//*[local-name()='deliveryHeader']/*[local-name()='messageType' and namespace-uri()='http://www.ech.ch/xmlns/eCH-0058/5']/text())" -)
    
    # Fallback using grep and sed if xmllint XPath fails or is not precise enough (less robust)
    if [ -z "$message_id" ] || [ -z "$message_type" ]; then
        echo "Warning: XPath extraction failed or returned empty. Attempting fallback..."
        # This grep approach is more brittle if XML formatting changes slightly
        message_id_grep=$(echo "$xml_response" | grep -o '<ns2:messageId>[^<]*</ns2:messageId>' | sed 's/<ns2:messageId>\(.*\)<\/ns2:messageId>/\1/')
        message_type_grep=$(echo "$xml_response" | grep -o '<ns2:messageType>[^<]*</ns2:messageType>' | sed 's/<ns2:messageType>\(.*\)<\/ns2:messageType>/\1/')
        
        # Assign if fallback produced results and original didn't
        if [ -n "$message_id_grep" ]; then message_id="$message_id_grep"; fi
        if [ -n "$message_type_grep" ]; then message_type="$message_type_grep"; fi
    fi

    echo "Extracted Information:"
    if [ -n "$message_id" ]; then
      echo "Message ID: $message_id"
    else
      echo "Message ID: Not found"
    fi
    
    if [ -n "$message_type" ]; then
      echo "Message Type: $message_type"
    else
      echo "Message Type: Not found"
    fi

  else
    echo "Error: Failed to retrieve XML response or response was empty for client_id: $i"
  fi
  
  echo -e "\n---------------------------"
done