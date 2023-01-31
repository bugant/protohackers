# PROTOHACKERS

Having fun solving some [server programming challenges](https://protohackers.com/).


## Deploy

Applications are deployed on [fly.io](https://fly.io) using the `fly` CLI,
please refer to their [documentations](https://fly.io/docs/) for all the details.

### Quick start

```bash
fly auth login
cd $APP_DIR
fly launch
# configure the generated fly.toml
# if you don't have an IP address allocated
fly ips allocate-v4
fly deploy
```
