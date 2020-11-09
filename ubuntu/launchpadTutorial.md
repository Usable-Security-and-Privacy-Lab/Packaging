# Ubuntu Launchpad Tutorial

## System Configuration:

- First, create an Ubuntu one account: [Launchpad](https://login.launchpad.net/)
To login to launchapd visit: <https://login.launchpad.net/>

- Create OpenPGP key, press start, type Passwords and Encryption Keys, File > New PGP Key (for ubuntu 20.04, open Passwords and Encryption keys, then click gnupg and click on the + in the top left corner)

- You need to push the newly generated public key to the Ubuntu Keyserver
To push the key, go to Passwords and Encryption Keys, click on GnuPG keys, select your key, and click on details to find the key ID. In the terminal, enter this command: `gpg --send-keys --keyserver keyserver.ubuntu.com [Replace with your Key id]`
eg: `gpg --send-keys --keyserver keyserver.ubuntu.com 12345ABC`

- Get your key fingerprint by going to the key in Passwords and Encryption Keys, selecting the key, and click details, then Find the fingerprint in the middle left side of the window. (you might have to repeat the process if it prompts you for your password again.) You should get an email from Launchpad with instructions on how to open it. The easiest way to do it is save the encrypted contents in a text file, instructions.gpg, then open the text file in emacs, it will prompt you for your password and auto-decrypt the file for you to read it. Otherwise you can do: `gpg --output instructions --decrypt instructions.gpg` and `cat` the file or open it with an inferior text editor.
There will be a link to follow, that looks something like this: https://launchpad.net/token/************** if you get an error and you uploaded your key to the Ubuntu Key Server, you may have to wait up to 10 minutes or more for your key to get processed.


- Go to <https://launchpad.net/codeofconduct> and download the Code of Cunduct.

- After reading the code of conduct, in a terminal type: gpg `--clearsign UbuntuCodeofConduct-2.0.txt`
Click the sign it link on the codeofconduct page.
(Make sure you are in the Directory where the file was downloaded, you will be prompted for your key password inorder to sign the document.) Then open the signed file, which might look like "UbuntuCodeofConduct-2.0.txt.asc" and copy the contents into the box and click continue.
You might have to try submitting it multiple times, but it will eventually recognize your upload.

- Once the key is recognized, try uploading a test repo:
to get ubuntu ready for packaging, execute the following command in the terminal:
`sudo apt install gnupg pbuilder ubuntu-dev-tools apt-file -y`

- If you don't have an ssh key setup, create one in the terminal: `ssh-keygen -t rsa`

- Set up pbuilder for the distros we want to build for. execute: pbuilder-dist <release> create
`eg pbuilder-dist bionic create`

- While this is running, you can upload your ssh public key to launchpad by visiting <https://launchpad.net/~/+editsshkeys>
open a new terminal and cat .ssh/id_rsa.pub
you can copy the output by highlighting and then pressing CTL+SHIFT+C
paste the key into the box and press import public key

- Next configure shell for changelogs.
add these lines to your ~/.bashrc, then source ~/.bashrc.
`export DEBFULLNAME="your name here"`
`export DEBEMAIL="yourEmailHere@example.com"`
(For the lab computer, DEBFULLNAME="internet research lab", DEBEMAIL="internetresearchlab@internet.byu.edu")
configure bzr: `bzr whoami "Your name yourEmail@example.com"` //the quotes are important.
the pgp key name and email are: internet research lab <internetresearchlab@internet.byu.edu> <email>

- install dh-make bzr-builddeb `sudo apt-get install dh-make bzr-builddeb`

## Project packaging

- When working on a package, you will want to make sure you have the newest version of the project from github by pulling from master, then you will copy the source to a new directory. The directory should represent the file structure you want to have on the target machine. If you want to install the source files in the /usr/src/YourDirectory directory, you would need to create that structure in the new directory. It would look something like ssadaemon-0.56/usr/src/ssa-1.0  where ssa-1.0 would hold all of the source files required to build the ssa kernel module.
    - once you are in the new directory with the copied source files, run `dh_make --single --native --email internetresearchlab@internet.byu.edu` (Or on the Ubuntu lab machine, `makedh`)
    - Then `cd` into the debian folder, and remove any files that you don't need. For a simple package, just run `rm *.ex; rm *.EX; rm README.source`
    - You will need to edit the changelog to say `softwareName (version) release; urgency=level` then after the * enter the notes for the release.
    Eg: `ssadaemon (0.12) focal; urgency=low` The software would be the ssadaemon, the version would be version 0.12, the release would be focal, and the urgency would be low. the parenthesis are important for the version.
    - There are some fields that you will need to fill in for the copyright, ssadaemon-0.22/debian has an example of how to do the copyright file.
    - The control file:
        - `Source: ssadaemon` this is the name that is used when using sudo apt install(I think, I need to test this.)
        - `Section: utils` this is the classification of the project, this is a utility package.
        - `Priority: optional` since it is not a security patch per say, it would be considered optional.
        - `Maintainter: internet research lab <internetresearchlab@internet.byu.edu>` this is the lab information for our ubuntu account, and the lab would be the maintainer of the project.
        - `Build-Depends: debhelper, libavachi-client-dev,...valgrind` these are the dependencies for the project, you may need to specify the version of some software like debhelper in the compat file.
        - `Homepage: https://github.com/Usable-Security-and-Privacy-Lab/ssa-daemon` this is a URL to our online repo.
        - `Package: ssadaemon` 
        - `Architecture: any`
        - `Depends:  ${shlibs:Depends}, ${misc:Depends}` We left these as their default configuration.
        - `Description: ssa-daemon to be used with the SSA` This is a short description of the package.
        `For more info, see docs in github repository` this is where a longer description of the project can go, this line should be indented 1 tab more than the line above it.
        - You might be able to specify the dependencies like this `Build-Depends: debhelper-compat (= 12), vim (>= 7.1), xml-twig-tools (>= 3.3), imagemagick (>= 6.3)` but we couldn't get it working like that at the time.
    - There are various scripts you can write to create files/directories and do other tasks to prep the install/uninstall environment, we used install, preinst, prerm, postinst
    - The rules file is how the project is built on the Ubuntu servers. dh $@ is the default command, if you need to do something different, you can override that particular section.
    Here is an example:
    `#!/usr/bin/make -f`
    `VERSION=0.16`
    `%:`
        `dh $@` this line should be indented by one tab
    `override_auto_install:`
	`mkdir -p /usr/src/ssa-daemon` this line should be indented by one tab
	`dh_install` this line should be indented by one tab
    - After the debian files are changed and ready to go, you need to try building the package with `bzr builddeb -- -B` for a binary package or `bzr builddeb -S` for a source code only package.
    we used the binary package for the ssa-daemon. These commands need to be run in the debian parent directory.
    - If the package builds successfully, you can try testing the .deb package before pushing it to Launchpad by executing `sudo dpkg -i ~/ppasrc/ssadaemon_"$1"_amd64.deb` where "$1" is the version of the package you want to install.
    - To test the removal of the package, you can run the regular apt remove command to remove the .deb package from your system.
    - When you are ready to push to launchpad, you need to be in directory that has the version source.changes file. Then execute `dput ppa:byu-ilab/ssa-daemon ssadaemon_"$1"_source.changes`
    ### Aliases to help with building the packages.
    - On the lab machine, there are aliases and bash functions to help with packaging.
        - pushDaemon takes a version number and then calls dput with the correct name and repo already filled in.
        - buildPackage/buildBinary can be used to run the bzr builddeb commands.
        - makedh runs the dh_make command with the email and other arguments already filled in.
        - testInstall takes a verion number and will install the .deb file for you if you are in the directory where the .deb is located.
        - newdaemon takes a version number and creates a new package for you, it also sets up some of the debian folder for you as well.
    - Once the package has been pushed to launchpad, you will get an email informing you if it was accepted/rejected and once the build has been published, you can run:
    `sudo add-apt-repository ppa:byu-ilab/ssa-daemon; sudo apt-get update` to add the repo to apt and then run `sudo apt install ssadaemon` to install the latest version of the software.

## Multiple Distro support

- If you want to use the same source for multiple distros, you can follow the steps on [this](https://askubuntu.com/questions/30145/ppa-packaging-having-versions-of-packages-for-multiple-distros) askubuntu question.

## Other tutorials

This is the best tutorial I found, it was simple, clear and easy to follow.
<http://www.forshee.me/2012/03/16/introduction-to-creating-dkms-packages.html>

<https://packaging.ubuntu.com/html/debian-dir-overview.html> explains about packaging files.
This is how to have multiple dependencies:


This is probably the second best to follow: <https://www.ebower.com/docs/ubuntu-ppa/>