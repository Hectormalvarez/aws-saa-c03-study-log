# Service Comparison Tables

The exam's core skill: choosing between similar services. Drill these until reflexive.

## Load Balancers
| | ALB | NLB | GWLB |
|---|---|---|---|
| Layer | 7 (HTTP/S, gRPC) | 4 (TCP/TLS/UDP) | 3 (gateway) |
| Static IP | no (DNS only) | yes (Elastic IP) | yes |
| WAF | yes | no | no |
| Client IP preserved | no (XFF header) | yes | yes |
| Use when | path/host routing, WAF | extreme perf, static IP | inline appliances |

## Queues vs Pub/Sub
| | SQS | SNS | EventBridge |
|---|---|---|---|
| Model | pull, point-to-point | push, fan-out | rules-based bus |
| Consumers | 1 app per message | many subscribers | many targets w/ filtering |
| Retention | up to 14 days | none (async retries) | archive (opt) |
| Best for | decoupling, buffering | notifications fan-out | event routing, SaaS |

## Storage Decision
| Need | Answer |
|---|---|
| Object, web-served, lifecycle | S3 |
| Shared POSIX file system, NFS | EFS (elastic) |
| High-perf POSIX / HPC | FSx for Lustre |
| Windows shares / AD | FSx for Windows |
| Block, attached to 1 instance | EBS |
| Ephemeral scratch, highest IOPS | Instance store |
| Hybrid on-prem cache/backup | Storage Gateway |

## Database Decision
| Need | Answer |
|---|---|
| Relational, strong SQL | RDS / Aurora |
| Unpredictable relational load | Aurora Serverless v2 |
| Key-value / document, huge scale, predictable PK | DynamoDB |
| Microsecond reads on DynamoDB | DAX |
| Caching (SQL or general) | ElastiCache Redis |
| Simple multi-node cache, no persistence | ElastiCache Memcached |
| In-memory for RDS queries | ElastiCache (lazy/write-through) |

## RDS vs Aurora HA facts
| | RDS Multi-AZ | Aurora |
|---|---|---|
| Standby | sync, not readable | 6 storage copies, 3 AZs |
| Read replicas | 5 (async, lag) | 15 (shared storage, ~no lag) |
| Failover | 1-2 min DNS switch | <30s to reader promotion |
| Cross-region | snapshot/replica | Global Database (<1s lag) |

## EC2 Purchase Options
| Option | Discount | Flexibility | Use |
|---|---|---|---|
| On-Demand | 0 | full | spiky, unpredictable, new apps |
| Spot | up to 90% | can lose in 2 min | batch, stateless, fault-tolerant |
| Reserved | 30-72% | locked attributes | steady-state, 1-3 yr |
| Savings Plan | similar | $-commit, cross-family | steady spend, mixed fleet |

## S3 Storage Classes (with minimums)
| Class | Min days | Retrieval | Use |
|---|---|---|---|
| Standard | – | instant | frequent |
| Std-IA | 30 | instant | infrequent, instant |
| One-Zone-IA | 30 | instant | infrequent, non-critical |
| Intelligent-Tiering | – | instant, no retrieval fee | unknown/changing pattern |
| Glacier IR | 90 | ms | archive w/ instant access |
| Glacier Flexible | 90 | mins–hrs | archive |
| Deep Archive | 180 | 12h+ | compliance long-tail |

## Networking quick facts
- NAT Gateway = outbound only; IGW = in+out; VPC endpoints = private AWS service access (no NAT cost)
- Enhanced Networking: ENA (up to 100 Gbps); EFA = HPC + MPI
- Route 53 policies: simple, weighted, latency, failover, geolocation, geoproximity, multivalue
- Global Accelerator: anycast IPs, TCP/UDP, no caching; CloudFront: HTTP caching at edge
