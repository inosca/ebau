#!/bin/bash

if [ -z "$1" ]
then
	echo usage: $0 \<report-date-dirs\>
	exit 1
fi

TARGET_DIR=$(echo "$@" | sed 's/ /,_/g')
FINAL_TARGET_DIR="./aggregated/$TARGET_DIR"

mkdir -p "$FINAL_TARGET_DIR"

for r in "$@"
do
	for t in document_export document_import dossier_import
	do
	  for s in $r/*
	  do
	    s="$(basename $s)"
	    mkdir -p "$FINAL_TARGET_DIR/${s}"
      for d in $r/$s/$t
      do
        for f in $d/*.csv
        do
          # only copy over the very first file incl. headers, in the subsequent ones filter them
          # write global report
          if [ -f "$FINAL_TARGET_DIR/${s}/${t}.csv" ]
          then
            tail -n +2 "$f" \
            | grep -v "^Importzeit" \
            | grep -v ",kein Dokument gefunden$" \
            | grep -v ",Dokument bereits importiert$" \
            >>"$FINAL_TARGET_DIR/${s}/${t}.csv"
          else
            cat "$f" \
            | grep -v ",kein Dokument gefunden$" \
            | grep -v ",Dokument bereits importiert$" \
            >>"$FINAL_TARGET_DIR/${s}/${t}.csv"
          fi

          # write per segment report
          if [ -f "$FINAL_TARGET_DIR/${t}.csv" ]
          then
            tail -n +2 "$f" \
            | grep -v "^Importzeit" \
            | grep -v ",kein Dokument gefunden$" \
            | grep -v ",Dokument bereits importiert$" \
            >>"$FINAL_TARGET_DIR/${t}.csv"
          else
            cat "$f" \
             | grep -v ",kein Dokument gefunden$" \
             | grep -v ",Dokument bereits importiert$" \
             >>"$FINAL_TARGET_DIR/${t}.csv"
          fi
        done
      done
    done
	done
done
