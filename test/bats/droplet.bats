#!/usr/bin/env bats

export MOCK=1

@test "List Droplets" {
	run pontoon droplet list
	[ "$status" = 0 ]
	[ "${lines[0]}" = "example.com:    (512mb, ubuntu-14-04-x64, nyc3, 104.236.32.182, active)" ]
}

@test "Detailed Droplet list" {
	run pontoon droplet list --detail
	[ "$status" = 0 ]
	[ "${lines[0]}" = "example.com" ]
}

@test "Fail trying to create Droplet with existing hostname" {
	run pontoon droplet create example.com
	[ "$status" = 1 ]
}

@test "Create a Droplet" {
	run pontoon droplet create something-different \
	--size="512mb" \
	--image="ubuntu-14-04-x64" \
	--region="nyc3" \
	--no-wait # we should test the 'wait' variant too
	[ "$status" = 0 ]
}

@test "SSH into a Droplet" {
	skip "can't test SSH yet"
	run pontoon ssh example.com
	[ "$status" = 0 ]
}

@test "Rename a Droplet" {
	run pontoon droplet rename example.com example.org
	[ "$status" = 0 ]
}

@test "Fail to rename a Droplet to an existing hostname" {
	skip "Needs more fake Droplets"
	run pontoon droplet rename example.com example.net
	[ "$status" = 1 ]
}

@test "Resize a Droplet" {
	skip "FIXME: broken in Tox"
	run sh -c 'yes | pontoon droplet resize example.com 1gb'
	[ "$status" = 0 ]
}

@test "Create a Droplet snapshot" {
	skip "FIXME: broken in Tox"
	run sh -c 'yes | pontoon droplet snapshot example.com example-snapshot-daily'
	[ "$status" = 0 ]
}

@test "Show details for one Droplet" {
	run pontoon droplet show example.com
	[ "$status" = 0 ]
	[ "${lines[0]}" = "example.com" ]
}

@test "Show status for one Droplet" {
	run pontoon droplet status example.com
	[ "$status" = 0 ]
	[ "${lines[0]}" = "active" ]
}

@test "Destroy a Droplet, scrub its data" {
	run pontoon droplet destroy example.com
	[ "$status" = 0 ]
	[ "${lines[0]}" = "Destroying example.com and scrubbing data..." ]
}

@test "Destroy a Droplet, don't scrub data" {
	skip "Deprecated in API V2"
	run pontoon droplet destroy example.com --no-scrub
	[ "$status" = 0 ]
	[ "${lines[0]}" = "Destroying example.com..." ]
}

@test "Start a Droplet" {
	run pontoon droplet start example.com
	[ "$status" = 0 ]
}

@test "Shutdown a Droplet" {
	run pontoon droplet shutdown example.com
	[ "$status" = 0 ]
}

@test "Reboot a Droplet" {
	run pontoon droplet reboot example.com
	[ "$status" = 0 ]
}

@test "Restore a Droplet from snapshot" {
	run pontoon droplet restore example.com "My Snapshot"
	[ "$status" = 0 ]
}

@test "Rebuild a Droplet using a default image" {
	run pontoon droplet rebuild example.com "14.04 x64"
	[ "$status" = 0 ]
}

@test "Powercycling a Droplet should create a warning" {
	skip "this really needs an expect script"
	run sh -c 'yes | pontoon droplet powercycle example.com'
	[ "$status" = 0 ]
}

@test "Powercycling a Droplet, forced with --yes" {
	run pontoon droplet powercycle example.com --yes
	[ "$status" = 0 ]
}

@test "Powering off a Droplet should create a warning" {
	skip "this really needs an expect script"
	run sh -c 'yes | pontoon droplet poweroff example.com'
	[ "$status" = 0 ]
}

@test "Power a Droplet off, forced with --yes" {
	run pontoon droplet poweroff example.com --yes
	[ "$status" = 0 ]
}

@test "Reset root password for a Droplet" {
	skip "this really needs an expect script"
	run sh -c 'yes | pontoon droplet passwordreset example.com'
	[ "$status" = 0 ]
}

@test "Reset root password for a Droplet, forced with --yes" {
	run pontoon droplet passwordreset example.com --yes
	[ "$status" = 0 ]
}

@test "Enable backups should fail (deprecated in API V2)" {
	run pontoon droplet backups example.com --enable
	[ "$status" = 1 ]
}

@test "Disable backups" {
	run pontoon droplet backups example.com --disable
	[ "$status" = 0 ]
}

@test "Should be a single error message when incorrect arguments used" {
	run pontoon droplet backups example.com
	[ "$output" = "action must be either 'enable' or 'disable'" ]
}

@test "--field filter errors on incorrect field" {
	run pontoon droplet show example.com --field=foo.bar.baz
	[ "$status" = 1 ]
}

@test "Provide output of a single field of a droplet's info" {
	run pontoon droplet show example.com --field=networks.v4.0.ip_address
	[ "$status" = 0 ]
}
