
## 2026-09-15 — card `hp-005`
- **Q:** Aurora read replica limits vs RDS?
- **My answer:** -
- **Correct:** Aurora: up to 15 replicas, shared storage (lag ~0), fast promotion. RDS: 5 replicas (MySQL/MariaDB/Postgres), async, lag possible.
- (requeued in scheduler)

## 2026-09-15 — card `hp-001`
- **Q:** EBS gp3 vs gp2 — the upgrade math?
- **My answer:** -
- **Correct:** gp3: 3000 IOPS + 125 MB/s baseline free, provision to 16k IOPS/1000 MB/s, 20% cheaper. gp2: IOPS tied to size (3 IOPS/GB) + burst buckets.
- (requeued in scheduler)

## 2026-09-15 — card `cost-004`
- **Q:** When is Aurora Serverless v2 the exam answer?
- **My answer:** -
- **Correct:** Unpredictable/infrequent DB load, dev/test, multi-tenant SaaS, no capacity planning — fine-grained scaling (vs v1's on/off ACUs).
- (requeued in scheduler)

## 2026-09-15 — card `sec-003`
- **Q:** STS AssumeRole vs AssumeRoleWithWebIdentity?
- **My answer:** -
- **Correct:** AssumeRole: existing identity or cross-account assumes role, temp creds. AssumeRoleWithWebIdentity: federate external OIDC IdP (Cognito, Google) without AWS credentials.
- (requeued in scheduler)

## 2026-09-15 — card `hp-002`
- **Q:** Lambda hard limits to memorize?
- **My answer:** -
- **Correct:** 15 min max run, 10,240 MB memory, 1000 default concurrency, /tmp 10,240 MB, zip 50MB compressed, container image 10GB.
- (requeued in scheduler)

## 2026-09-15 — card `res-005`
- **Q:** ASG target tracking vs step vs scheduled scaling?
- **My answer:** -
- **Correct:** Target tracking: keep metric at target, simplest, preferred. Step: scale in bands around alarm. Scheduled: known predictable load patterns.
- (requeued in scheduler)

## 2026-09-15 — card `hp-003`
- **Q:** DynamoDB on-demand vs provisioned — when each?
- **My answer:** -
- **Correct:** On-demand: unpredictable/spiky/unknown load, pay per request. Provisioned + auto scaling: predictable load, cheaper at scale; reserved capacity for very steady.
- (requeued in scheduler)

## 2026-09-15 — card `res-002`
- **Q:** SQS vs SNS vs EventBridge — one line each?
- **My answer:** -
- **Correct:** SQS: point-to-point queue, pull, decoupling/buffer. SNS: pub/sub fan-out push. EventBridge: event bus w/ rule filtering, SaaS+AWS sources, many targets.
- (requeued in scheduler)

## 2026-09-15 — card `cost-001`
- **Q:** S3 lifecycle minimum-days rules?
- **My answer:** -
- **Correct:** Std-IA min 30d, Glacier Instant Retrieval min 90d, Deep Archive min 180d. Early transition still bills the full minimum.
- (requeued in scheduler)

## 2026-09-15 — card `sec-004`
- **Q:** Secrets Manager vs SSM Parameter Store?
- **My answer:** -
- **Correct:** Secrets Manager: native auto-rotation (RDS etc.), higher $/secret, cross-region replication. Parameter Store: cheaper, SecureString w/ KMS, rotation needs custom logic.
- (requeued in scheduler)

## 2026-09-15 — scenario `res-q4`
- **Q:** RTO must be under 15 minutes for a static site + API, with the lowest possible cost. Which DR strategy?
- **My answer:** -
- **Correct:** Warm standby (scaled-down live copy + data replication + DNS failover) meets a 15-min RTO without active/active cost. Backup/restore RTO is hours.
- (requeued in scheduler)
