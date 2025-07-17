pipeline {
    agent any

    environment {
        TARGET_HOST = "ubuntu@13.62.19.114"
        APP_DIR = "/home/ubuntu/"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/awsconsultant9/apis.git'
            }
        }

        stage('Deploy to EC2-B') {
            steps {
                sshagent(['ec2-bapp-key']) {
                    sh '''
                    echo "[1] Ensure target directory exists on EC2-B..."
                    ssh -o StrictHostKeyChecking=no $TARGET_HOST "mkdir -p $APP_DIR"

                    echo "[2] Copy project files from EC2-A to EC2-B..."
                    rsync -avz -e "ssh -o StrictHostKeyChecking=no" --exclude='.venv' ./ $TARGET_HOST:$APP_DIR
                    '''
                }
            }
        }

stage('Install Dependencies & Start FastAPI Server') {
    steps {
        sshagent(['ec2-bapp-key']) {
            sh """
                ssh -o StrictHostKeyChecking=no \$TARGET_HOST '
                    cd \$APP_DIR/apis &&
                     export PATH="\$HOME/.local/bin:\$PATH" &&

                    echo "[4] Install Python dependencies..." &&
                    poetry install --no-root --directory /home/ubuntu/apis &&

                    echo "[5] Kill previous Uvicorn process (if any)..." &&
                    pkill -f "uvicorn" || true &&

                    echo "[6] Start FastAPI server in background..." &&
                    /usr/bin/nohup /usr/bin/poetry --directory /home/ubuntu/apis run uvicorn apis.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
                '
            """
        }
    }
}

    }
}
