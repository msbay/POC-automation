pipeline {
    agent any
    parameters {
        choice(name: 'Environment', choices: ['PROD', 'STG', 'DEV'], description: '')
        choice(name: 'Site', choices: ['fr', 'gb', 'de', 'us'], description: '')
        choice(name: 'Delivery', choices: ['Standard', 'Express', 'Click & Collect', 'Relay Point'], description: '')
        choice(name: 'Payment', choices: ['Visa', 'MasterCard', 'Klarna', 'Paypal'], description: '')

    }
    stages {
        stage("init") {
            steps {
            echo "Checkout SCM"
            }
        }
        stage("build") {
            steps {
            echo "build in progress"
            }
        }
        stage("test") {
                steps {
                    script{
                    sh 'cd /Users/moncef/Desktop/Lacoste/Automation/POC-Automation'
                    sh 'ls'
                    sh 'python3 POC-browser.py --env ${Environment} --site ${Site} --delivery ${Delivery} --payment ${Payment}'
                    }
                    }
            }

        stage("deploy") {
            steps {

                    echo "deployment"

            }
        }
    }
}