#!/usr/bin/env bats

export MOCK=1

@test "List images" {
	run pontoon image list
	[ "$status" = 0 ]
	[ "${lines[3]}" = " - Ubuntu     14.04 x64                                     ubuntu-14-04-x64" ]
}

@test "List OSes" {
	run pontoon image oses
	[ "$status" = 0 ]
	[ "${lines[1]}" = " - Ubuntu" ]
}

@test "Show image details" {
	run pontoon image show "14.04 x64"
	[ "$status" = 0 ]
	[ "${lines[1]}" = "name: 14.04 x64" ]
}
