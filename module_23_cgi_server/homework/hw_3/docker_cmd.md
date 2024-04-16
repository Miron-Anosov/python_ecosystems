# Run

Build and Start:
```bash 
cd ./. && docker build -t static . && docker run --name uwsgi_app -p 80:80 static
```
TEST:
```bash
curl -D - -s http://127.0.0.1/status/ 
```
Wait 5 sec.
```bash
curl -D - -s http://127.0.0.1/long_task/
```
Error logs nginx:
```bash
docker exec -it uwsgi_app bash -c "tail -f /var/log/nginx/error.log"
```
Container and image remove.
```bash
docker stop uwsgi_app && docker rm uwsgi_app && docker rmi static -f
```