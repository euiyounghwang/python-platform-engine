
### Elasticsearch Curator

<i>Elasticsearch Curator helps you curate, or manage, your Elasticsearch indices and snapshots by:
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

# cd $SCRIPTDIR
# cd ..
# filepath=`pwd`
# echo $filepath

# source $filepath/.venv/bin/activate
source $SCRIPTDIR/.venv/bin/activate

NOW=$(date +"%y-%m-%d %T")
echo "[$NOW] ***** Start *****" >> $SCRIPTDIR/debug.log

# $filepath/.venv/bin/curator --config ./Curator/curator-config.yml --dry-run ./Curator/delete-indices.yml
# Test
curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/delete-indices.yml | tee -a $SCRIPTDIR/debug.log

# -- snapshot
# curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/action_snapshot.yml
# curator --config $SCRIPTDIR/curator-config.yml --dry-run $SCRIPTDIR/restore_snapshot.yml
# Run
# curator --config ./Curator/curator-config.yml ./Curator/delete-indices.yml
# curator --config $SCRIPTDIR/curator-config.yml $SCRIPTDIR/delete-indices.yml

echo "[$NOW] ***** End *****" >> $SCRIPTDIR/debug.log
~

# curator for delete
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

# curator for snapshot
(.venv) ➜  python-platform-engine git:(master) ✗ ./Monitoring/Curator/curator-run-job.sh
2024-02-10 16:43:31,967 INFO      Preparing Action ID: 1, "snapshot"
2024-02-10 16:43:31,967 INFO      Creating client object and testing connection
2024-02-10 16:43:31,967 INFO      Creating client object and testing connection
2024-02-10 16:43:31,977 INFO      GET http://localhost:9203/ [status:200 duration:0.008s]
2024-02-10 16:43:31,980 INFO      GET http://localhost:9203/_nodes/_local [status:200 duration:0.003s]
2024-02-10 16:43:31,984 INFO      GET http://localhost:9203/_cluster/state/master_node [status:200 duration:0.004s]
2024-02-10 16:43:31,984 INFO      Trying Action ID: 1, "snapshot": Snapshot log-production- prefixed indices older than 1 day (based on index creation_date) with the default snapshot name pattern of 'curator-%Y%m%d%H%M%S'.  Wait for the snapshot to complete.  Do not skip the repository filesystem access check.  Use the other options to create the snapshot.
2024-02-10 16:43:31,987 INFO      GET http://localhost:9203/*/_settings?expand_wildcards=open,closed [status:200 duration:0.002s]
2024-02-10 16:43:31,991 INFO      HEAD http://localhost:9203/_alias/test_index-20240201 [status:404 duration:0.002s]
2024-02-10 16:43:31,992 INFO      HEAD http://localhost:9203/_alias/test_index-20240209 [status:404 duration:0.002s]
2024-02-10 16:43:31,994 INFO      GET http://localhost:9203/test_index-20240201,test_index-20240209/_settings [status:200 duration:0.001s]
2024-02-10 16:43:31,995 INFO      HEAD http://localhost:9203/_alias/test_index-20240201 [status:404 duration:0.002s]
2024-02-10 16:43:31,997 INFO      HEAD http://localhost:9203/_alias/test_index-20240209 [status:404 duration:0.001s]
2024-02-10 16:43:31,998 INFO      GET http://localhost:9203/test_index-20240201,test_index-20240209/_settings [status:200 duration:0.001s]
2024-02-10 16:43:32,002 INFO      GET http://localhost:9203/test_index-20240201,test_index-20240209/_settings [status:200 duration:0.002s]
2024-02-10 16:43:32,004 INFO      GET http://localhost:9203/_snapshot/my_backup [status:200 duration:0.002s]
2024-02-10 16:43:32,053 INFO      POST http://localhost:9203/_snapshot/my_backup/_verify [status:200 duration:0.048s]
2024-02-10 16:43:32,076 INFO      GET http://localhost:9203/_snapshot/_status [status:200 duration:0.023s]
2024-02-10 16:43:32,076 INFO      Creating snapshot "test_index-20240210" from indices: ['test_index-20240201', 'test_index-20240209']
2024-02-10 16:43:32,136 INFO      PUT http://localhost:9203/_snapshot/my_backup/test_index-20240210?wait_for_completion=false [status:200 duration:0.060s]
2024-02-10 16:43:32,140 INFO      GET http://localhost:9203/_snapshot/my_backup/test_index-20240210 [status:200 duration:0.004s]
2024-02-10 16:43:32,140 INFO      Snapshot test_index-20240210 still in progress.
2024-02-10 16:43:41,168 INFO      GET http://localhost:9203/_snapshot/my_backup/test_index-20240210 [status:200 duration:0.021s]
2024-02-10 16:43:41,172 INFO      Snapshot test_index-20240210 successfully completed.
2024-02-10 16:43:41,184 INFO      GET http://localhost:9203/_snapshot/my_backup/test_index-20240210 [status:200 duration:0.011s]
2024-02-10 16:43:41,184 INFO      Snapshot backup-20240210224924 successfully completed.
2024-02-10 16:43:41,184 INFO      Action ID: 1, "snapshot" completed.
2024-02-10 16:43:41,184 INFO      All actions completed.
(.venv) ➜  python-platform-engine git:(master) ✗ 

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