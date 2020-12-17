# Commands to use to rebuild image and push to docker
podman build -f ansible_runner_github.Dockerfile -t excalibrax/ansible_github_runner:v1
podman push excalibrax/ansible_github_runner:latest

# privledged pod creation
oc adm policy add-scc-to-user privileged -z default -n github-runner-tower