#!/bin/bash
# Author:      Matthew White <matthew.white@telefonica.com>
# Description: Creates a capture of an Azure Instance 
# Requires:    git, bash
# Compatibility: currently only compatible with Linux & Apple Mac
# Version: 0.1
# Usage ./createCapture

echo -n "Please enter your Azure Username [ENTER] "
	read USERNAME
		USERNAME=`echo ${USERNAME} | awk '{print $1}'`
echo -n "Please enter your Azure Password [ENTER] "
	read PASSWORD
		PASSWORD=`echo ${PASSWORD} | awk '{print $1}'`
echo ""
echo "********************************************************************"
echo "The following information will be available from your Azure Resource"
echo "********************************************************************"
echo ""
echo -n "Please enter your Resource Group [ENTER] "
	read MYRESOURCEGROUP
		MYRESOURCEGROUP=`echo ${MYRESOURCEGROUP} | awk '{print $1}'`
echo -n "Please enter your Virtual Machine [ENTER] "
	read MYVM
		MYVM=`echo ${MYVM} | awk '{print $1}'`
echo -n "Please enter a new image name [ENTER] "
	read IMAGE
		IMAGE=`echo ${MYVM} | awk '{print $1}'`
echo

az login -u ${USERNAME} -p ${PASSWORD}

az vm deallocate --resource-group ${MYRESOURCEGROUP} --name ${MYVM}

az vm generalize --resource-group ${MYRESOURCEGROUP} --name ${MYVM}

az image create --resource-group ${MYRESOURCEGROUP} --name ${IMAGE} --source ${MYVM}