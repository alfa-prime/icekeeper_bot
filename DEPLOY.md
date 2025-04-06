# IceKeeper: Чит-лист по CI/CD и деплою

---

## ✅ 1. Подготовка сервера

- Установи Python, `git`, `python3-venv`, `pip`:
  ```bash
  apt update && apt install -y git python3-venv python3-pip
  ```

- Создай директорию:
  ```bash
  mkdir -p /opt/icekeeper_bot
  ```

---

## ✅ 2. SSH-доступ с GitHub

- Создай ключ:
  ```bash
  ssh-keygen -t ed25519 -f .deploy_keys/icekeeper_deploy_key
  ```

- Копируй `.pub` на сервер:
  ```bash
  ssh root@<ip> "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys" < .deploy_keys/icekeeper_deploy_key.pub
  ```

- Добавь в `.gitignore`:
  ```
  .deploy_keys/
  .env
  ```

---

## ✅ 3. GitHub Secrets

Добавь в репозиторий:

| Название     | Значение                        |
|--------------|----------------------------------|
| `SSH_KEY`    | приватный ключ (OpenSSH) |
| `HOST`       | IP или домен сервера            |
| `USER`       | `root`                          |

---

## ✅ 4. `.env` и venv

- Скопируй `.env` на сервер:
  ```bash
  scp .env root@<ip>:/opt/icekeeper_bot/.env
  ```

- На сервере:
  ```bash
  cd /opt/icekeeper_bot
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

---

## ✅ 5. `icekeeper.service`

```ini
# /etc/systemd/system/icekeeper.service

[Unit]
Description=IceKeeper Telegram Bot
After=network.target

[Service]
WorkingDirectory=/opt/icekeeper_bot
ExecStart=/opt/icekeeper_bot/.venv/bin/python /opt/icekeeper_bot/main.py
Restart=always
User=root
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable icekeeper.service
sudo systemctl start icekeeper.service
```

---

## ✅ 6. GitHub Actions `.github/workflows/deploy.yml`

```yaml
name: Deploy IceKeeper to VPS

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v3
        # Скачивает код репозитория

      - name: Set up SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H ${{ secrets.HOST }} >> ~/.ssh/known_hosts
        # Добавляет SSH-ключ для доступа к серверу

      - name: Deploy
        run: |
          ssh ${{ secrets.USER }}@${{ secrets.HOST }} << 'EOF'
            cd /opt/icekeeper_bot                   # Входим в директорию проекта
            git pull origin main                    # Обновляем код с GitHub
            source .venv/bin/activate               # Активируем venv
            pip install -r requirements.txt         # Устанавливаем/обновляем зависимости
            systemctl restart icekeeper.service && echo "✅ IceKeeper перезапущен!"  # Рестарт бота
          EOF
```

---

## ✅ 7. Проверка

```bash
# Смотри логи:
journalctl -u icekeeper.service -n 50 --no-pager

# Ручной перезапуск:
sudo systemctl restart icekeeper.service
```

---


