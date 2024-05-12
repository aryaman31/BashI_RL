helm create helm-create
helm template . --name my-release-name
helm upgrade my-release-name . --install --dry-run --debug
helm search httpbin
helm package .
l ~/.helm/repository/local
helm dependency update
helm install local/helm-httpbin --name cloudatine
k get po
k get svc
watch kubectl get po
watch kubectl get svc
k port-forward svc/cloudatine-helm-httpbin 4242:80
helm delete cloudatine --purge
kustomize build base
mkdir -p overlays/official
cd overlays/official
touch kustomization.yaml
kustomize edit fix
kustomize edit add base ../../base
kustomize edit set image mccutchen/go-httpbin=kennethreitz/httpbin:latest
tee deployment-port.yaml <<EOF \
apiVersion: apps/v1beta2\
kind: Deployment\
metadata:\
  name: kustomize-httpbin\
spec:\
  template:\
    spec:\
      containers:\
      - name: httpbin\
        ports:\
        - containerPort: 8080\
          \$patch: delete\
        - name: http\
          containerPort: 80\
          protocol: TCP\
EOF
kustomize edit add patch deployment-port.yaml
k apply --dry-run -o yaml -k kustomize-httpbin/base