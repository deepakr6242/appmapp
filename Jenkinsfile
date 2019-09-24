pipeline {
  agent any
  stages {
    stage('Buzz') {
      parallel {
        stage('Buzz') {
          steps {
            echo 'Stage A'
          }
        }
        stage('parallel check') {
          steps {
            echo 'I am here'
          }
        }
        stage('dir') {
          steps {
            echo "${ env.GIT_COMMIT.substring(0,6) }"
          }
        }
      }
    }
  }
}