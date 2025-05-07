# h5cpp Conan Recipe

This repository contains a [Conan](https://conan.io/) recipe for packaging [h5cpp](https://github.com/ess-dmsc/h5cpp), a modern C++ wrapper for the HDF5 C library.


## Creating a New Conan Package Release

When a new `h5cpp` release is published on [GitHub Releases](https://github.com/ess-dmsc/h5cpp/releases):

### 1. Update `conandata.yml`

Update the version entry with the new URL and its SHA256 checksum.

To calculate the SHA256:

```bash
curl -L https://github.com/ess-dmsc/h5cpp/archive/refs/tags/<release_number>.tar.gz | sha256sum
```

### 2. Update the Version in `conanfile.py`

Modify the `version = "<new_version>"` field accordingly.

### 3. Create a Merge Request

Submit your changes via a merge request. This will trigger a CI pipeline to test the package creation.
**Note:** The package won't be uploaded to the remote yet.

Once the MR is merged, a second pipeline will:
- Create the package
- Upload it to the ECDC Conan remote
- Done!

---

## Testing Package Creation Locally

If you'd like to verify the recipe locally:

```bash
conan config install https://github.com/ess-dmsc/conan-configuration.git
git clone git@gitlab.esss.lu.se:ecdc/ess-dmsc/conan-h5cpp.git
cd conan-h5cpp
```

Then run:

```bash
conan create . ess-dmsc/testing -pr=linux_x86_64_gcc11 --build=missing
```

---

## Verifying the Package

To inspect the generated package:

```bash
conan search h5cpp
conan info h5cpp/0.7.1@ess-dmsc/testing -pr=linux_x86_64_gcc11
```

---

## Using the Docker Build Environment

Use the pre-built Docker image for a clean build environment:

```bash
docker run --rm -it \
  -v "$(pwd)":/project \
  -w /project \
  registry.esss.lu.se/ecdc/ess-dmsc/docker-almalinux9-conan:1.2.0 \
  bash
```

Inside the container, use Conan as usual:

```bash
conan create . ess-dmsc/testing -pr=linux_x86_64_gcc11 --build=missing
```
