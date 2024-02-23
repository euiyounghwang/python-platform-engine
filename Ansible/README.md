
# Create instances of Elasticsearch using Ansible

- Install UTM Ubuntu for GUI and change IP address
```bash
$ sudo apt update
$ sudo apt install tasksel

$ sudo systemctl set-default graphical.target

$ sudo ifconfig eth0 192.168.69.3
```

- Add keys to instances
```bash
# https://community.sophos.com/intercept-x-endpoint/f/discussions/84268/change-ip-address-from-command-line-utm-9-3
# UTM : sudo ifconfig eth0 192.168.69.4
ssh-copy-id -i ./id_rsa.pub devuser@192.168.64.2
```

- Build Your Inventory : `Create inventory.yml`
- First, group your inventory logically. Best practice is to group servers and network devices by their What (application, stack or microservice), Where (datacenter or region), and When (development stage):

- You can use the ansible-inventory CLI command to display the inventory as Ansible sees it.
```bash
(.venv) ➜  python-elasticsearch git:(master) ✗ ansible-inventory -i ./ansible/inventory.yml --list
{
    "_meta": {
        "hostvars": {
            "esdata1": {
                "ansible_host": "192.168.69.3"
            },
            "esmaster1": {
                "ansible_host": "192.168.69.2"
            }
        }
    },
    "all": {
        "children": [
            "data",
            "masters",
            "ungrouped"
        ]
    },
    "data": {
        "hosts": [
            "esdata1"
        ]
    },
    "masters": {
        "hosts": [
            "esmaster1"
        ]
    }
}
```

- Once you have the above requisites ready and Ansible configured and up and running, it’s just a matter of getting the repository accessible with the following command:
```bash
ansible-galaxy install elastic.elasticsearch,7.9.0

[WARNING]: - elastic.elasticsearch (7.10.0) is already installed - use --force to change version to 7.4.2
ansible-galaxy install elastic.elasticsearch,7.4.2 --force --ignore-errors
```

- Once we have our YAML definition, now it’s just a matter of executing the following command. Do it and watch the magic flow!
```bash
ansible-playbook ./ansible/elastic.yml -i ./ansible/inventory.yml --extra-vars "ansible_sudo_pass=yourPassword"
```

- After a few minutes, the above command should get us a nice Elasticsearch cluster up and running. We can verify its status like this:
```bash
$ curl -XGET 'https://esmaster1'
{
  "name" : "esmaster1",
  "cluster_name" : "esprd",
  "cluster_uuid" : "ABC6pGHgRWGhooEjvIElkA",
  "version" : {
    "number" : "7.4.2",
    "build_flavor" : "default",
    "build_type" : "rpm",
    "build_hash" : "7a013de",
    "build_date" : "2019-12-07T14:04:00.380842Z",
    "build_snapshot" : false,
    "lucene_version" : "8.0.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

$ curl -XGET 'https://esmaster1:9200/_cluster/health?pretty'
{
  "cluster_name" : "esprd",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 8,
  "number_of_data_nodes" : 3,
  "active_primary_shards" : 0, "active_shards" : 0,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
```

- Service validate
```bash
systemctl status elasticsearch.service
journalctl -u elasticsearch.service
```