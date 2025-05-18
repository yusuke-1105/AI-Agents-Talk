# 🔎 AI Agents Talk

このアプリケーションは、あらかじめ定義した人格を持つ2つの生成AIが対話形式で質問に答えるStreamlitアプリです。  
ユーザーが入力した質問に対して、2人のエージェントが議論を行い、最終的な結論を導き出すアプリケーションです。対話はClaudeのAIモデルを活用して生成されます。

## 🛠️ 必要条件

- Docker Desktop (Docker と Docker Compose) がインストールされていること。  
[こちら](https://www.docker.com/products/docker-desktop/)からインストールしてください。
- Anthropic APIキーを取得していること。  
APIキーは[Anthropicの公式サイト](https://www.anthropic.com/api)の "Start building" から取得できます。

## 🐳 起動方法（Docker を使用）

### 📥 リポジトリをクローン
以下のコマンドを実行するか、GitHub Desktopを使用してリポジトリをクローンします。

```bash
git clone https://github.com/yusuke-1105/AI-Agents-Talk.git
cd AI-Agents-Talk
```

### 📝 環境変数ファイルを作成

`example.env`ファイルの名前を`.env`に変更し、以下のようにAPIキーを設定します。

```
ANTHROPIC_API_KEY=xxxxxxxxx
```

### 🚀 Dockerコンテナを起動

以下のコマンドを実行して、アプリケーションを起動します。

```bash
docker-compose up -d
```

このコマンドにより、アプリケーションがバックグラウンドで起動します。

### 🌐 アプリケーションにアクセス

ブラウザで以下のURLにアクセスします。

```
http://localhost:8501
```

これで、アプリケーションの利用が可能になります。

### 🛑 アプリケーションの停止方法

アプリケーションを停止するには、以下のコマンドを実行します。

```bash
docker-compose down
```

## 🐍 起動方法（Python環境で実行）

1. `example.env`をコピーし、`.env`にリネームしてAPIキーを設定します。

```bash
cp example.env .env
```

1. 仮想環境を作成して有効化します。

```bash
python3 -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

1. 必要なパッケージをインストールします。

```bash
pip install streamlit anthropic
```

1. アプリケーションを起動します。

```bash
streamlit run app.py
```

1. ブラウザで`http://localhost:8501`にアクセスします。

## 💡 使い方

1. テキストエリアに質問を入力します
2. 「会話を開始」ボタンをクリックします
3. Agent-1とAgent-2の対話が自動的に始まります。会話回数が最大に達すると、少ししてから最終的な結論が表示されます

## 🐞 トラブルシューティング

### ❗ アプリケーションが起動しない場合

1. Dockerが正常に動作しているか確認してください
2. `.env`ファイルが正しく作成されているか確認してください
3. APIキーが有効であることを確認してください

### ❓ その他の問題

- ログを確認するには、以下のコマンドを実行してください：

```bash
docker-compose logs
```

## 🔄 アプリケーションの更新

アプリケーションに変更を加えた場合は、以下のコマンドで再ビルドと再起動を行ってください。

```bash
docker-compose down
docker-compose up -d --build
```

これにより、最新の変更が適用されたアプリケーションが起動します。

## 📄 その他

このアプリケーションのコードの大半はGitHub Copilotによって生成されています。このアプリケーションを使用したことにより損害や問題が発生した場合でも、開発者は一切の責任を負いませんのでご了承ください。