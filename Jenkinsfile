pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout (SCM)') {
            steps {
                checkout scm
                bat 'git log -1 --oneline'
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Cek Sintaks') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    python -m py_compile app.py models.py seed.py
                '''
            }
        }

        stage('Seed Database (Uji)') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    python seed.py
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Isi langkah deploy di sini.'
            }
        }
    }

    post {
        success { echo 'Build berhasil.' }
        failure { echo 'Build gagal, cek Console Output.' }
    }
}
