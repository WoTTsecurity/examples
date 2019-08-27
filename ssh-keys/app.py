import json
import os
import pwd

JSON_PATH = '/opt/wott/credentials/root/ssh-keys.json'


def get_ssh_keys():
    """
    We expect this file to look like this a single key:

    { "user": "ssh-[...]" }

    or, as follows multiple keys ('\n' as separator):

    { "user": "ssh-[...]\nssh-[...]" }
    """
    with open(JSON_PATH) as f:
        return json.load(f)


def prepare_paths(user):
    """
    We will assume that SSH being configured to user '~/.ssh/authorized_keys'
    for SSH keys.
    """

    try:
        user_lookup = pwd.getpwnam(user)
    except KeyError:
        print('User {} not found.'.format(user))
        return

    ssh_user_path = '{}/.ssh'.format(user_lookup.pw_dir, user)
    authorized_keys_file = '{}/authorized_keys'.format(ssh_user_path)

    # Create ~/.ssh if it doesn't exist
    # and then set the appropriate permission.
    if not os.path.exists(ssh_user_path):
        os.mkdir(ssh_user_path)

    # Create authorized_keys file if empty
    if not os.path.exists(authorized_keys_file):
        os.mknod(authorized_keys_file)

    # Make sure permission is right
    os.chmod(ssh_user_path, 0o700)
    os.chown(ssh_user_path, user_lookup.pw_uid, user_lookup.pw_gid)
    os.chmod(authorized_keys_file, 0o600)
    os.chown(authorized_keys_file, user_lookup.pw_uid, user_lookup.pw_gid)
    return authorized_keys_file


def install_ssh_key(authorized_keys_file, keys):
    expand_keys = keys.split()

    with open(authorized_keys_file, 'r+') as f:
        for key in expand_keys:
            if '{}\n'.format(key) not in f:
                print('Adding key to {}'.format(authorized_keys_file))
                f.write('{}\n'.format(key))


def main():
    ssh_keys = get_ssh_keys()

    for user in ssh_keys:
        print('Found user {}.'.format(user))

        authorized_keys_file = prepare_paths(user)
        if authorized_keys_file:
            install_ssh_key(
                    authorized_keys_file,
                    ssh_keys[user]
                    )


if __name__ == '__main__':
    main()
