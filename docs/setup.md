
## 環境構築

環境をセットアップするには、以下の手順に従ってください。

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. 依存関係のインストール

```bash
uv sync
uv pip install -e .
```

### （任意）Docker を使用する場合

Docker を使って環境を構築することもできます。

1. Docker イメージをビルドし、コンテナを起動します。

   ```bash
   source scripts/env.sh
   docker compose up -d --build
   docker compose exec dev bash
   ```

   * `scripts/env.sh`：基本的な環境変数（UID/GID、.env）を設定します。

> [!NOTE]
> **参考**：Git 操作のために SSH アクセスを有効にした開発者モード
>
> ```bash
> source scripts/activate.sh
> docker compose -f compose.yaml -f compose.ssh.yaml up -d
> docker compose -f compose.yaml -f compose.ssh.yaml exec dev bash
> ```
>
> コンテナ内で GitHub への SSH 接続を確認します。
>
> ```bash
> ssh -T git@github.com
> ```
>
> * `scripts/activate.sh`：ssh-agent を起動し、Git アクセス用の SSH 鍵を追加します。

2. Docker コンテナ内で依存関係をインストールします。

   ```bash
   uv sync
   uv pip install -e .
   ```

## 使い方

* シンプルな VAE の学習を実行する場合：

```bash
python scripts/train.py --config configs/config.yaml
```
