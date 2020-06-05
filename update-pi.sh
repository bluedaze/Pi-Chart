echo "Updating pi-graph.com..."
sleep 1s
echo "Pulling from repository"
git pull https://github.com/bluedaze/Pi-Chart.git
sleep 4s
echo "Killing green unicorns. Die unicorn, die!"
pkill -f gunicorn
sleep 2s
echo "Spawning three new gunicorn babies"
gunicorn -w 3 pigraph:app &
sleep 2s
clear
sleep 1s
ps -ef | grep gunicorn
ps -ef | grep python
