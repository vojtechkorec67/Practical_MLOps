# Practical MLOps

Simple Python MLOps training project with:
- unit tests + linting,
- CI in GitHub Actions,
- container build/push to GHCR,
- load testing on `staging`,
- continuous deployment of container image to Azure App Service.

## What This Repository Demonstrates

This repository is intentionally small, but it covers the full DevOps/MLOps flow:

1. **Code quality checks** (`make lint`)
2. **Unit tests + coverage** (`make test`)
3. **Containerization** (Docker image in GHCR)
4. **Branch-based automation** (`main` vs `staging`)
5. **Load testing** (Locust on staging branch)
6. **Automatic deployment** (Azure App Service on push to main)

---

## Project Structure

```text
Practical_MLOps/
├── hello.py                          # Core function: add(x, y)
├── app.py                            # Flask API exposing /health and /add
├── test_hello.py                     # Unit tests for hello.add
├── locustfile.py                     # Load test scenario for API endpoints
├── requirements.txt                  # Python dependencies
├── Makefile                          # Local automation commands
├── Dockerfile                        # Container build definition
└── .github/workflows/
        ├── python-app.yml                # CI: lint + tests on pushes
        ├── docker-publish.yml            # Build/push image + deploy to Azure
        └── load-test.yml                 # Load test on staging branch
```

---

## Application Endpoints

The API is served by `app.py`:

- `GET /health`
    - Returns service health.
    - Example response: `{"status":"healthy"}`

- `GET /add?x=5&y=3`
    - Returns addition result.
    - Example response: `{"x":5.0,"y":3.0,"result":8.0}`

---

## Local Setup

### Prerequisites
- Python 3.10+
- `pip`
- (optional) Docker

### 1) Clone project
```bash
git clone https://github.com/vojtechkorec67/Practical_MLOps.git
cd Practical_MLOps
```

### 2) Create virtual environment
```bash
python3 -m venv ~/.Practical_MLOps
source ~/.Practical_MLOps/bin/activate
```

### 3) Install dependencies
```bash
make install
```

---

## Makefile Commands

```bash
make all      # install + lint + test
make install  # install dependencies from requirements.txt
make lint     # run pylint on hello.py
make test     # run pytest with coverage
```

---

## Local API Run

Run locally:
```bash
python app.py
```

Test endpoints:
```bash
curl -i http://localhost:5000/health
curl -i "http://localhost:5000/add?x=5&y=3"
```

---

## Docker

Build image locally:
```bash
docker build -t practical-mlops:local .
```

Run container locally:
```bash
docker run --rm -p 5000:5000 practical-mlops:local
```

Test API from host:
```bash
curl -i http://localhost:5000/health
```

---

## Branch Strategy

- **`main` branch**
    - Primary branch.
    - Triggers CI + container build + Azure deployment.

- **`staging` branch**
    - Performance validation branch.
    - Triggers Locust load test workflow.

Typical flow:
1. Push feature changes to `staging`
2. Verify load-test results
3. Merge to `main`
4. Auto-deploy to Azure from `main`

## End-to-End Process (Step by Step)

This is the exact practical sequence used in this repository:

1. Update code locally.
2. (Optional but recommended) validate locally with `make all`.
3. Push to `staging` branch:
    ```bash
    git checkout staging
    git add .
    git commit -m "your change"
    git push origin staging
    ```
4. GitHub triggers `load-test.yml` on staging.
5. Review load-test workflow result and artifacts in GitHub Actions.
6. If staging checks are OK, merge `staging` into `main`.
7. Push/merge to `main` triggers:
    - `python-app.yml` (install/lint/test matrix),
    - `docker-publish.yml` (build + push container + deploy).
8. Docker image is built and pushed to GHCR with unique tag `sha-<commit>`.
9. Azure App Service is updated to that exact SHA image tag.
10. Validate production endpoints:
     - `/health`
     - `/add?x=5&y=3`

---

## GitHub Actions Workflows

### 1) `python-app.yml` (CI)
Triggered on push. Runs matrix tests on Python `3.10`, `3.11`, `3.13`:
- install dependencies (`make install`)
- lint (`make lint`)
- unit tests with coverage (`make test`)

### 2) `docker-publish.yml` (Build + Deploy)
Triggered on push/PR to `main`:
- builds Docker image,
- pushes image to **GitHub Container Registry** (`ghcr.io/vojtechkorec67/practical_mlops`),
- uses unique image tag `sha-<commit>`,
- on push to `main` deploys that exact tag to Azure App Service.

### 3) `load-test.yml` (Performance on Staging)
Triggered on push/PR to `staging`:
- starts API app,
- runs Locust headless test,
- stores CSV metrics as workflow artifact.

---

## Container Registry (GHCR)

Container images are published to:
```text
ghcr.io/vojtechkorec67/practical_mlops
```

Image tags include:
- branch tags,
- SHA-based immutable tags (`sha-...`).

SHA tags are used for reliable, traceable deployments.

---

## Azure Deployment

Application is deployed to Azure App Service (Linux, container-based).

Current app URL format:
```text
https://<app-name>.azurewebsites.net
```

Deployment workflow uses GitHub secret:
- `AZURE_WEBAPP_PUBLISH_PROFILE`

How it works:
1. GitHub Actions builds and pushes image tag `sha-<commit>`.
2. Deploy step points App Service to that exact image tag.
3. Azure runs that container version.

You can verify active deployed image via CLI:
```bash
az webapp show \
    --name practical-mlops \
    --resource-group practical-mlops_group \
    --query "siteConfig.linuxFxVersion" \
    -o tsv
```

---

## Load Testing Details

Locust scenario in `locustfile.py`:
- weighted traffic to `/add` and `/health`,
- simulated concurrent users,
- request-level metrics exported to CSV.

This is used as a branch gate before promoting to main.

---

## Troubleshooting Quick Notes

- If Azure does not update after new image:
    - check latest `docker-publish.yml` run is green,
    - verify deployed tag in `siteConfig.linuxFxVersion`.

- If deployment auth fails:
    - re-download publish profile,
    - update `AZURE_WEBAPP_PUBLISH_PROFILE` GitHub secret.

- If API endpoint fails:
    - check App Service logs (`Log stream`),
    - verify container image/tag exists in GHCR.

---

## License

MIT
