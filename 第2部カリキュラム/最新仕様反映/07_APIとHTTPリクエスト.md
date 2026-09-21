---
video: 7
title: "APIとHTTPリクエスト"
base: "第2部カリキュラム/既存動画/07_APIとHTTPリクエスト.md"
source: "Transcripts/drive-download-20260921T103213Z-1-001/⑦APIとHTTPリクエスト.txt"
duration: "00:20:42"
type: "座学（スライド）＋画面操作（Tavily ＋ n8n）"
verified_on: "2026-09-21"
n8n_version: "2.40"
---

# 07 — APIとHTTPリクエスト（最新仕様反映版）

`00:20:42 / 座学＋画面操作`

> **この版について**：既存動画の内容をベースに、2026-09-21 時点の n8n / Tavily の仕様に合わせて修正したもの。動画のままの記述は [既存動画版](../既存動画/07_APIとHTTPリクエスト.md) を参照。

## 現行仕様との差分サマリ

| # | 動画の記述 | 現行仕様（2026-09） | 対応 |
|---|---|---|---|
| 1 | Tavily には専用ノードがないので HTTP Request で繋ぐ | **Tavily の公式ノードが存在する**（n8n 検証済みコミュニティノード `@tavily/n8n-nodes-tavily`）。ただし **n8n Cloud の無料トライアルではコミュニティノードを使えない**うえ、インスタンスのオーナーによる有効化が必要 | **前提の補足が必須。演習としての HTTP Request は維持** |
| 2 | Tavily は毎月 1000 クレジットまで無料 | **変更なし**（クレジットカード不要） | そのまま |
| 3 | cURL の Header の `Your API Key` の部分を自分のキーに置き換える | 現行の Tavily の cURL は `Authorization: Bearer tvly-YOUR_API_KEY`。**`Bearer ` を残してキーだけ差し替える**という動画の説明は正しい | 文字列を正確化 |
| 4 | エンドポイント・ボディ（動画では「メッシは誰ですか」） | 現行も `POST https://api.tavily.com/search`、ボディ `{"query": "Who is Leo Messi?"}`。**変更なし** | そのまま |
| 5 | **API キーをヘッダーの値に直書きする** | **重大な問題。** 直書きしたキーは**ワークフローの JSON エクスポートに含まれる**。動画はこの直後に「JSON を ChatGPT にアップロードして」と案内しているため、**そのままだと API キーが外部サービスに渡る** | **手順の変更が必須** |
| 6 | Import cURL の手順 | **変更なし**（Parameters タブ → Import cURL → 貼り付け → Import） | そのまま |
| 7 | `{{ $json.chatInput }}` でチャット入力と連動 | **変更なし** | そのまま |
| 8 | Save を押す | **自動保存。Save ボタンなし** | 削除・置き換え |
| 9 | エラーが出たら ChatGPT / Google AI Studio に聞く | 現行では **n8n 内蔵の n8n Assistant / Ask n8n AI / AI Workflow Builder** が使える。外部にワークフローを出さずに解決できるケースが増えた | 選択肢の追加 |

## このパートの位置づけ

AIエージェントの能力を**文字通り無限に広げる鍵**として、API と HTTP Request ノードを扱う。n8n に専用ノードがないサービス（社内システム、最新のAIサービスなど）と連携する方法を、**Tavily**（Webリサーチツール）を練習題として習得する。

### 【重要な前提の追記】Tavily には今は公式ノードがある

動画は「Tavily には専用ノードがない」という前提で組まれているが、現在は **Tavily 公式が提供し、n8n が検証した公式ノード**が存在する。そのうえで、**この回の題材として Tavily を HTTP Request で繋ぐ意味は失われていない**。理由は3つ：

