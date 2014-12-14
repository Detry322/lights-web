node ./node/app.js &
node_pid=$!
sleep 1
python ./python/app.py &
python_pid=$!
echo "Press enter to quit..."
read
kill $node_pid
kill $python_pid
