#!/usr/bin/env bats

export MOCK=1

@test "List snapshots" {
	run pontoon snapshot list
	[ "$status" = 0 ]
	[ "${lines[3]}" = " - Ubuntu     My Snapshot" ]
}

@test "Show snapshot details" {
	skip "FIXME: Key order is different in pypy"
	run pontoon snapshot show "My Snapshot"
	[ "$status" = 0 ]
	[ "${lines[0]}" = "   distribution: Foobuntu" ]
	[ "${lines[1]}" = "   id: 1024" ]
	[ "${lines[2]}" = "   name: snapshot-foo" ]
}

@test "Destroy snapshot" {
	run pontoon snapshot destroy "My Snapshot"
	[ "$status" = 0 ]
	[ "${lines[0]}" = "Destroying My Snapshot..." ]
}

@test "Fail to destroy non-existant snapshot" {
	run pontoon snapshot destroy "Your Snapshot"
	[ "$status" = 1 ]
	[ "${lines[1]}" = "No image named 'Your Snapshot'" ]
}

@test "Transfer a snapshot" {
	run pontoon snapshot transfer "My Snapshot" "nyc2"
	[ "$status" = 0 ]
}
