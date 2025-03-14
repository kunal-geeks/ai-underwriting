pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/kunal-geeks/ai-underwriting.git'
            }
        }
        stage('Build and Deploy') {
            steps {
                sh 'cd docker && docker-compose up --build -d'
            }
        }
    }
}
