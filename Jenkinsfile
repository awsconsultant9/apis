pipeline {
    agent any

    environment {
        TARGET_HOST = "ubuntu@13.53.182.90"
        APP_DIR = "/home/ubuntu/fastapi-app"
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
                    ssh -o StrictHostKeyChecking=no $TARGET_HOST << 'EOF'
                        cd $APP_DIR

                        echo "[3] Install Poetry if not present..."
                        if ! command -v poetry &> /dev/null; then
                            curl -sSL https://install.python-poetry.org | python3 -
                            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
                            export PATH="$HOME/.local/bin:$PATH"
                        else
                            export PATH="$HOME/.local/bin:$PATH"
                        fi

                        echo "[4] Install Python dependencies..."
                        poetry install --no-root --directory /home/ubuntu/fastapi-app/apis

                        echo "[5] Kill previous Uvicorn process (if any)..."
                        pkill -f "uvicorn" || true

                        echo "[6] Start FastAPI server in background..."
                        nohup poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
                    EOF
                    """
                }
            }
        }
    }
}
