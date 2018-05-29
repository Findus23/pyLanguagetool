pipeline {
  agent {
    docker {
      image 'python'
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
            sh 'python -m pytest  --junitxml=junit.xml'
          }
        }
        stage('setup test') {
          steps {
            sh 'python setup.py check -ms'
          }
        }
      }
    }
    stage('') {
      steps {
        junit 'junit.xml'
      }
    }
  }
  environment {
    API_URL = 'https://languagetool.org/api/v2/'
  }
}