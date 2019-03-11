docker rm --force $(docker ps -q -a)
docker build -t "investing-calculator" .
docker run -p 8000:8000 -ti investing-calculator