# genkai-docker-templete

## 🐳 Docker Hub へのイメージ push 手順

このリポジトリに含まれる `Dockerfile` から Docker イメージをビルドし，Docker Hub に push する手順を示します．

### 前提条件

* Docker がインストールされていること
* [Docker Hub](https://hub.docker.com/) アカウントを持っていること
* Docker Hub 上に push 先の[リポジトリが作成済み](./docs/dockerhub.md)であること
  （例：`<dockerhubユーザー名>/<リポジトリ名>`）


### 1. Docker Hub にログイン

```bash
docker login
```

Docker Hub のユーザー名とパスワード
（または Access Token）を入力します．


### 2. Docker イメージをビルド

プロジェクトのルートディレクトリ（`Dockerfile` がある場所）で実行します．

```bash
docker build -t <dockerhubユーザー名>/<リポジトリ名>:<タグ> .
```

例：

```bash
docker build -t rish/ext-genkai:latest .
```


### 3. （任意）ビルド結果の確認

```bash
docker images
```

指定したイメージ名とタグが表示されれば成功です．


### 4. Docker Hub に push

```bash
docker push <dockerhubユーザー名>/<リポジトリ名>:<タグ>
```

例：

```bash
docker push rish/ext-genkai:latest
```


## 🌊 Genkaiで利用する