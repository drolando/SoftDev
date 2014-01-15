i=0
cat shrine.xml | while read line
do
    res=$(echo $line | grep 'o="trees:05"')
    if [ "$res" != "" ]
    then
        echo $line | sed "s/o=\"trees:05\"/o=\"trees:05\" id=\"tree:$i\"/g"
        i=$(($i+1))
    else
        echo $line
    fi

done > shrine2.xml

