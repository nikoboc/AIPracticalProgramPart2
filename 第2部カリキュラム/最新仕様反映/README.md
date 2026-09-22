# 第2部 既存動画の説明内容 — 最新仕様反映版

既存の講義動画の内容（[`../既存動画/`](../既存動画/)）を、**2026-09-21 時点の n8n および関連サービスの仕様に合わせて修正したもの**。

| 項目 | 値 |
|---|---|
| 調査日 | **2026-09-21** |
| 実機確認日 | **2026-09-22**（n8n Cloud 無料トライアルのアカウントで確認） |
| n8n の最新版 | **2.40**（2026-09-15 リリース） |
| ベース | [`第2部カリキュラム/既存動画/`](../既存動画/) |
| 元データ | `Transcripts/drive-download-20260921T103213Z-1-001/*.txt` |

> **使い方**
> - 各ファイルの冒頭に **「現行仕様との差分サマリ」** の表がある。**どこが変わったかだけ見たい場合はそこだけ読めばよい。**
> - 本文中の 【追記】【修正】 は、動画には無い／動画と異なる内容。
> - 打ち消し線（~~…~~）は、動画の記述のうち**現行では誤りになったもの**。
> - **仕様は変わり続ける。収録・実施の直前に、この README の「要再確認リスト」を必ず確認すること。**

## ファイル一覧

| # | ファイル | 修正量 | 主な修正内容 |
|---|---|---|---|
| 01 | [オリエンテーション](01_オリエンテーション.md) | 小 | 連携サービス数、前提バージョンの明示 |
| 02 | [基本操作](02_基本操作.md) | **特大** | **Save ボタン廃止／自動保存／Publish**、**アカウント＝インスタンスという構造**、Data Tables 正式化、テンプレート数、Overview・Insights |
| 03 | [AIオートメーションとAIエージェント](03_AIオートメーションとAIエージェント.md) | 小 | Chat Trigger の名称、Agent type 廃止、Streaming |
| 04 | [Credential（認証情報）](04_Credential認証情報.md) | **大** | **Gateway credits の追加**、OpenAI 100クレジット特典の失効、API キー上限の必須化 |
| 05 | [メモリとシステムメッセージ](05_メモリとシステムメッセージ.md) | 中 | Context Window Length の意味、英語推奨のトーン緩和、新オプション |
| 06 | [ツールとオーケストレーション](06_ツールとオーケストレーション.md) | 中 | `$fromAI()` の正式名称、Human-in-the-loop、MCP servers |
| 07 | [APIとHTTPリクエスト](07_APIとHTTPリクエスト.md) | **大** | **API キーを Credential に登録する手順へ変更**、Tavily 公式ノードの存在、cURL の正確化 |
| 08 | [サブエージェント 概念と構成](08_サブエージェント_概念と構成.md) | **大** | **本番ではサブワークフローの Publish が必須**、AI Agent Tool という新しい選択肢、UI ラベルの修正 |
| 09 | [ワークフロー構築のフレームワーク](09_ワークフロー構築のフレームワーク.md) | **大** | **AI Workflow Builder / n8n Assistant の追加**、JSON を外部AIに渡す際の注意、Publish で締める |

## 講座全体に効く最重要の変更：Save ボタンの廃止

**この講座は「n8n には自動保存がない。変更のたびに Save を押せ」というメッセージを②以降ほぼ毎回繰り返している。現行の n8n にこの操作は存在しない。**

| | 動画（n8n 1.x） | 現行（n8n 2.4 以降） |
|---|---|---|
| 保存 | **Save ボタン**を手動で押す。押さないと消える | **1〜5秒で自動保存**。Save ボタン・Ctrl+S・コマンドバーの save はすべて削除済み |
| 保存されたもの | そのまま本番に反映される | すべて**ドラフト（下書き）**。本番には影響しない |
| 本番反映 | **Active / Inactive トグル** | **Publish ボタン**（`Shift` + `P`）。公開したバージョンが本番で動く |
| 取り消し | — | **バージョン履歴**から復元／`Unpublish`（`Cmd/Ctrl` + `U`） |
| `Cmd/Ctrl` + `S` | 保存 | **「Name version（バージョンに名前を付ける）」** |

