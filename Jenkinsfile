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
          environment {
            API_URL = 'https://languagetool.lw1.at/v2/'
          }
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
  }
  post {
    always {
      junit 'junit.xml'
    }
  } 
}
