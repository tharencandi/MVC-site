for f in ./*; do
	b=`basename $f`
	mv $f $b.tpl
done