- 出典：[Save and publish workflows — n8n Docs](https://docs.n8n.io/build/understand-workflows/save-and-publish-workflows) / [Announcing Autosave — n8n Blog](https://blog.n8n.io/announcing-autosave/)（2.4.0、2026-01-13）
- セルフホストのみ `N8N_WORKFLOWS_AUTOSAVE_DISABLED` でオートセーブを無効化でき、その場合 Save ボタンが復活する。**n8n Cloud では無効化できない。**

**教え方の置き換え**：「都度 Save」→ **「編集はドラフト、本番は公開バージョン」**。この2段構えを②で丁寧に入れると、⑧（サブワークフローの Publish）と⑨（完成後の Publish）まで一本の線でつながる。

## 動画では触れていない前提：n8n のアカウントは「インスタンス単位」

**他サービスと構造が違うため、先に伝えておかないと後でつまずく。** 動画には説明がないので追加した（→ [02 基本操作](02_基本操作.md) の「1-2」節）。

- **n8n Cloud はアカウントとインスタンス（ワークスペース）が実質1対1。** サインアップ＝インスタンス作成。Notion や Google のような「1アカウントで複数ワークスペースを切り替える」構造ではない。
- **ユーザーはインスタンスに属する。** 各ユーザーは1つのインスタンスロール（Owner / Admin / Member）を持つ。**Cloud 管理画面に入れるのは Owner のみ。**
- **オーナーのメールはインスタンスごとに一意。インスタンス名（URL）は後から変更できない**（変えるなら新規アカウント＋エクスポート／インポート）。
- **Credential・ワークフロー・実行履歴・Data tables・Gateway credits の残高はすべてインスタンス単位。** ⑧の「Credential を別ワークフローで使い回せる」が成立するのは同じインスタンス内だから。
- **トライアル終了でワークスペースごと削除**（ダウンロード猶予90日）。**講座で作ったものは会社の n8n には自動では引き継がれない。**

出典：[Manage users and access](https://docs.n8n.io/administer/manage-users-and-access) / [Understand instance roles](https://docs.n8n.io/administer/manage-users-and-access/understand-instance-roles) / [Change instance ownership or username](https://docs.n8n.io/deploy/use-n8n-cloud/configure-cloud/change-instance-ownership-or-username)

## 数値の更新一覧

| 項目 | 動画時点 | 2026-09-21 時点 | 出典 |
|---|---|---|---|
| 連携できるサービス数 | 1,000種類以上 | **2,192** | [n8n Integrations](https://n8n.io/integrations/) |
| 公開テンプレート数 | 6,700ちょっと／6,000〜7,000 | **12,428** | [n8n Workflow Templates](https://n8n.io/workflows/) |
| n8n Cloud 無料トライアル | 14日間 | **14日間（変更なし）**。Pro 相当の機能、実行 1,000 回まで、クレカ不要 | [n8n Docs](https://docs.n8n.io/deploy/use-n8n-cloud/start-your-free-trial) |
| Tavily 無料枠 | 毎月 1,000 クレジット | **毎月 1,000 クレジット（変更なし）**。クレカ不要 | [Tavily Docs](https://docs.tavily.com/documentation/api-credits) |
| Data Tables | ベータ版（本格実装前） | **正式機能**（n8n 1.113 以降、全プラン） | [n8n Docs](https://docs.n8n.io/build/work-with-data/data-tables) |
| OpenAI 100 クレジット無料特典 | n8n から提供 | **現存しない。** 実機（2026-09-22）でも確認できず、**Gateway credits に統合された**とみられる | 実機確認 |
| Gateway credits の無料枠 | （機能なし） | **無料トライアル中でも利用可。初期残高 $2.00** | 実機確認（2026-09-22） |

## UI 名称の対応表

古い解説記事・テンプレートを読むときの読み替え表としても使える。

| 動画／1.x の表記 | 現行（2.x）の表記 |
|---|---|
| ダッシュボード／管理画面 | **Overview ページ** |
| `On chat message` | **Chat Trigger** |
| Save ボタン | **（廃止。自動保存）** |
| Active / Inactive トグル | **Publish / Unpublish** |
| （サブワークフロー用トリガー） | **Execute Sub-workflow Trigger**（表示名 When Executed by Another Workflow） |
| Data Mode → `All Data` | **Input data mode → `Accept all data`** |
| `Source for Prompt (User Message)` | **`Prompt`**（`Take from previous node automatically` / `Define below`） |
| キラキラ（✨）ボタン | **Let the model define this parameter**（`$fromAI()`） |
| Agent type（Tools Agent 等）の選択 | **（廃止。すべて Tools Agent）** |
| Edit（エディット）ノード | **Edit Fields（Set）ノード** |

## 動画には無い、現行 n8n の新機能（追加を検討すべきもの）

| 機能 | 内容 | 関連回 |
|---|---|---|
| **Gateway credits** | プロバイダのアカウント・API キーなしで AI モデルを動かせる（n8n 2.36 以降 / Cloud Starter・Pro）。**無料トライアルでも利用可・初期残高 $2.00**（2026-09-22 実機確認） | ④ |
| **AI Workflow Builder** | 自然言語の説明から、動くワークフローを生成・修正・デバッグ | ②⑨ |
| **n8n Assistant / Ask n8n AI** | n8n 内蔵のチャットで作成・編集・テスト・トラブルシューティング | ②⑦⑨ |
| **AI Agent Tool ノード** | 同一キャンバス内にサブエージェントを置ける（別ワークフロー化が不要） | ⑧ |
| **Human-in-the-loop for tools** | AI エージェントが特定のツールを実行する前に人間の承認を挟む（n8n 2.6 以降） | ⑥ |
| **MCP servers ワンクリック接続** | Notion・Linear・monday.com などのツール群をまとめてエージェントに渡す（n8n 2.22 以降） | ⑥ |
| **Insights** | 本番実行数・失敗率・Time saved・平均実行時間の分析 | ② |
| **evaluations** | テストケースを流して AI ワークフローの品質を定量評価する | ⑨ |
| **バージョン履歴 / n8n packages** | 過去バージョンへの復元、ワークフロー一式（`.n8np`）の移送 | ②⑨ |
| **Agent Builder**（Preview） | エージェントを第一級の成果物として構成（スキル・ナレッジベース・チャンネル・サブエージェント） | ⑧（発展） |

## セキュリティ上の修正（動画の手順に問題があるもの）

| # | 問題 | 修正 | 該当回 |
|---|---|---|---|
| 1 | **API キーを HTTP Request ノードのヘッダーに直書きしている。** 直後に「ワークフローの JSON を ChatGPT にアップロードして」と案内しているため、**そのままだと受講者の API キーが外部に渡る** | API キーは **Credential（Generic Credential Type → Header Auth）に登録する**。Credential の値は JSON エクスポートに含まれない | ⑦（⑨に波及） |
| 2 | OpenRouter の API キー作成時、**利用上限（Credit limit）を設定せずに進めている** | OpenRouter 公式ドキュメントは**すべてのキーに上限を設定するよう推奨**。講座では少額の上限を必ず設定させる | ④ |
| 3 | ワークフローの JSON を外部 AI に渡す手順に、**中身の確認ステップがない** | 渡す前に、**ノードに直書きされた API キー・メールアドレス・社内 URL が含まれていないか確認**し、必要ならダミーに置き換える | ⑦⑨ |

## 実機確認の結果（2026-09-22）

無料トライアルのアカウントで実際に確認した結果。**この節の内容は実画面で裏が取れている。**

| # | 確認したこと | 結果 |
|---|---|---|
| 1 | 無料トライアルで Gateway credits が使えるか／初期残高 | **使える。初期残高 $2.00 のフリークレジットを確認。** |
| 2 | n8n から OpenAI 100 クレジットの特典が今もあるか | **確認できず。Gateway credits に統合された模様。**（→ ④の該当箇所は削除済み） |
| 3 | Workflows / Credentials / Executions / Data tables / Templates / Insights の置き場所 | **サイドバーにあるのは Templates と Insights（＋Overview）のみ。Workflows / Credentials / Executions / Data tables は Overview ページの中。**（→ ②の記述を修正済み） |
| 4 | オートセーブの提供状態 | **正式に提供中**（Beta の注記なし） |
| 6 | AI Agent ノードのバージョン | **v3.1** |

## 要再確認リスト（収録・実施の直前に確認すること）

n8n は更新が非常に速い（2026年に入ってから 2.0 → 2.40）。以下は**まだ確定していない／特に変わりやすい**項目。

| # | 確認すること | 理由 |
|---|---|---|
| 5 | **⑨の演習用ワークフローの配布 URL** | 元動画では「こちらが指定する URL」とのみ言及され、文字起こしに URL が残っていない。**現在も不明。受講者へ別途案内が必要**（仕様変更ではない） |
| 7 | **Starter / Pro プランで1アカウントが複数インスタンスを持てるか** | 公式ドキュメントに明示なし。実機でも確認できず。インスタンス名の変更に新規アカウント作成を求めている記述から実質1対1と読めるが、断定できない |

## 元動画側の課題（仕様変更とは無関係）

修正版でも解消できていない、**再収録・編集で対応すべき**もの。

- ⑥の文字起こし末尾に、本編と無関係な音声の断片が混入している。
- ⑨の演習用ワークフローのダウンロード URL が動画中で明示されていない。**現在も不明のため、受講者には講座資料などで別途案内する必要がある。**
- ④で一度エラーが出た後に「失礼しました」と言い直して再実行しており、エラーの原因説明がない。
- 文字起こし由来の誤変換（「デポジット製」「校舎別キャンバス」「中性を簡単にする」など）は [`../既存動画/`](../既存動画/) 側の各ファイルの「備考」に記録済み。

## 主な出典

- [Save and publish workflows](https://docs.n8n.io/build/understand-workflows/save-and-publish-workflows) — 自動保存と Publish
- [Announcing Autosave（n8n Blog）](https://blog.n8n.io/announcing-autosave/) — 2.4.0 / 2026-01-13、Save ボタン廃止
- [Introducing n8n 2.0（n8n Blog）](https://blog.n8n.io/introducing-n8n-2-0/) — 2025-12
- [Release notes](https://docs.n8n.io/changelog/release-notes) — 2.40 / 2026-09-15
- [Use Gateway credits](https://docs.n8n.io/build/understand-workflows/use-gateway-credits)
- [Call n8n Workflow Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolworkflow) — 本番での Publish 要件
- [AI Agent Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolaiagent)
- [Execute Sub-workflow Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflowtrigger)
- [Tools Agent](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/tools-agent)
- [Simple Memory](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorybufferwindow)
- [HTTP Request](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest)
- [Tavily Quickstart](https://docs.tavily.com/documentation/quickstart) / [Tavily on n8n](https://n8n.io/integrations/tavily/)
- [OpenRouter API Authentication](https://openrouter.ai/docs/api-reference/authentication)
