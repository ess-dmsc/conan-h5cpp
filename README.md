# conan-h5cpp

[![Build Status](https://jenkins.esss.dk/dm/job/ess-dmsc/job/conan-h5cpp/job/master/badge/icon)](https://jenkins.esss.dk/dm/job/ess-dmsc/job/conan-h5cpp/job/master/)

Conan package for [h5cpp](https://github.com/ess-dmsc/h5cpp), a modern c++ wrapper for hdf5.

This repository tracks the recipe for generating the conan package. You should not have to run these steps yourself but instead simply fetch the package from the the conan remote server as described below.

## Using the package

See the DMSC [conan-configuration repository](https://github.com/ess-dmsc/conan-configuration) for how to configure your remote.

In `conanfile.txt`:

```
[requires]
h5cpp/0.4.1@ess-dmsc/stable
...
[options]
h5cpp:parallel=False
h5cpp:with_boost=False
```

Where:
* `parallel` indicates if you intend to use the library with MPI
* `with_boost` is needed if your compiler does not provide `std::filesystem`

In CMake:
```
find_package(h5cpp 0.4.1 REQUIRED)
...
target_link_libraries(my_target
  PUBLIC h5cpp::h5cpp
)
```

See [h5cpp](https://github.com/ess-dmsc/h5cpp) documentation for further details on how to use the library.

## Updating the recipe

If you are a contributor and wish to update this recipe to use the latest version of the target library.

There are 2 ways of doing this, depending on whether you want to create a package for a new (stable) release or if you want to create a test (development) version based on an arbitrary commit.

* make a branch
* change `channel` in [Jenkinsfile](Jenkinsfile) from "stable" to "testing"
* steps **only** for tagged release:
  * In [conanfile.py](conanfile.py), set `package_type` to "release"
  * In [conanfile.py](conanfile.py), set `version` to the release that you want to create a package for
  * Download the *\*tar.gz* from the [h5cpp release page](https://github.com/ess-dmsc/h5cpp/releases) and generate the SHA-256 checksum for the file: `sha256sum v0.x.y.tar.gz` or `shasum -a 256 v0.x.y.tar.gz`. Make sure that it is the *\*tar.gz* version of the file that you create the checksum for.
  * In [conanfile.py](conanfile.py), set `archive_sha256` to the new checksum.
* steps **only** for arbitrary commits:
    * In [conanfile.py](conanfile.py), set `package_type` to "test".
    * In [conanfile.py](conanfile.py), set `commit` to the commit hash (first 7 hex letters) of the commit that you want to package
* push and massage until the job succeeds on [Jenkins](https://jenkins.esss.dk/dm/job/ess-dmsc/job/conan-h5cpp/)
* ideally, test new version of package with actual projects that use it
* update the conan package name in code example, under the ["Using the package"](#using-the-package) section above
* if this a stable release, change `channel` back to "stable" in [Jenkinsfile](Jenkinsfile) 
* make a merge request
