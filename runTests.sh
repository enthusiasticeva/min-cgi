count=0

for folder in `ls -d ./mytests/* | sort -V`; do
  name=$(basename "$folder")

  echo Running test $name

  expected_file=./mytests/$name/$name.out
  in_file=./mytests/$name/$name.in

  bash $in_file | diff - $expected_file || echo "Test $name failed!\n"
  count=$((count+1))
done

echo "Finished running $count tests!"