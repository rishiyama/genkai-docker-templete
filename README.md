# genkai-docker-templete

## 🐳 Docker Hub へのイメージ push 手順

目標：このリポジトリに含まれる `Dockerfile` から Docker イメージをビルドし，Docker Hub に push する．

### 前提条件

* Docker がインストールされていること
* [Docker Hub](https://hub.docker.com/) アカウントを持っていること
* Docker Hub 上に push 先の[リポジトリが作成済み](./docs/dockerhub.md)であること
  （例：`<dockerhubユーザー名>/<リポジトリ名>`）
* ローカルのPC（開発環境）で操作を行います．


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
docker build -t ishiyamaryo/cuda11.8.0-ubuntu22.04-uv:v1.0 .
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
docker push ishiyamaryo/cuda11.8.0-ubuntu22.04-uv:v1.0
```


## 🌊 Genkaiで利用する
目標： 小規模な対話型ジョブで試す．(b-inter-mig)

### 1. docker imageをsifに焼く
```bash
[ku{number}@genkai0001 projects]$ singularity build ubuntu.sif docker://ishiyamaryo/cuda11.8.0-ubuntu22.04-uv:v1.0
INFO:    Starting build...
INFO:    Fetching OCI image...
21.8MiB / 21.8MiB [==============================================================================================================] 100 % 0.0 b/s 0s
53.6MiB / 53.6MiB 
...
165.8MiB / 165.8MiB [============================================================================================================] 100 % 0.0 b/s 0s
INFO:    Extracting OCI image...
INFO:    Inserting Singularity configuration...
INFO:    Creating SIF file...
INFO:    Build complete: ubuntu.sif
```
### 2. ログインノードでsifイメージからコマンドを叩く
```bash
[ku{number}@genkai0001 projects]$ singularity exec ubuntu.sif cat /etc/os-release
NAME="Ubuntu"
VERSION="20.04.6 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.6 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal
```

### 3. インタラクティブジョブ（計算ノード）でsifイメージを検証．
> [!IMPORTANT]
> pjsubコマンドに対するオプションの追加（`jobenv=singularity`）が必要です．

```bash
[ku{number}@genkai0001 projects]$  pjsub --interact -L rscgrp=b-inter-mig,gpu=1,elapse=01:00:00,jobenv=singularity

[INFO] PJM 0000 pjsub Job 4926150 submitted.
[INFO] PJM 0081 .connected.
[INFO] PJM 0082 pjsub Interactive job 4926150 started.

[ku{number}@b0030 projects]$ 
```

gpuに関するモジュールをロードし，sifイメージから`nvidia-smi`を叩きます．
```bash
[ku{number}@b0030 projects]$ module load cuda/11.8.0
[ku{number}@b0030 projects]$ module load singularity-ce/4.1.3
[ku{number}@b0030 projects]$ singularity exec --nv ubuntu.sif nvidia-smi
Tue Jan 13 23:08:24 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.105.08             Driver Version: 580.105.08     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA H100                    On  |   00000000:BC:00.0 Off |                   On |
| N/A   26C    P0            144W /  700W |                  N/A   |     N/A      Default |
|                                         |                        |              Enabled |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| MIG devices:                                                                            |
+------------------+----------------------------------+-----------+-----------------------+
| GPU  GI  CI  MIG |              Shared Memory-Usage |        Vol|        Shared         |
|      ID  ID  Dev |                Shared BAR1-Usage | SM     Unc| CE ENC  DEC  OFA  JPG |
|                  |                                  |        ECC|                       |
|==================+==================================+===========+=======================|
|  0    8   0   0  |              15MiB / 11008MiB    | 16      0 |  1   0    1    0    1 |
|                  |               0MiB /  4405MiB    |           |                       |
+------------------+----------------------------------+-----------+-----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

今回のイメージでは`uv`が利用できます．
```bash
[ku{number}@b0030 projects]$ singularity exec --nv ubuntu.sif uv -V
uv 0.9.24
```

以上より，`nvidi-smi`が通ることと，`uv`が操作できることが確認できました．
（インタラクティブジョブは，`exit`で終了できます．）


### 4. インタラクティブジョブ（計算ノード）で pythonプログラムを実行する
Genkaiのログインノードの所望のディレクトリで，リポジトリをclone.
```bash
[ku{number}@genkai0001 projects]$ git clone https://github.com/rishiyama/genkai-docker-templete.git
[ku{number}@genkai0001 projects]$ cd genkai-docker-templete
```

簡易的な実験．[scripts/genkai/inter.sh](./scripts/genkai/inter.sh)をインタラクティブノードで走らせます．
```bash
[ku{number}@genkai0001 projects]$  pjsub --interact -L rscgrp=b-inter-mig,gpu=1,elapse=01:00:00,jobenv=singularity
[ku{number}@b0030 projects]$ module load cuda/11.8.0
[ku{number}@b0030 projects]$ module load singularity-ce/4.1.3
[ku{number}@b0030 projects]$ singularity exec --nv ubuntu.sif bash scripts/genkai/inter.sh
```

### 5. バッチジョブ（計算ノード）に スクリプトを投げる
> [!CAUTION]
> このセクションは執筆中です．動くかもしれません．
簡易的な実験．[scripts/genkai/run.sh](./scripts/genkai/run.sh)をバッチジョブとして投入します．
```bash
[ku{number}@genkai0001 projects]$ pjsub scripts/genkai/run.sh
```