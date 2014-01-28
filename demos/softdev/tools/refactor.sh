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

OLDNAME=$(basename $1)
NEWNAME=$(basename $2)
DIRPATH=$(dirname $1)

if [ $# -ne 2 ]
then
	echo "Use: refactor.sh original_name new_name"
	exit
fi
if [ "$(dirname $2)" != "." ]
then
	echo "new_name cannot contains /"
	exit
fi

echo "Renaming $OLDNAME to $NEWNAME"

for file in $(grep -rl "from $OLDNAME" $DIRPATH/*)
do
	sed -i "s/from $OLDNAME/from $NEWNAME/g" $file
done
mv $1 $DIRPATH/$NEWNAME

