#!/usr/bin/env bash

load_identity() {
    grep '^Identity:' work/state/seed_state.md | cut -d':' -f2- | xargs
}

load_pulse() {
    grep '^Pulse:' work/state/seed_state.md | cut -d':' -f2- | tr -cd '0-9'
}

next_pulse() {
    local p
    p="$(load_pulse)"
    [ -z "$p" ] && p=0
    echo $((p+1))
}
