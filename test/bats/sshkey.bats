#!/usr/bin/env bats

export MOCK=1

@test "List SSH keys" {
	run pontoon sshkey list
	[ "$status" = 0 ]
	[ "${lines[1]}" = " - foobarbaz" ]
}

@test "Add SSH key" {
	run pontoon sshkey add foo `mktemp -t pontoontest.XXXXX`
	[ "$status" = 0 ]
}

@test "Show SSH key" {
	run pontoon sshkey show foobarbaz
	[ "$status" = 0 ]
}

@test "Fail to show non-existant key" {
	run pontoon sshkey show bar
	[ "$status" = 1 ]
}

@test "Replace an existing key" {
	run pontoon sshkey replace foobarbaz `mktemp -t pontoontest.XXXXX`
	[ "$status" = 0 ]
}

@test "Fail to replace a non-existant key" {
	run pontoon sskey replace foo `mktemp -t pontoontest.XXXXX`
	[ "$status" = 1 ]
}

@test "Destroy a key" {
	run pontoon sshkey destroy foobarbaz
	[ "$status" = 0 ]
}
