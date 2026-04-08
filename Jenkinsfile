pipeline {
  agent any

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Start App') {
      steps {
        sh '''
          pip install flask
          python app.py &
          sleep 8
          curl http://localhost:5000 || echo "App not responding"
        '''
      }
    }

    stage('Dastardly DAST Scan') {
      steps {
        sh '''
          docker run --rm \
            --network=host \
            -v ${WORKSPACE}:/dastardly \
            public.ecr.aws/portswigger/dastardly:latest \
            --target-url http://localhost:5000 \
            --output-file /dastardly/dastardly-report.xml || true
        '''
      }
      post {
        always {
          junit testResults: 'dastardly-report.xml',
                allowEmptyResults: true
        }
      }
    }

  }

  post {
    always {
      archiveArtifacts artifacts: '*.xml',
                       allowEmptyArchive: true
    }
  }
}