1. **無料トライアルのアカウントでは、そもそもコミュニティノードを使えない。** 本講座の受講者の大半はトライアルで受講するため、**実際に Tavily を使うには HTTP Request が唯一の手段**になる。
2. コミュニティノードは**インスタンスのオーナーが事前に有効化する必要がある**。会社の n8n では管理者の許可が要る。
3. そもそもこの回の目的は「**Tavily を使えるようになること**」ではなく「**専用ノードがないサービスと繋ぐ方法を身につけること**」。題材は何でもよく、Tavily はドキュメントが分かりやすいので教材として優秀。

→ 講義では、**「実は今は公式ノードもある。でも君たちのアカウントでは使えないし、本当に大事なのは専用ノードがないときの繋ぎ方だ」**と明示的に断ってから進めると、受講者が後で混乱しない。

## 説明している内容

### 専用ツールの限界

- これまで使ってきた Gmail・Wikipedia は、**n8n 側があらかじめ用意してくれているノード**。
- しかし世の中には専用ノードが用意されていないサービスが山ほどある。
  - 特定の業界の業務システム
  - 出たばかりの最新のAIサービス
  - 社内で使っている独自のツール
- **そうしたあらゆるサービスと接続するために使うのが HTTP Request ノード。**「専用ノードがないから n8n は使えない」と諦める必要は一切ない。

### API とは

- **Application Programming Interface** の略。難しく考えなくてよい。
- 言ってしまえば、**普通ならつながらないアプリケーション A と B を連携させるもの**。
- **レストランの例え**：
  - お客様（クライアント）／キッチン（サーバー）／**ウェイター＝API**
  - お客様が注文をウェイターに伝える → ウェイターがキッチンに伝えて料理を受け取る → ウェイターがお客様に料理を提供する
  - ＝ お客様のリクエストをキッチンに伝え、処理してレスポンスを返す流れ。
- つまり **プログラム同士が接続するためのルール**のこと。
- ④で使った **API キー**は、そのルールにおける**会員証・身分証明書**のようなもの。

### HTTP Request ノードとは

- 外部サービスの API と接続するための**自由度の高いノード**。
- 専用ノードには n8n と接続するための設定がすでに入っているが、**HTTP Request ノードではその設定を自分で書く必要がある**。
- 講師の比喩：**「白紙の注文伝票」**。
- 【追記】HTTP Request には **AI エージェントのツールとして使う版（HTTP Request Tool）**もあり、AI Agent ノードの Tool に直接ぶら下げられる。⑧ではこれを使う。

### GET と POST

| メソッド | 意味 |
|---|---|
| **GET** | データの取得 |
| **POST** | データの送信・作成 |

→ 今回の Tavily はデータを作って送信するので **POST**。

### cURL とは

- 小文字の c ＋ 大文字の URL で **cURL**。
- **API を接続するための設定内容が書かれたコードのようなもの。**
- これをコピーできれば、**専門知識がなくても、注文に必要な情報が一気に手に入る**。
- 開発者向けドキュメントは全部英語で難しそうに見えるが、**僕たちが探すべきものはたった一つ、cURL だけ**。

### cURL の構成（Tavily の現行サンプル）

現行の Tavily ドキュメントに載っている cURL は次のとおり（2026-09-21 時点）：

```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tvly-YOUR_API_KEY" \
  -d '{"query": "Who is Leo Messi?"}'
```

| 部分 | 意味 |
|---|---|
| `-X POST` | リクエストの種類。何かをお願いするものか、受け取るものか |
| `https://api.tavily.com/search` | 接続先のリンク。リクエストを送る宛先 |
| `-H "Authorization: Bearer tvly-..."` | ヘッダー。「自分の会員証はこれです」＝ API キーを載せる部分。**`Bearer ` は残したまま、`tvly-YOUR_API_KEY` の部分を自分のキーに差し替える** |
| `-d '{"query": "..."}'` | 具体的なリクエスト内容。Tavily に何を調べてほしいかというお願い（プロンプトのようなもの） |

## 画面操作の手順

### 1. Tavily のアカウント作成と API キー取得

