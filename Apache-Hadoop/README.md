
# Apache Hadoop
- URL :  <i>https://hadoop.apache.org/</i>

The Apache Hadoop software library is a framework that allows for the distributed processing of large data sets across clusters of computers using simple programming models. It is designed to scale up from single servers to thousands of machines, each offering local computation and storage <i>

Basic architecture of Apache Hadoop

![Alt text](../screenshot/HADOOP.png)

The architectural design of HDFS is composed of two processes: 
- a process known as the NameNode holds the metadata for the filesystem : `The NameNode` is the most important machine in HDFS. It stores metadata for the entire filesystem: filenames, file permissions, and the location of each block of each file. To allow fast access to this information, the NameNode stores the entire metadata structure in memory. The NameNode also tracks the replication factor of blocks, ensuring that machine failures do not result in data loss.
- one or more DataNode processes store the blocks that make up the files : The machines that store the blocks within HDFS are referred to as DataNodes. `DataNodes` are typically commodity machines with large storage capacities. Unlike the NameNode, HDFS will continue to operate normally if a DataNode fails. When a DataNode fails, the NameNode will replicate the lost blocks to ensure each block meets the minimum replication factor.

The following section describes how to interact with HDFS using the built-in commands.

![Alt text](../screenshot/Name-Node.png)

Interacting with HDFS
Interacting with HDFS is primarily performed from the command line using the script named hdfs. The hdfs script has the following usage:

```bash
$ hdfs COMMAND [-option <arg>]
```