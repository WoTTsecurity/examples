# Manage SSH keys with WoTT

This is a sample script that allows you to manage SSH keys on devices using WoTT as the management platform.

In simple terms, the script works as follows:

 * Install the WoTT agent onto your device(s).
 * Add a tag to each device you want to target.
 * Create a secret with the name 'ssh-keys'.
   * Set the owner to 'root'.
   * Each 'key' corresponds to a user and the value to the SSH key(s). For instance, if you want to add the key 'ssh-abc123' to the user 'foobar', you'd set 'foobar' as the key, and 'ssh-abc123' as the value (user `\n` as the separator for multiple keys).
 * Download and run the script in this directory.
   * If you want to automatically install new keys automatically, you can add this script to a cronjob.