1. Tavily のサイト（tavily.com）を開き、管理画面 https://app.tavily.com にログインする。
   - Tavily とは：一言で言うと **AI によって強化された Google**。AI が検索をかけ、インターネットの情報を賢く調べてまとめてくれるサービス。
   - **毎月 1000 クレジットまで無料。クレジットカードの登録は不要。**（現行も同じ）
2. **Sign up** からログイン（Google ログイン等。手順は OpenRouter とほぼ同じ）。
3. ダッシュボードの **API キー**の欄から新規作成する。
   - **Key Name**：例 `n8nデモ`。
4. 発行されたキー（**`tvly-` で始まる**）をコピーして、安全な場所に保管する。

> 【クレジットの目安（追記）】basic な検索は 1 クレジット、advanced な検索は 2 クレジット。Research 系の呼び出しは**1回で 4〜250 クレジット**消費することがある。無料枠は月 1000 なので、**Research を多用すると一瞬で使い切る**点を伝えておく。

### 2. Tavily のドキュメントから cURL を取得

1. Tavily サイトの **Documentation** を開く。
2. **Quickstart** を開く。
3. Python / JavaScript / **cURL** のタブがあるので **cURL** を選択。
4. **右上のコピーボタン**でコピー。

### 3. n8n に cURL をインポートする

1. キャンバスの**＋**から `HTTP Request` を検索して追加。
2. HTTP Request ノードの **Parameters** タブに **「Import cURL」** がある。
3. 開いたモーダルにコピーした cURL を**ペースト**。
4. **Import** を押す。
   → **設定が一気にすべて入力される。**（講師の表現：「難解な呪文みたいなものが自動で伝票に書かれたみたいな感じ」）
   > 注意：Import は**既存の設定を上書きする**。

### 4. 【手順変更】API キーは Credential に登録する

> ⚠️ **ここが動画からの最も重要な変更点。**
>
> 動画では、インポートされたヘッダーの値の `Your API Key` の部分に**キーを直接貼り付けて**いる。しかし：
> - ノードのパラメータに直書きした値は、**ワークフローの JSON をエクスポートするとそのまま含まれる**。
> - この回の最後と⑨では、**「エラーが出たらワークフローの JSON をダウンロードして ChatGPT にアップロードする」**と案内している。
> - つまり動画の手順どおりにやると、**受講者の Tavily の API キーが ChatGPT にアップロードされる。**
>
> **API キーは必ず Credential に登録する。** Credential に登録した値は、**JSON エクスポートには含まれない。**

現行版の手順：

1. Import cURL でインポートしたあと、**ヘッダーから `Authorization` の行を削除する**。
2. HTTP Request ノードの **Authentication** を設定する。
   - n8n がそのサービスに対応している場合：**Predefined Credential Type** を選ぶ（推奨。設定が楽）。
   - Tavily のように汎用で繋ぐ場合：**Generic Credential Type → Header Auth** を選ぶ。
     - **Name**：`Authorization`
     - **Value**：`Bearer tvly-（自分のキー）`
   - この Credential に名前を付けて保存する。以降、別のワークフローからも選ぶだけで使える。
3. **Body** の `query` の値を、自分が調べたい内容に書き換える。
   - 例：**`今日のAIニュースについて詳しく教えて`**
   - ⚠️ **ダブルクォーテーション（`" "`）で囲むのを忘れずに。** 忘れがちなポイント。

> 【補足】Import cURL は**すべての値を文字列として取り込む**。数値や真偽値を元の型のまま扱いたい場合は、Body の指定を **Using Fields Below → Using JSON** に切り替えて JSON を直接貼る。

### 5. ノード単体でテスト実行

1. HTTP Request ノードを**単体で1回実行**する。
2. **Output** に Tavily が調べてくれた結果が返ってきたら成功。

### 6. チャット入力と連動させる

- 直接書いていた検索文を、**チャットで入力したものを反映させる**ように変更する。
- Body の `query` の値を式に切り替え、**`{{ $json.chatInput }}`** を指定する。
- チャットから **`今日のAIニュースについて教えて`** と送ると、調べた内容が返ってくる。

