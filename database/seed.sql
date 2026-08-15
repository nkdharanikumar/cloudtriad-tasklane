-- ============================================================
-- Optional sample data.
-- Run after init.sql if you want to see the app populated.
-- Safe to skip, edit, or delete - it's just a starting point.
-- ============================================================

INSERT INTO tasks (title, description, status, priority, due_date) VALUES
    ('Learn Docker', 'Get comfortable with images, containers, and volumes.', 'COMPLETED', 'HIGH', CURRENT_DATE - INTERVAL '5 days'),
    ('Set up Kubernetes cluster', 'Provision a local or cloud cluster to deploy the app to.', 'IN_PROGRESS', 'HIGH', CURRENT_DATE + INTERVAL '3 days'),
    ('Deploy application to EKS', 'Push images to ECR and roll out to an EKS cluster.', 'TODO', 'HIGH', CURRENT_DATE + INTERVAL '10 days'),
    ('Configure GitOps', 'Wire up Argo CD to sync manifests from Git.', 'TODO', 'MEDIUM', CURRENT_DATE + INTERVAL '14 days'),
    ('Monitor application', 'Set up Prometheus and Grafana dashboards.', 'TODO', 'MEDIUM', CURRENT_DATE + INTERVAL '18 days'),
    ('Write API documentation', 'Document all REST endpoints for the team.', 'TODO', 'LOW', NULL);
