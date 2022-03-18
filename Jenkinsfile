@Library('ecdc-pipeline')
import ecdcpipeline.ContainerBuildNode
import ecdcpipeline.ConanPackageBuilder

project = "conan-h5cpp"

conan_user = "ess-dmsc"
conan_pkg_channel = "stable"

container_build_nodes = [
  'centos': ContainerBuildNode.getDefaultContainerBuildNode('centos7-gcc8'),
  'debian10': ContainerBuildNode.getDefaultContainerBuildNode('debian10'),
  'ubuntu2004': ContainerBuildNode.getDefaultContainerBuildNode('ubuntu2004')
]

package_builder = new ConanPackageBuilder(this, container_build_nodes, conan_pkg_channel)
package_builder.defineRemoteUploadNode('centos')

builders = package_builder.createPackageBuilders { container ->
  package_builder.addConfiguration(container, [
    'settings': [
      'h5cpp:build_type': 'Release'
    ],
    'options': [
      'h5cpp:with_boost': 'True'
    ]
  ])

  package_builder.addConfiguration(container, [
    'settings': [
      'h5cpp:build_type': 'Debug'
    ],
    'options': [
      'h5cpp:with_boost': 'True'
    ]
  ])
  
  package_builder.addConfiguration(container, [
    'settings': [
      'h5cpp:build_type': 'Release'
    ],
    'options': [
      'h5cpp:with_boost': 'False'
    ]
  ])

  package_builder.addConfiguration(container, [
    'settings': [
      'h5cpp:build_type': 'Debug'
    ],
    'options': [
      'h5cpp:with_boost': 'False'
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

        stage("macOS: Package") {
          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings h5cpp:build_type=Release \
            --options h5cpp:with_boost=False \
            --build=outdated"

          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings h5cpp:build_type=Debug \
            --options h5cpp:with_boost=False \
            --build=outdated"
            
          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings h5cpp:build_type=Release \
            --options h5cpp:with_boost=True \
            --build=outdated"

          sh "conan create . ${conan_user}/${conan_pkg_channel} \
            --settings h5cpp:build_type=Debug \
            --options h5cpp:with_boost=True \
            --build=outdated"

          sh "conan info ."
        }  // stage
      }  // dir
    }  // node
  }  // return
}  // def

node {
  checkout scm

  builders['macOS'] = get_macos_pipeline()

  try {
    parallel builders
  } finally {
    cleanWs()
  }
}
