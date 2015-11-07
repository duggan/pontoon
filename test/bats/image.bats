#!/usr/bin/env bats

export MOCK=1

@test "List images" {
	run pontoon image list
	[ "$status" = 0 ]
	[ "${lines[3]}" = " - Ubuntu     14.04 x64" ]
}

@test "List OSes" {
	skip "FIXME: key order different with 3.3"
	run pontoon image oses
	[ "$status" = 0 ]
	[ "${lines[2]}" = " - Foobuntu" ]
}

@test "Show image details" {
	skip "FIXME: key order different in 3.3/pypy"
	run pontoon image show "Foobuntu 12.04 x64"
	[ "$status" = 0 ]
	[ "${lines[0]}" = "   distribution: Foobuntu" ]
}
