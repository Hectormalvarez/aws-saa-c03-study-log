# Domain 4 — Design Cost-Optimized Architectures (20%)

## 4.1 Design cost-optimized storage
- [ ] S3 lifecycle transitions and the minimum-days rules (30d IA, 90d Glacier, 180d Deep Archive)
- [ ] Intelligent-Tiering for unknown/changing access patterns (no retrieval fees)
- [ ] EBS: gp3 vs gp2 pricing, snapshot strategy, unattached-volume cleanup
- [ ] S3 vs EBS vs EFS cost lens for the same workload

## 4.2 Design cost-optimized compute
- [ ] Purchase options: On-Demand, Spot (interruption handling), Reserved, Savings Plans
- [ ] Spot for stateless/fault-tolerant ASG workloads; Spot Fleet, interruption notices
- [ ] Serverless as cost answer: Lambda vs always-on EC2 for spiky/idle workloads
- [ ] Right-sizing: Compute Optimizer, instance families, stopping dev/test instances

## 4.3 Design cost-optimized databases
- [ ] Aurora Serverless v2 for unpredictable/infrequent workloads
- [ ] DynamoDB on-demand vs provisioned with auto scaling
- [ ] ElastiCache to cut database load (cost-per-query logic)
- [ ] Aurora read replicas vs adding DB instances for read scaling cost

## Self-check questions
Question deck: `questions.json`.
