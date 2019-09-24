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
            archiveArtifacts 'appmap-master'
          }
        }
      }
    }
  }
}