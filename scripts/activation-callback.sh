#!/bin/sh

log() {
    printf "%s: %s\n" $(date --iso-8601=seconds) "${1}"
    logger -it "activation-callback" "$1"
}

help() {
    echo "
    $(tput bold)Camac Activation Callback:$(tput sgr0)

    activation-callback execute
        Callback due activations or notify services if any activations due shortly.

    activation-callback dryrun
        Show what callback would do.
"
}

login() {

    CSRF_TOKEN=$(curl "${URL}/user" \
			    --cookie-jar ./cookies.txt \
			    -f \
			    -s \
			   | awk -F '"' '/hidden/ { print $6 }')

    # Cleanup cookies.txt after exit
    trap "rm -f cookies.txt" EXIT

    log "Logging into \"${URL}\" with user \"${USER}\""
    curl "${URL}/user/authenticate" \
	 --cookie-jar ./cookies.txt \
	 --cookie ./cookies.txt \
	 -X POST \
	 -L \
	 -f \
	 -s \
	 -o /dev/null \
	 -d "username=${USER}&password=${PASS}&token=${CSRF_TOKEN}&login_button=Login"

    if [[ $? != 0 ]]; then
	log "Login failed"
	exit 1
    fi

    log "Login succeeded"
}

call_endpoint() {

    local BODY=$(curl "${URL}/activationcallback/callback/${1}" \
		       --cookie-jar ./cookies.txt \
		       --cookie ./cookies.txt \
	       	       -f \
		       -s)

    log "Calling endpoint  \"$1\""

    if [[ $? != 0 ]]; then
	log "Calling endpoint \"$1\" failed"
	exit 1
    fi

    log "Activation callback completed. The following activation were considered: ${BODY}"
}

dryrun() {
    call_endpoint "dryrun"
}

execute() {
    call_endpoint "execute"
}


: "${USER?"Need to set USER"}"
: "${PASS?"Need to set PASS"}"
: "${URL?"Need to set URL"}"

case "$1" in
    execute)
	shift;
	login
	execute "$@"
	;;
    dryrun)
	shift;
	login
	dryrun "$@"
	;;
    *)
	help "$@"
	;;
esac
exit 0
