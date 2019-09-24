pipeline {
  agent any
  stages {
    stage('Buzz') {
      steps {
        echo 'Stage A'
      }
    }
    stage('parallel') {
      steps {
        waitUntil() {
          input 'Click  OK to continue'
        }

      }
    }
  }
}