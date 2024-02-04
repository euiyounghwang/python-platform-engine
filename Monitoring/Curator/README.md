
### Elasticsearch Curator

Elasticsearch Curator helps you curate, or manage, your Elasticsearch indices and snapshots by:
- Obtaining the full list of indices (or snapshots) from the cluster, as the actionable list
- Iterate through a list of user-defined filters to progressively remove indices (or snapshots) from this actionable list as needed.
- Perform various actions on the items which remain in the actionable list.
- Curator-Airflow Example(<i>https://github.com/occidere/airflow-example/blob/master/dags/curator_example.py, https://ikeptwalking.com/taking-elasticsearch-snapshots-using-curator/</i>)
- Installation Local: Curator is breaking into version dependent releases. Curator 6.x will work with Elasticsearch 6.x, Curator 7.x will work with Elasticsearch 7.x, and when it is released, Curator 8.x will work with Elasticsearch 8.x.
```bash
(.venv) ➜  python-elasticsearch git:(master) ✗ poetry add elasticsearch-curator       
Using version ^8.0.8 for elasticsearch-curator

Updating dependencies
Resolving dependencies... (0.8s)

Package operations: 6 installs, 0 updates, 0 removals

  • Installing elastic-transport (8.12.0)
  • Installing elasticsearch8 (8.8.2)
  • Installing voluptuous (0.14.1)
  • Installing ecs-logging (2.0.2)
  • Installing es-client (8.8.2.post1)
  • Installing elasticsearch-curator (8.0.8)

Writing lock file
```

- Installation Ubuntu (Data Node, 192.168.71.2)
```bash
(.venv) ➜  Curator git:(master) scp ./* devuser@192.168.71.2:/home/devuser/ES/curator-5.8.1
Job-run-delete-data.sh                                                                                                                   100%  362   307.7KB/s   00:00    
README.md                                                                                                                                100% 3400     5.7MB/s   00:00    
curator-config.yml                                                                                                                       100%  531   432.9KB/s   00:00    
curator-run-job.sh                                                                                                                       100%  386   465.4KB/s   00:00    
delete-indices.yml  

(.venv) devuser@ubuntu-node-1:~/ES/curator-5.8.1$ vi ./curator-run-job.sh
#!/bin/bash
set -e

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# echo $SCRIPTDIR

cd $SCRIPTDIR
#cd ..
filepath=`pwd`
# echo $filepath

source $filepath/.venv/bin/activate

# $filepath/.venv/bin/curator --config ./Curator/curator-config.yml --dry-run ./Curator/delete-indices.yml
curator --config ./curator-config.yml --dry-run ./delete-indices.yml
~

(.venv) devuser@ubuntu-node-1:~/ES/curator-5.8.1$ ./curator-run-job.sh
2024-01-24 21:31:36,423 INFO      Preparing Action ID: 1, "delete_indices"
2024-01-24 21:31:36,423 INFO      Creating client object and testing connection
2024-01-24 21:31:36,423 INFO      Creating client object and testing connection
2024-01-24 21:31:36,525 INFO      GET http://192.168.71.1:9209/ [status:200 duration:0.101s]
2024-01-24 21:31:36,556 INFO      GET http://192.168.71.1:9209/_nodes/_local [status:200 duration:0.031s]
2024-01-24 21:31:36,598 INFO      GET http://192.168.71.1:9209/_cluster/state/master_node [status:200 duration:0.041s]
2024-01-24 21:31:36,598 INFO      Trying Action ID: 1, "delete_indices": No description given
2024-01-24 21:31:36,630 INFO      GET http://192.168.71.1:9209/*/_settings?expand_wildcards=open,closed [status:200 duration:0.031s]
2024-01-24 21:31:36,633 INFO      Skipping action "delete_indices" due to empty list: <class 'curator.exceptions.NoIndices'>
2024-01-24 21:31:36,634 INFO      Action ID: 1, "delete_indices" completed.
2024-01-24 21:31:36,634 INFO      All actions completed.

```


### Run Curator
```bash
# Test
(.venv) ➜  python-elasticsearch git:(master) ✗ /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/.venv/bin/curator --config  /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/Curator/curator-config.yml --dry-run  /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/Curator/delete-indices.yml

(.venv) ➜  python-elasticsearch git:(master) ✗ curator --config ./Curator/curator-config.yml --dry-run ./Curator/delete-indices.yml
2024-01-24 14:53:18,271 INFO      Preparing Action ID: 1, "delete_indices"
2024-01-24 14:53:18,271 INFO      Creating client object and testing connection
2024-01-24 14:53:18,271 INFO      Creating client object and testing connection
2024-01-24 14:53:18,300 INFO      GET http://localhost:9209/ [status:200 duration:0.028s]
2024-01-24 14:53:18,308 INFO      GET http://localhost:9209/_nodes/_local [status:200 duration:0.008s]
2024-01-24 14:53:18,331 INFO      GET http://localhost:9209/_cluster/state/master_node [status:200 duration:0.023s]
2024-01-24 14:53:18,332 INFO      Trying Action ID: 1, "delete_indices": No description given
2024-01-24 14:53:18,339 INFO      GET http://localhost:9209/*/_settings?expand_wildcards=open,closed [status:200 duration:0.007s]
2024-01-24 14:53:18,341 INFO      Skipping action "delete_indices" due to empty list: <class 'curator.exceptions.NoIndices'>
2024-01-24 14:53:18,341 INFO      Action ID: 1, "delete_indices" completed.
2024-01-24 14:53:18,341 INFO      All actions completed.
```


### Configure Curator Cronjob
```bash
## Delete older index of Elasticsearch

sudo */15 * * * * root /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/.venv/bin/curator --config  /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/Curator/curator-config.yml --dry-run  /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/Curator/delete-indices.yml

sudo 0 5 * * * root /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/.venv/bin/curator --config  /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/Curator/curator-config.yml /Users/euiyoung.hwang/ES/Python_Workspace/python-elasticsearch/Curator/delete-indices.yml

```