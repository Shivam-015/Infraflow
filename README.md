# InfraFlow - Kubernetes Local Observability Stack

A production-ready setup for deploying Prometheus, Grafana, and Prometheus Operator on a local Kubernetes cluster (Kind) with automated custom TLS certificate generation for Admission Webhooks.

---

## 📋 Prerequisites

Ensure your host machine (Linux / Ubuntu / WSL2) has the following tools installed:

- **Docker Engine**
- **kubectl CLI**
- **Kind (Kubernetes in Docker)**
- **Helm 3**
- **OpenSSL**

---

## 🚀 Quick Start Guide

### Step 1: Install System Dependencies

Run the following commands to install required tools:

```bash
# Update package lists and install utilities
sudo apt-get update -y && sudo apt-get install -y curl ca-certificates openssl git

# Install Docker Engine
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER
newgrp docker

# Install kubectl CLI
curl -LO "[https://dl.k8s.io/release/$(curl](https://dl.k8s.io/release/$(curl) -L -s [https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl](https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl)"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Kind
[ $(uname -m) = x86_64 ] && curl -Lo ./kind [https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-amd64](https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-amd64)
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Install Helm 3
curl [https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3](https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3) | bash
```
### Step 2: Provision Kubernetes Cluster
Create a 2-node local cluster using Kind:

```Bash
# Clean up any existing cluster named 'infraflow'
kind delete cluster --name infraflow || true

# Define cluster configuration
cat <<EOF> /tmp/kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
EOF

# Create cluster
kind create cluster --name infraflow --config /tmp/kind-config.yaml

# Verify node status
kubectl get nodes
```
### Step 3: Setup Namespace & Webhook TLS Secret
Generate self-signed TLS certificates to satisfy Prometheus Operator admission webhook expectations (/cert/cert and /cert/key):

```Bash
# Create temporary directory for TLS keys
mkdir -p /tmp/k8s-certs

# Generate self-signed TLS certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /tmp/k8s-certs/key \
  -out /tmp/k8s-certs/cert \
  -subj "/CN=prometheus-kube-prometheus-admission.monitoring.svc"

# Create monitoring namespace
kubectl create namespace monitoring

# Create generic TLS secret expected by the operator
kubectl create secret generic prometheus-kube-prometheus-admission \
  --from-file=cert=/tmp/k8s-certs/cert \
  --from-file=key=/tmp/k8s-certs/key \
  -n monitoring
```
### Step 4: Deploy kube-prometheus-stack
Add the official Helm repository and deploy the observability stack:

```Bash
# Add Helm community repository
helm repo add prometheus-community [https://prometheus-community.github.io/helm-charts](https://prometheus-community.github.io/helm-charts)
helm repo update

# Install/Upgrade kube-prometheus-stack release
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --set prometheusOperator.admissionWebhooks.enabled=true \
  --set prometheusOperator.admissionWebhooks.patch.enabled=false

# Restart operator to reload mounted secrets
kubectl rollout restart deployment prometheus-kube-prometheus-operator -n monitoring
```

### Step 5: Verify Deployment Status
Check that all pods in the monitoring namespace reach Running status:
```Bash
kubectl get pods -n monitoring -w

```

### Step 6: Access Dashboards
🔑 Retrieve Grafana Admin Password:
```bash 
kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo


###📊 Access Grafana UI
Start port-forwarding for Grafana:

Bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80 --address 0.0.0

URL: http://localhost:3000
Username: admin

📈 Access Prometheus UI
In a separate terminal window, start port-forwarding for Prometheus:

Bash
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090 --address 0.0.0.0
URL: http://localhost:9090
```
