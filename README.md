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
'''
Step 2: Provision Kubernetes Cluster
Create a 2-node local cluster using Kind:

Bash
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
