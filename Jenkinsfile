pipeline {
    triggers {
      pollSCM('')
    } 

    agent any

    environment{
        GIT_REPO_NAME = 'argocd-devops'
        GIT_USER_EMAIL = credentials('git-user-email')
        GIT_USER_NAME = credentials('git-user-name')
        HOME = '/var/root/.jenkins'
    }

    stages {        
        stage('Run Automation Test Cases') {
            steps {
                script {
                    sh "pip3 install -r requirements.txt"
                    sh "python3 test.py"
                }
            }
            post {
              always {
                junit 'test-reports/*.xml'
              }
            }    
        }

        stage('Docker Build') {
            steps {
                script {
                  sh "/opt/homebrew/bin/docker build -t ${BUILD_NUMBER} ."
                  sh "/opt/homebrew/bin/docker tag ${BUILD_NUMBER}:latest chaudharishubham2911/argocd-demo:${BUILD_NUMBER}"
                }
            }
        }

        stage('Docker Image Scanning') {
            steps {
                script {
                  sh "curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/html.tpl > html.tpl"
                  sh "/usr/local/bin/trivy image --format template --template '@html.tpl' --output trivy_report.html --exit-code 0 --severity HIGH,CRITICAL chaudharishubham2911/argocd-demo:${BUILD_NUMBER}"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: "trivy_report.html", fingerprint: true      
                    publishHTML (target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'trivy_report.html',
                        reportName: 'Trivy Scan',
                        ])
                    }
             }            
        }

         stage('Docker Push') {
             steps {
                 script {
                         def registryCredentials = [
                         credentialsId: 'docker-creds'
                         ]
                         withCredentials([usernamePassword(credentialsId: 'docker-creds', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
                         sh "/opt/homebrew/bin/docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}"
                         sh "/opt/homebrew/bin/docker push chaudharishubham2911/argocd-demo:${BUILD_NUMBER}"
                     }
                 }
             }
         }

         stage('Update Helm Values File') {
             steps {
                 script {
                        withCredentials([usernamePassword(credentialsId: 'git-creds', passwordVariable: 'GitPassword', usernameVariable: 'GitUser')]) {
                            sh '''
                                git config --global user.email '${GIT_USER_EMAIL}'
                                git config --global user.name '${GIT_USER_NAME}'
                                git clone https://${GitPassword}@github.com/${GitUser}/${GIT_REPO_NAME}
                                cd ${WORKSPACE}/${GIT_REPO_NAME}
                                sed -i '' "s/tag: .*/tag: ${BUILD_NUMBER}/g" helm-chart/values.yaml
                                git add helm-chart/values.yaml
                                git commit -m "Update image version to ${BUILD_NUMBER}"
                                git push https://${GitPassword}@github.com/${GitUser}/${GIT_REPO_NAME} HEAD:main
                            '''
                        stash name: "${GIT_REPO_NAME}", includes: '**/*', path: "${GIT_REPO_NAME}"   
                        }
                     }
                 }
            }

         stage('Create ArgoCD Application') {        
             steps {
                 script {
                        unstash "${GIT_REPO_NAME}"
                        withKubeConfig([credentialsId: 'KUBECONFIG', serverUrl: 'https://127.0.0.1:6443']) {
                            sh '''  
                                cd ${WORKSPACE}/${GIT_REPO_NAME}
                                /usr/local/bin/kubectl apply -f application.yaml
                            '''
                        }
                     }
                 }
            }            
    }

        post {
          always {
            cleanWs()
          }
        }
}
