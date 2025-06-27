# ubuntu-dev-scripts
Random (relatively undocumented) scripts I made to help work on packages in Ubuntu

## Script Overview

#### [lxcquick](./lxcquick)
Create an LXD container of a given Ubuntu version, update it, and enter a shell for it. Once you exit the shell the container will be automatically deleted.

#### [autopkgquick](./autopkgquick)
Run autopkgtest locally for an Ubuntu package on a given Ubuntu version, optionally providing a PPA to test against. Run buildubuntutestimg to create the image for the Ubuntu version you need first.

#### [buildubuntutestimg](./buildubuntutestimg)
Create a virtual machine image of a given Ubuntu version to use for running autopkgtests locally.

#### [getsourcereversedepends](./getsourcereversedepends)
Get the source package names for all reverse-dependencies of a binary package in an Ubuntu release.

#### [rebuildallpackagesinfolder](./rebuildallpackagesinfolder)
Prepare a no-change rebuild release with a ~ppa1 extension for every git-ubuntu sub-directory in the current directory. This is useful for testing reverse-depends of a package alongside getsourcereversedepends.

#### [updatepackagetoversion](./updatepackagetoversion)
Forcibly update the upstream contents of a package in the current directory to that of the provided upstream version and commit the contents to git.
