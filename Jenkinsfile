pipeline {
    agent any

    stages {
        stage ('Pre-Build') {
            steps {
				        sh 'ssh root@cerebus "ansible-libvirt-create.yml -e baseImageFilename=Fedora-Cloud-Base-34-1.2.x86_64.qcow2 -e vmTitle=olivetin-int -e ramMb=4096 -e diskSize=8 -e count=1 -e vmCustomize=virt-customize= "'
                sh 'ssh root@olivetin-int "uname -a" '
            }
        }
}
