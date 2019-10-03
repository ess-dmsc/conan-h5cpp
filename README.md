# conan-h5cpp

Conan package for h5cpp (https://github.com/ess-dmsc/h5cpp).

## Updating the conan package

For creating a new *h5cpp* package, choose the instructions based on if you have created a new release (stable) or if you want to create a test (develpoment) version.

### Create release (stable) package

1. Set the variable `package_type` on line 8 of *conanfile.py* to "release".

1. Edit line 10 of the *conanfile.py*-file to set the version (commit tag and release version) of the release that you want to create package for.

2. Download the *\*tar.gz* from the h5cpp release page and generate the SHA-256 checksum for the file: `shasum -a 256 v0.x.y.tar.gz`
   *NOTE:* Make sure that it is the *\*tar.gz* version of the file that you create the checksum for.

3. Replace the `archive_sha256` string on line 11 of *conanfile.py* with the new checksum.


3. When in the directory of the local copy of *conan-h5cpp*, execute this command:

	```
	conan create . h5cpp/0.x.y@ess-dmsc/stable
	```
	Where **0.x.y** is the same version string as set on line 10 in the *conanfile.py*-file.

4. Upload the new package to the relevant conan package repository by executing:

	```
	conan upload h5cpp/0.x.y@ess-dmsc/stable --remote alias_of_repository
	```

	Where **0.x.y** is the version of the conan package as mentioned above and **alias\_of\_repository** is exactly what it says. You can list all the repositories that your local conan installation is aware of by running: `conan remote list`.

### Create test package

1. Set the variable `package_type` on line 8 of *conanfile.py* to "test".

2. Edit line 26 of the *conanfile.py*-file to the commit hash (first 7 hex letters) of the commit that you want to package.

3. When in the directory of the local copy of *conan-h5cpp*, execute this command:

	```
	conan create . h5cpp/xxxxxxx@ess-dmsc/test
	```
	Where **xxxxxxx** is the same commit has as set on line 10 in the *conanfile.py*-file.

4. Upload the new package to the relevant conan package repository by executing:

	```
	conan upload h5cpp/xxxxxxx@ess-dmsc/test --remote alias_of_repository
	```

	Where **xxxxxxx** is once again the relevant commit hash. **alias\_of\_repository** is exactly what it says. You can list all the repositories that your local conan installation is aware of by running: `conan remote list`.
  