pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: env.BRANCH_NAME, url: 'https://github.com/awsconsultant9/apis'
            }
        }
        stage('Build') {
            steps {
                echo "Building branch ${env.BRANCH_NAME}"
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy_to_prod.sh'
            }
        }
    }
}
