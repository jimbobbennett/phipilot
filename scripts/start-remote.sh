cd /home/jim/copilot-api
poetry run start > /dev/null &
ngrok http http://localhost:8000 > /dev/null &