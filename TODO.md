# Improvements

## I. Can we use a database? What for? SQL or NoSQL?

### Large number of gists/files

Scanning through a large list of gists with possibly large number of files is costly.
We can use NoSQL database (e.g. a key-value storage like Redis) in order to:

1. Cache scanning results and make response for the same search much quicker
2. Cache results to spare GitHub API rate limits
3. Implement our own API rate limits

Further testing of the search API is needed. But there's a suspicion that search can be extremely slow 
for users with the large number of huge gists. It's very likely that gist service doesn't allow Git LFS, 
so the max gist size is limited to 100Mb. We may want to further improve searching the following way:

- When iterating through the file objects of the `/gists/{gist_id}` response, get `size` and `type` fields
- Discard binary blobs as grepping them with regex doesn't make much sense
- Use background daemon to persist large text contents asynchronously as files or in a database 
(MongoDB or even PostgreSQL will [probably](https://blog.rustprooflabs.com/2020/07/postgres-storing-large-text) do)
- Search through the saved texts once daemon finishes its job

### Respecting GitHub API rate limits

Using GitHub API Key allows 5k requests per hour. Depending on how our service usage looks like, we may bump into
rate limit errors from GitHub API side. In this case we may want to use a *request queue*.
In the naive implementation a key-value DB like Redis can be used to implement time bucket rate limiting
(set counter of N requests with expiration of K time units, decrease the counter if positive or refuse if negative).
Leaky bucket rate limiting can be slightly better alternative, as it provides a buffer for request bursts
(use [https://docs.python.org/3/library/collections.html#collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
as a buffer limited by a given bucket size, + rate limiting requests to API to simulate leaking).
In conjunction with Redis, Postgres queue-like table can also be used for background retries once limits are reset
(client is given a timestamp when retry will happen)

## II. How can we protect the api from abusing it?

1. API Rate limiting (e.g. Redis to store client IP address and counter)
2. CDN / DDoS protection
3. Firewall
4. Service scaling + Load balancing (HAProxy or Cloud-based Ingress/Load balancer)

### III. How can we deploy the application in a cloud environment?

1. Small scale solution:
- VPS Linux in the Cloud (e.g. DigitalOcean, Exoscale, etc.)
- Ansible playbook to provision the server and deploy the app 
(e.g. see [my playbook](https://github.com/pilosus/dienstplan-deploy/) for a Slack bot app)

2. Med-Big scale solution:
- Terraform for AWS/GCP/Azure, e.g. building & pushing Docker image to AWS ECR, VPC + Ingress/Egress + Load Balancer, ECS/EKS
  (e.g. see [my Terraform](https://github.com/pilosus/dienstplan-tf) config for the same app deploy to DO App Platform)


### IV. How can we be sure the application is alive and works as expected when deployed into a cloud environment?

- API health check endpoint + cloud provider automatic liveliness probes (or external Saas like Pingdom)
- Alert management (Prometheus + Grafana): error status code rates, 
   response time (avg, percentile 90) increase over time window, dashboards for service health monitoring
- Error tracking services (Sentry or the like): get notifications about unhandled exceptions in production environment
- Logging (ELK stack)

### V. Any other topics you may find interesting and/or important to cover

- Instead of Flask development server, use production-grade app server like `uWSGI` or `Gunicorn`.
  (Optionally) use a proxy server like `nginx` to serve static files and or do advanced caching, load balancing, etc.
- CI/CD pipelines to ensure quality (GitHub Actions/Workflows or GitLab or Jenkins)
- Software composite analysis & Dependency management: 
  vulnerability scanner & dependency updater (GitHub Dependabot), 
  open-source license compliance tools (see my [license checker](https://github.com/pilosus/pip-license-checker) 
  and contributions to [third-parties](https://github.com/scarletcomply/license-finder/blob/main/CHANGELOG.md))
