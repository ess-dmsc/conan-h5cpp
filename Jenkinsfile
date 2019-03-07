@Library('ecdc-pipeline')
import ecdcpipeline.ContainerBuildNode
import ecdcpipeline.ConanPackageBuilder

project = "conan-h5cpp"

conan_remote = "ess-dmsc-local"
conan_user = "ess-dmsc"
conan_pkg_channel = "testing"

container_build_nodes = [
  'centos': ContainerBuildNode.getDefaultContainerBuildNode('centos7'),
  'debian': ContainerBuildNode.getDefaultContainerBuildNode('debian9'),
  'ubuntu': ContainerBuildNode.getDefaultContainerBuildNode('ubuntu1804')
]

package_builder = new ConanPackageBuilder(this, container_build_nodes, conan_pkg_channel)
package_builder.defineRemoteUploadNode('centos')

builders = package_builder.createPackageBuilders { container ->
  package_builder.addConfiguration(container, [
    'settings': [
      'h5cpp:build_type': 'Release'
    ]
  ])

  package_builder.addConfiguration(container, [
    'settings': [
      'h5cpp:build_type': 'Debug'
    ]
  ])

  // Build parallel libraries only on CentOS.
  if (container.key == 'centos') {
    package_builder.addConfiguration(container, [
      'settings': [
        'h5cpp:build_type': 'Release'
      ],
      'options': [
        'h5cpp:parallel': "True"
      ],
      'env': [
        'CC': '/usr/lib64/mpich-3.2/bin/mpicc',
        'CXX': '/usr/lib64/mpich-3.2/bin/mpic++'
      ]
    ])
  }
}

def get_macos_pipeline() {
  return {
    node('macos') {
      cleanWs()
      dir("${project}") {
        stage("macOS: Checkout") {
          checkout scm
        }  // stage

        stage("macOS: Conan setup") {
          withCredentials([
            string(
              credentialsId: 'local-conan-server-password',
              variable: 'CONAN_PASSWORD'
            )
          ]) {
            sh "conan user \
              --password '${CONAN_PASSWORD}' \
              --remote ${conan_remote} \
              ${conan_user} \
              > /dev/null"
          }  // withCredentials
        }  // stage

        stage("macOS: Package") {
          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings h5cpp:build_type=Release \
            --build=outdated"

          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings h5cpp:build_type=Debug \
            --build=outdated"

          sh "conan info ."

          // pkg_name_and_version = sh(
          //   script: "./get_conan_pkg_name_and_version.sh",
          //   returnStdout: true
          // ).trim()
        }  // stage

        // stage("macOS: Upload") {
        //   sh "conan upload \
        //     --all \
        //     --remote ${conan_remote} \
        //     ${pkg_name_and_version}@${conan_user}/${conan_pkg_channel}"
        // }  // stage
      }  // dir
    }  // node
  }  // return
}  // def

def get_win10_pipeline() {
  return {
    node('windows10') {
      // Use custom location to avoid Win32 path length issues
      ws('c:\\jenkins\\') {
      cleanWs()
      dir("${project}") {
        stage("win10: Checkout") {
          checkout scm
        }  // stage

        // stage("win10: Conan setup") {
        //   withCredentials([
        //     string(
        //       credentialsId: 'local-conan-server-password',
        //       variable: 'CONAN_PASSWORD'
        //     )
        //   ]) {
        //     bat """C:\\Users\\dmgroup\\AppData\\Local\\Programs\\Python\\Python36\\Scripts\\conan.exe user \
        //       --password ${CONAN_PASSWORD} \
        //       --remote ${conan_remote} \
        //       ${conan_user}"""
        //   }  // withCredentials
        // }  // stage

        stage("win10: Package") {
          bat """C:\\Users\\dmgroup\\AppData\\Local\\Programs\\Python\\Python36\\Scripts\\conan.exe \
            create . ${conan_user}/${conan_pkg_channel} \
            --settings h5cpp:build_type=Release \
            --build=outdated"""
        }  // stage

        // stage("win10: Upload") {
        //   sh "upload_conan_package.sh conanfile.py \
        //     ${conan_remote} \
        //     ${conan_user} \
        //     ${conan_pkg_channel}"
        // }  // stage
      }  // dir
      }
    }  // node
  }  // return
} // def

node {
  checkout scm

  builders['macOS'] = get_macos_pipeline()
  builders['windows10'] = get_win10_pipeline()

  try {
    parallel builders
  } finally {
    cleanWs()
  }
}
