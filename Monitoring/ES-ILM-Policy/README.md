### Elasticsearch ILM(Index Life-Cycle Management)

<i>You can configure index lifecycle management (ILM) policies to automatically manage indices according to your performance, resiliency, and retention requirements. For example, you could use ILM to:
- Spin up a new index when an index reaches a certain size or number of documents
- Create a new index each day, week, or month and archive previous ones
- Delete stale indices to enforce data retention standards

You can create and manage index lifecycle policies through Kibana Management or the ILM APIs. Default index lifecycle management policies are created automatically when you use Elastic Agent, Beats, or the Logstash Elasticsearch output plugin to send data to the Elastic Stack

