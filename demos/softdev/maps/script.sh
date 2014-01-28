i=0
cat shrine.xml | while read line
do
    res=$(echo $line | grep 'o="trees:05"')
    #res=$(echo $line | grep "<cell")
    if [ "$res" != "" ]
    then
        #echo $line | sed "s/o=\"trees:05\"/o=\"trees:05\" id=\"tree:$i\"/g"
        #i=$(($i+1))
        echo $line | sed 's/">/" static="0">/g'
        #echo $line | sed 's-></i>-/>-g'
        #cat shrine.xml | grep "o=\"trees:05\"" | sed -r 's/o="[^"]*" //g' | sed 's/z="[^"]*" //g' | sed 's/ static="0"//g' | sed 's/ r="[^"]*"//g'| sed 's/<i/<cell narrow="1"/g'
    else
        echo $line
    fi

done > shrine2.xml