## エラーが出たときの対処（フレームワークの先出し）

### 【追記】まず n8n の中で解決を試みる

現行の n8n には、キャンバスを離れずにエラーを相談できる機能がある。**外部にワークフローを持ち出さずに済む**ので、こちらを先に教える。

| 機能 | 使いどころ |
|---|---|
| **n8n Assistant** | チャットでワークフローの作成・編集・テスト・トラブルシューティングを依頼できる |
| **Ask n8n AI** | n8n の使い方についての質問 |
| **AI Workflow Builder** | 自然言語でワークフローを生成・修正・デバッグする |

### 外部の AI に相談する場合

それでも解決しない場合は、ChatGPT や Google AI Studio（Gemini）を使う。

1. ノードの下部（アウトプットのエラー部分）を押すと、**エラーの理由が詳しく出る**。
2. その**エラーメッセージをコピー**。
3. ワークフロー全体の **JSON をエクスポート**する。
4. ⚠️ **渡す前に必ず中身を確認する。**
   - Credential に登録した認証情報は **JSON に含まれない**（安全）。
   - しかし**ノードのパラメータに直書きした API キー・メールアドレス・社内 URL などは含まれる**。
   - 心当たりがあれば、**該当箇所をダミーの文字列に置き換えてから渡す。**
5. ファイルを ChatGPT や Google AI Studio に**アップロード**する。
6. 「◯◯というところでエラーになっています。これを修正したいです」と伝える。
7. → AI がトラブルシューティングをしてくれる。

> **エラーが出たらまず AI に聞いてみる、を習慣づけること。ただし、渡すものに秘密が混ざっていないかを必ず確認すること。**

## 動画中の入力例・設定値（現行版）

| 項目 | 値 |
|---|---|
| 追加ノード | `HTTP Request` |
| 練習用サービス | Tavily（毎月 1000 クレジット無料 / クレカ不要） |
| Tavily API キー名 | `n8nデモ`（キーは `tvly-` で始まる） |
| HTTP メソッド | `POST` |
| URL | `https://api.tavily.com/search` |
| 認証 | **Generic Credential Type → Header Auth**（Name: `Authorization` / Value: `Bearer tvly-...`）※動画はヘッダーに直書き |
| Body のプロンプト（直書き） | `今日のAIニュースについて詳しく教えて` |
| Body のプロンプト（チャット連動） | `{{ $json.chatInput }}` |
| チャット入力 | `今日のAIニュースについて教えて` |
| 保存操作 | 不要（自動保存） |

## 講師が強調すべき点（現行版）

- 外部サービスと連携する際の手順は2点だけ：**① ドキュメントを見つける ② cURL を見つける**。
- API キーは会員証・身分証明書。**ノードに直書きせず、Credential に入れる。**
- **ワークフローの JSON を人や AI に渡すときは、中に秘密が入っていないか必ず確認する。**
- ダブルクォーテーションで囲むのを忘れない。
- 専用ノードがなくても諦める必要はない。**AIエージェントの可能性は文字通り無限大に広がる。**
- **API・HTTP リクエスト・cURL** の3つをしっかり覚えること。

## 出典

- [HTTP Request — n8n Docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest)（Import cURL / Predefined・Generic credentials）
- [Tavily Quickstart](https://docs.tavily.com/documentation/quickstart)（現行の cURL・エンドポイント・無料枠）
- [Credits & Pricing — Tavily Docs](https://docs.tavily.com/documentation/api-credits)
- [Tavily integrations — n8n](https://n8n.io/integrations/tavily/)（検証済みコミュニティノードの存在）
- [Install verified community nodes — n8n Docs](https://docs.n8n.io/integrations/community-nodes/installation-and-management/install-verified-community-nodes)（無料トライアルでは利用不可）
- [Use AI Workflow Builder — n8n Docs](https://docs.n8n.io/build/ways-of-building-workflows/ai-workflow-builder)
