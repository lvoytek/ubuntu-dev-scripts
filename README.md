# ubuntu-dev-scripts
Random (relatively undocumented) scripts I made to help work on packages in Ubuntu

## Script Overview

#### [lxcquick](./lxcquick)
Create an LXD container of a given Ubuntu version, update it, and enter a shell for it. Once you exit the shell the container will be automatically deleted.

#### [autopkgquick](./autopkgquick)
Run autopkgtest locally for an Ubuntu package on a given Ubuntu version, optionally providing a PPA to test against. Run buildubuntutestimg to create the image for the Ubuntu version you need first.

#### [buildubuntutestimg](./buildubuntutestimg)
Create a virtual machine image of a given Ubuntu version to use for running autopkgtests locally.
