# Domain 1 — Design Secure Architectures (30%)

Exam guide task statements. Mark `[x]` only when you can **answer from memory**
(asked cold, without notes) and have drilled the associated questions/cards.

## 1.1 Design secure access controls
- [ ] IAM users, groups, roles, policies; policy evaluation logic (explicit deny > allow)
- [ ] Federation: IAM Identity Center, SAML, STS (AssumeRole, AssumeRoleWithWebIdentity)
- [ ] Permission boundaries, scp's, resource-based vs identity-based policies
- [ ] Root account protection, MFA, Access Analyzer

## 1.2 Design secure workloads and applications
- [ ] Security groups (stateful) vs NACLs (stateless) — when and why
- [ ] Encryption in transit: TLS, ACM, TLS termination at ALB/NLB/CloudFront
- [ ] Application protection: WAF, Shield (Standard/Advanced), DDoS patterns
- [ ] Secrets management: Secrets Manager vs SSM Parameter Store vs KMS
- [ ] VPC security boundaries: endpoints, NAT vs IGW, private subnets

## 1.3 Determine data security controls
- [ ] Encryption at rest: KMS (SSE-KMS vs SSE-S3 vs SSE-C), customer-managed keys
- [ ] S3 security: bucket policies, ACLs, public access block, presigned URLs, Object Lock
- [ ] EBS/EFS/RDS/DynamoDB encryption options
- [ ] CloudHSM use cases; KMS key policies, grants, cross-account access
- [ ] Data classification and compliance-driven controls

## Self-check questions
Attempt BEFORE reading notes (pretesting). Question deck: `questions.json`.
