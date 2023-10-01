import os
from pathlib import Path

from invoke import task

CONTAINER_REGISTRY_ID = os.environ.get('CONTAINER_REGISTRY_ID')
CONTAINER_URL = f'cr.yandex/{CONTAINER_REGISTRY_ID}/energostat:master'
CONTAINER_ID = os.environ.get('CONTAINER_ID')
SERVICE_ACCOUNT_ID = os.environ.get('SERVICE_ACCOUNT_ID')


@task
def api_gateway_render(c):
    """

    """
    if SERVICE_ACCOUNT_ID and CONTAINER_ID:
        with Path('.ci/api-gateway.yml').open('r') as f_in:
            body = f_in.read() \
                .replace('{{ service_account_id }}', SERVICE_ACCOUNT_ID) \
                .replace('{{ container_id }}', CONTAINER_ID)
            with Path('tmp/api-gateway.yml').open('w') as f_out:
                f_out.write(body)
        print('Write tmp/api-gateway.yml')
    else:
        print('Provide CONTAINER_ID and SERVICE_ACCOUNT_ID env vars for template')


@task
def build(c):
    c.run('poetry install')
    c.run('poetry run pytest')
    c.run('poetry build')
    c.run('poetry export -f requirements.txt --output dist/requirements.txt')
    if CONTAINER_REGISTRY_ID:
        c.run(f'docker build --pull -t {CONTAINER_URL} -f .ci/Dockerfile .')
        c.run(f'docker push {CONTAINER_URL}')
    else:
        print('Provide CONTAINER_REGISTRY_ID env var for docker build')


@task
def deploy(c):
    if CONTAINER_REGISTRY_ID and SERVICE_ACCOUNT_ID:
        cmd = f'yc serverless container revision deploy \
          --container-name energostat \
          --image {CONTAINER_URL} \
          --cores 1 \
          --core-fraction 20 \
          --memory 128MB \
          --concurrency 2 \
          --execution-timeout 30s \
          --service-account-id {SERVICE_ACCOUNT_ID}'
        c.run(cmd)
    else:
        print('Provide CONTAINER_REGISTRY_ID and SERVICE_ACCOUNT_ID env vars for docker deploy')
