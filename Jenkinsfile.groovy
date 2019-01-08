
node() {
    checkoutStage()
    testStage()
    buildAndDeployImageStage()
}


def checkoutStage() {
    stage('Checkout') {
        checkout scm
    }
}


def testStage() {
    stage('Test') {
        docker.image('python:3.7-slim').inside("-v/var/jenkins:/var/jenkins") {
            withEnv(['XDG_CACHE_HOME=/var/jenkins']) {
                sh('pip3 install -U pip')
                sh('pip3 install -r requirements.txt')
                sh('pip3 install pytest')
            }
            try {
                sh('pytest --junitxml target/results.xml')
            } finally {
                junit('target/results.xml')
            }
       }
    }
}


def buildAndDeployImageStage() {
    stage('Build & Deploy') {
        docker.image('python:3.7-slim').inside("-v/var/jenkins:/var/jenkins") {
            withEnv(['XDG_CACHE_HOME=/var/jenkins', 'ANSIBLE_HOST_KEY_CHECKING=False']) {
                sh('pip3 install ansible docker-py')

                def key = sshUserPrivateKey(credentialsId: 'dev.loc', keyFileVariable: 'KEY')
                def vault = file(credentialsId: 'ansible_vault', variable: 'VAULT')
                withCredentials([key, vault]) {
                    sh("ansible-playbook --private-key=$KEY --vault-password-file=$VAULT --inventory=ansible/hosts.ini ansible/playbook.yml -e build_id=${env.BUILD_ID}")
                }
            }
        }
   }
}
