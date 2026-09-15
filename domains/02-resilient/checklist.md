# Domain 2 — Design Resilient Architectures (26%)

## 2.1 Design scalable and loosely coupled architectures
- [ ] ELB family: ALB vs NLB vs GWLB — listeners, health checks, cross-zone, sticky sessions
- [ ] Auto Scaling: policies (target tracking, step, scheduled), launch templates, warm pools
- [ ] Queuing vs pub/sub: SQS (standard vs FIFO), SNS (fan-out), EventBridge vs SNS vs SQS
- [ ] Decoupling patterns: worker queues, Lambda + SQS, Step Functions use cases
- [ ] Containers: ECS (EC2 vs Fargate), EKS, ECR — when to choose each
- [ ] Caching at app layer: ElastiCache Redis vs Memcached; CloudFront origin patterns

## 2.2 Design highly available and/or fault-tolerant architectures
- [ ] Multi-AZ vs multi-region: what each buys you (HA vs DR)
- [ ] RDS Multi-AZ vs read replicas; Aurora HA (quorum, global database)
- [ ] Route 53 failover routing, health checks, latency/weighted/geolocation policies
- [ ] S3 resilience: cross-region replication, versioning, 11x9s durability math
- [ ] DR strategies ranked: backup & restore → pilot light → warm standby → multi-site active
- [ ] Graceful degradation: static fallback, reserved instances of last resort
- [ ] Fault domains: AZ-independent design, no single-instance tiers, chaos thinking

## Self-check questions
Question deck: `questions.json`. Design prompts: attempt cold in `practice/answers/`.
