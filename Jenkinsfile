pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    // Cek repo GitHub tiap 2 menit (pakai webhook jika Jenkins bisa diakses publik)
    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout (SCM)') {
            steps {
                // Mengambil kode dari repo yang dikonfigurasi di job Jenkins
                checkout scm
                sh 'git log -1 --oneline'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Cek Sintaks') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m py_compile app.py models.py seed.py
                '''
            }
        }

        stage('Seed Database (Uji)') {
            steps {
                sh '''
                    . venv/bin/activate
                    python seed.py
                '''
            }
        }

        // Aktifkan stage ini setelah ada folder tests/ (pytest)
        // stage('Test') {
        //     steps {
        //         sh '''
        //             . venv/bin/activate
        //             pip install pytest
        //             pytest -v
        //         '''
        //     }
        // }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                echo 'Isi langkah deploy di sini (mis. ssh ke server / trigger Render/Heroku).'
            }
        }
    }

    post {
        success { echo 'Build berhasil.' }
        failure { echo 'Build gagal, cek Console Output.' }
        always  { cleanWs() }
    }
}
