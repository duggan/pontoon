## 0.2.2 (March 5, 2016)

BUGFIXES:

   * **Python 3.5 compatibility** [GH-42]

FEATURES:

   * **Pass commands to Droplet** Can pass shell commands to a Droplet, e.g,
	 `pontoon droplet ssh example.com "ls /"`

## 0.2.1 (November 6, 2015)

BUGFIXES:

   * **`pontoon configure` fixed** was broken by the 0.2.0 release.

## 0.2.0 (November 6, 2015)

This is mostly a maintenance update to keep Pontoon working with the Digital Ocean V2 API, as [V1 is being sunset soon](https://github.com/duggan/pontoon/issues/21). New functionality exposed by the API has not been integrated yet.

FEATURES:

   * **Partial Windows support :tada::** Thanks to some fantastic effort from @bendtherules, Pontoon is now most of the way towards being usable on Windows. Work on this will hopefully continue through the 0.2.x series.
   * **`--field=<foo>` on droplet show:** Allows for deep access to Droplet attributes, e.g., `pontoon droplet show foobar --field=networks.v4.0.ip_address`
   Thanks to @nureineide for the initial implementation!

IMRPOVEMENTS:

   * **Migrated to V2 API:** [GH-21]
   * **Removed library component:** Now uses the better maintained [python-digitalocean](https://github.com/koalalorenzo/python-digitalocean)
   * **`--no-wait` added to more commands:** Useful for asynchronous instrumentation.
   * **Removed `--no-scrub` flag:** DigitalOcean wisely removed this from the V2 API.
	
CHANGES:

   * **`--detail` output:** The V2 API now provides more information. Internally,
   this has been switched to a YAML formatted output for consistency.
   * **`--with-ids` removed:** the `pontoon region` and `pontoon size` commands no longer accept the `--with-ids` parameter, as DigitalOcean have stopped supplying IDs in the return of API V2.
