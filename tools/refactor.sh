# This script is a simple refactoring tool to rename the directory
# that contains the application source code. 
# The script is invoked passing two parameters: the current name of 
# the directory and the new name.
# E.g., ./tools/refactor.sh code sources

# After the previous execution the "code" directory needs to be renamed
# as "sources". Obviously, several "from" statements in the python source
# files need to be adjusted as well to reflect the change.
# To test if everything is ok, execute the previous command and then try
# to run the game. If it works without raining exceptions, it is ok.

OLDNAME=$1
NEWNAME=$2

if [ $# -ne 2 ]
then
	echo "Use refactor.sh orig_name new_name"
	exit
fi

echo "Renaming $1 to $2"
echo $(dirname $1) #directory path
echo $(basename $1) #name of the directory

grep --color -rE "from $(basename $1)" $(dirname $1)/* | sed "s/from $(basename $1)/from $2/g"

# Put here your code

