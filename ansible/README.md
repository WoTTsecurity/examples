# Ansible Playbook for WoTT Agent

## Usage

* Copy in the `wott-agent` directory into your [Ansible Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) directory.
* Update `wott-agent/vars/main.yml` with your claim token (available within [dash.wott.io](https://dash.wott.io)).
* Enable the role in your playbook.

## Testing

### Pre-requisites

 * Vagrant
 * Ansible (pinned in `requirements.txt`)

### Running

Simply run:

```
$ vagrant up
```

If all goes well, the agent should install in all distributions.
