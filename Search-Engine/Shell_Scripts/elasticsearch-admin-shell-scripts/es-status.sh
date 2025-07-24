#/bin/bash

declare -A ES_ENV
ES_ENV[01]=localhost

start_time=$(date)
echo "start time = $start_time"

for env in "${!ES_ENV[@]}"
  do
	eachenv=${ES_ENV[$env]}
	http_code=$(curl -I -silent http://$eachenv:9200 | head -n 1  |cut -d$' ' -f2)
	echo $http_code
	if [ $http_code == "200" ]; then
		#health_output=$(curl -I -silent http://$eachenv:9200/_cat/health)
        health_output=$(curl http://$eachenv:9200/_cat/health) 
	    # echo $health_output > healthoutput.txt
   	    echo "ENV = "$env
		echo "health_output = "$health_output
		echo "http_code = "$http_code
		status=$(echo $health_output | awk '{ print $4}')

		if [ "$status" != "green" ]; then
	        #echo "Elasticsearch on $env is $status. Restart Elasticsaerch on down-node. Kibana: GET _cat/nodes" | /usr/bin/mailx -s "ALERT:ENV$env :$eachenv:- Elasticsearch is $status" -r "ES DEV Team<${from}>" ${to}
			echo "Elasticsearch on $env is $status. Restart Elasticsaerch on down-node. Kibana: GET _cat/nodes"
		fi	
	else
		echo "Elasticsearch on $env is not reachable. The Main-Elasticsearch node might be down, so Kibana may not work. Check on terminal-vm and execute command: "curl -get http:2nd-es-node:9200/_cat/nodes", where 2nd-es-node = another node on the $env cluster. Then bring up the ES on 1st node" | /usr/bin/mailx -s "ALERT:ENV$env :$eachenv:- elasticsearch is not reachable" -r "ES DEV Team<${from}>" ${to}
	fi
done
