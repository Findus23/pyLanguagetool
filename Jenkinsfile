pipeline {
  agent {
    docker {
      image 'python'
      args '3.6-slim'
    }

  }
  stages {
    stage('install') {
      steps {
        sh 'pip install -e .[dev]'
        sh 'pip install -e .[optional]'
      }
    }
    stage('tests') {
      parallel {
        stage('pytest') {
          steps {
            sh 'python -m pytest'
          }
        }
        stage('setup test') {
          steps {
            sh 'python setup.py check -ms'
          }
        }
      }
    }
  }
  environment {
    API_URL = 'https://languagetool.org/api/v2/'
  }
}