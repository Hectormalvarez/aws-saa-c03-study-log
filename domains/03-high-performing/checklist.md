# Domain 3 — Design High-Performing Architectures (24%)

## 3.1 Determine high-performing and/or scalable storage
- [ ] S3 storage classes & retrieval times: Standard, Std-IA, One-Zone-IA, Glacier IR/Flex/DR, Deep Archive
- [ ] Lifecycle policies + Intelligent-Tiering; when each is the cost/perf answer
- [ ] EBS volume types: gp2 vs gp3, io1/io2, st1/sc1 — IOPS vs throughput tradeoffs
- [ ] EFS (performance modes, throughput modes) vs FSx (Lustre, Windows, ONTAP, OpenZFS)
- [ ] Instance store: ephemeral, when it's the right answer
- [ ] Storage gateway modes (file, volume, tape)

## 3.2 Design high-performing and elastic compute
- [ ] EC2 families (general/compute/memory/storage-optimized) and picking by workload
- [ ] Placement groups: cluster vs spread vs partition
- [ ] Lambda: limits (15 min, memory), concurrency, cold starts, SnapStart, when NOT to use
- [ ] Compute elasticity: ASG + ELB, instance mix (on-demand/spot/reserved), capacity providers

## 3.3 Determine high-performing networking
- [ ] Enhanced networking: ENA vs EFA (HPC)
- [ ] CloudFront: edge caching, origin types, signed URLs, OAC for S3
- [ ] Global Accelerator vs CloudFront (TCP/UDP vs HTTP caching)
- [ ] Route 53 latency-based routing; VPC peering vs Transit Gateway throughput implications

## 3.4 Determine high-performing database solutions
- [ ] RDS: read replicas (scaling reads), Multi-AZ (availability, NOT perf), instance sizing
- [ ] Aurora: storage auto-scaling, up to 15 read replicas, Aurora Serverless v2, Global Database
- [ ] DynamoDB: partition key design, hot partitions, on-demand vs provisioned, DAX caching
- [ ] ElastiCache: Redis (complex/persistent) vs Memcached (simple/multi-node); lazy vs write-through
- [ ] Relational vs NoSQL vs in-memory decision matrix by access pattern

## Self-check questions
Question deck: `questions.json`.
