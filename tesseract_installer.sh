#!/bin/bash

function showHelp {
	echo "Usage: tesseract_installer.sh {3.05, 4.00}"
	echo ""
	echo "Bash script that install Tesseract in the system."
	echo "You can choose between the 3.05 or 4.00 version."
	echo "If this script is executed in Ubuntu 18.04 or CentOS 7 it will install some dependecies\
 automatically."
	echo ""
	echo "Options:"
	echo "    -h, --help         show this help message and exit"
	echo "    --only-tesseract   install Tesseract only without dependecies"
}

function installTesseractAndDependecies {

	# Install dependecies in Ubuntu 18.04 LTS
	if [ "$OS_NAME" == "Ubuntu" ] && [ "$OS_VERSION" == "18.04" ]; then
		apt-get update
		apt-get install wget unzip autoconf automake libtool autoconf-archive pkg-config\
 libpng-dev libjpeg8-dev libtiff5-dev zlib1g-dev

	# Install dependecies in CentOS 7
elif [ "$OS_NAME" = "CentOS Linux" ] && [ "$OS_VERSION" = "7" ]; then
		sudo yum update
		sudo yum install wget unzip libstdc++ autoconf automake libtool autoconf-archive\
 pkg-config gcc gcc-c++ make libjpeg-devel libpng-devel libtiff-devel zlib-devel libXrender-devel\
 libXext-devel libSM-devel
	else
		echo "Not able to install the required packages with apt or yum."
		echo "Please check how to install GNU autotools, autoconf-archive, libpng-dev,\
 libtiff-dev, libjpeg-dev, zlib-dev and pkg-config in your system."
 		echo ""
 		echo "Do you want to proceed with the installation of Tesseract?"
		echo "Proceeding without these dependencies can cause problems."
		echo "[yes/no]"
		read ans
		if ! [[ $ans == y* ]]; then
			echo "Aborted."
			exit
		fi
	fi

	# Remove any previous Leptonica installation
	rm -rf /usr/local/include/leptonica
	rm -rf /usr/include/leptonica

	# Compile Leptonica from source
	LEPTONICA_ARC="v1.74.3.zip"
	wget https://github.com/DanBloomberg/leptonica/archive/$LEPTONICA_ARC
	unzip $LEPTONICA_ARC
	LEPTONICA_DIR="leptonica-1.74.3"
	cd $LEPTONICA_DIR
	./autobuild
	./configure
	make
	make install
	ldconfig
	cd ..
	sudo rm -rf $LEPTONICA_ARC $LEPTONICA_DIR

	installTesseract $1
}


function installTesseract {
	# Remove any previous Tesseract installation
	if [ "$OS_NAME"=="Ubuntu" ] || [ "$OS_NAME"=="Debian" ]; then
		apt purge tesseract-ocr*
		apt autoremove --purge
	fi
	rm -rf /usr/local/share/tessdata
	rm -rf /usr/share/tesseract-ocr/
	rm -rf /usr/local/lib/libtesseract*
	rm -rf /usr/local/lib/pkgconfig/tesseract.pc
	rm -rf /usr/local/include/tesseract
	rm -rf /usr/local/bin/tesseract

	# Compile Tesseract from source
	if [ "$1" == "3.05" ]; then
		TESSERACT_ARC="3.05.02.zip"
		TESSERACT_DIR="tesseract-3.05.02"
	else
		TESSERACT_ARC="4.0.0-beta.3.zip"
		TESSERACT_DIR="tesseract-4.0.0-beta.3"
	fi
	wget https://github.com/tesseract-ocr/tesseract/archive/$TESSERACT_ARC
	unzip $TESSERACT_ARC
	cd $TESSERACT_DIR
	./autogen.sh
	./configure
	LDFLAGS="-L/usr/local/lib"
	TSLAGS="-I/usr/local/include"
	make
	make install
	ldconfig
	cd ..
	rm -rf $TESSERACT_ARC $TESSERACT_DIR

	# Install languages packs
	# It installs:
	# - English
	# - Italian
	# - OSD (Orientation Script Detection)
	if [ "$1" == "3.05" ]; then
		LANG_VER="3.04.00"
	else
		LANG_VER="4.00"
	fi
	wget https://raw.github.com/tesseract-ocr/tessdata/$LANG_VER/eng.traineddata
	wget https://raw.github.com/tesseract-ocr/tessdata/$LANG_VER/ita.traineddata
	wget https://raw.github.com/tesseract-ocr/tessdata/$LANG_VER/osd.traineddata
	mv *.traineddata /usr/local/share/tessdata/
	echo "po'" > /usr/local/share/tessdata/ita.special-words
}


if [ -f /etc/os-release ]; then
	. /etc/os-release
	OS_NAME=$NAME
	OS_VERSION=$VERSION_ID
else
	OS_NAME=""
	OS_VERSION=""
fi

if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
	showHelp
	exit
fi

if [ "$EUID" -ne 0 ]; then
	echo "Please run as root"
	exit
fi

if [ "$(command -v tesseract)" ]; then
	echo "Tesseract $(tesseract --version | grep tesseract | cut -b11-17) was found in the\
system."
	echo "Do you want to replace it?"
	echo "[yes/no]"
	read ans
	if ! [[ $ans == y* ]]; then
		echo "Aborted."
		exit
	fi
fi

if [ "$1" == "3.05" ] || [ "$1" == "4.00" ]; then
	installTesseractAndDependecies $1
elif [ "$1" == "--tesseract-only" ] && ([ "$2" == "3.05" ] || [ "$2" == "4.00" ]); then
	installTesseract $2
else
	echo "Please specify a version: 3.05 or 4.00"
fi
