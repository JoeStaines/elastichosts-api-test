#!/bin/bash

set +o posix
shopt -s extglob

die() {
  echo "$@" >&2
  exit 1
}

usage() {
  cat >&2 <<EOF
Usage: $0 [ OPTIONS ] DRIVE-UUID FILENAME
Options:
  -c CHUNK       size of chunks (default: 4194304)
  -o OFFSET      byte offset from which to resume download
EOF
  exit 1
}

if ! type -t curl >/dev/null; then
  die "This tool requires curl, available from http://curl.haxx.se/"
fi

[ -n "$EHURI" ] || die "Please set EHURI=<API endpoint URI>"
[ -n "$EHAUTH" ] || die "Please set EHAUTH=<user uuid>:<secret API key>"

CHUNK=4194304
unset OFFSET

while getopts c:o:s: OPTION; do
  case "$OPTION" in
    c)
      case "$OPTARG" in
        [1-9]*([0-9]))
          CHUNK="$OPTARG"
          ;;
        *)
          usage
          ;;
      esac
      ;;
    o)
      case "$OPTARG" in
        0|[1-9]*([0-9]))
          OFFSET="$OPTARG"
          ;;
        *)
          usage
          ;;
      esac
      ;;
    *)
      usage
      ;;
  esac
done
shift $(($OPTIND - 1))
[ $# -eq 2 ] || usage

EHAUTH="user = \"$EHAUTH\""

if [ -z "$OFFSET" ]; then
  OFFSET=0
  if [ -f "$2" ]; then
    OFFSET=`wc -c < "$2"`
    OFFSET=$((OFFSET - OFFSET % CHUNK))
  fi
fi

unset SIZE
while read KEY VALUE; do
  [ "$KEY" = "size" ] && SIZE=$VALUE
done <<< "`curl -K <(echo "$EHAUTH") -f -s "${EHURI%/}/drives/$1/info"`"
[ -n "$SIZE" ] || die "Drive $1 not found"

exec 3<>"$2" || die "Failed to open $2"

COUNT=$(((SIZE - OFFSET + CHUNK - 1)/CHUNK))
echo -n "Downloading $COUNT chunks of $CHUNK bytes starting at $OFFSET: "

dd if=/dev/null bs=1 seek=$OFFSET count=0 >&3 2>/dev/null
while [ $OFFSET -lt $SIZE ]; do
  [ $SIZE -lt $((CHUNK + OFFSET)) ] && CHUNK=$((SIZE - OFFSET))

  if ! curl -K <(echo "$EHAUTH") -f -s \
            "${EHURI%/}/drives/$1/read/$OFFSET/$CHUNK" >&3; then
    echo E
    cat <<EOF >&2
Failed to read chunk at offset $OFFSET: aborting
Restart with '-o $OFFSET' to resume the download
EOF
    exit 1
  fi

  echo -n .
  OFFSET=$((OFFSET + CHUNK))
done
echo " completed"
