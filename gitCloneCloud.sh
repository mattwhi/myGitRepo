#!/bin/bash
LOCALREPO="$HOME/repositories3"

#Repos

REPOS="smartdrive_config_prod
smartdrive_config_nonprod
smartdrive_deployment
common_management_nonprod
common_management_prod
cloudservices-scripts
netcool_api
O2CloudServices
test_getupdates_deployment
prod_getupdates_deployment"

#Test to see if the local repositories directory already exits

if [ -d $LOCALREPO ]; then
	echo -e "Directory $LOCALREPO already exists, skipping the creation of new $LOCALREPO...\n"
else
	mkdir $LOCALREPO
fi

#Enter current directory to clone Git Repos
cd $LOCALREPO

# clone cloud services repositories
for repo in $REPOS 
	do 
	if [ -d $LOCALREPO/$repo ]; then
		echo -e "Git repo $repo already exists, updating... \n"
		cd $LOCALREPO/$repo
		git pull
		cd $HOME
	else
		echo -e "Cloning $repo ...."
		git clone git@github.com:O2IP/$repo.git
	fi
done

echo -e "****** All repos are now cloned & updated *******"