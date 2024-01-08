if screen -list | grep -q '\<barbara\>'; then
    echo "Barbara is running"
else
    echo "Barbara is offline"
fi