# ホーム画面アイコン用ランチャー

タスクダッシュボード（GAS Web アプリ）を iPhone のホーム画面に追加したとき、
独自アイコンを表示させるための **外部ランチャーページ**。

## なぜ必要か（背景）

GAS の Web アプリは、ブラウザから見て「Google のページの中の入れ子 iframe」として配信される。
iOS がホーム画面アイコンに使う `apple-touch-icon` は **一番外側のページ（Google 側・編集不可）** から読むため、
GAS の `index.html`（iframe 内）に何を書いてもアイコンはブラウザに届かない。
→ GAS 内だけで直そうとした試行（v33〜v40）が全滅した根本原因。

### 解決策
自分で編集できる外部の静的ホスト（GitHub Pages）に「ランチャーページ」を置く。
ランチャーは top-level ドキュメントなので `apple-touch-icon` が iOS に確実に届く。
ホーム画面のアイコンをタップすると、ランチャーが GAS アプリ本体へリダイレクトする。

## 公開先

- 公開 URL: https://mugichaha.github.io/task-dashboard-launcher/
- GitHub リポジトリ: https://github.com/mugichaha/task-dashboard-launcher （public・mugichaha）
- ホスティング: GitHub Pages（main ブランチ root）

## ファイル構成

| ファイル | 役割 |
|---|---|
| `index.html` | ランチャー本体。`apple-touch-icon` を持ち、ホーム画面起動時（`navigator.standalone`）に GAS 本体へリダイレクト |
| `manifest.json` | Android（PWA）用のマニフェスト。iOS では無害 |
| `icon-180.png` | apple-touch-icon（iOS 標準サイズ 180×180） |
| `icon-192.png` | manifest 用アイコン（192×192） |
| `icon-source.png` | アイコンの元画像（Gemini 生成・285×283）。再編集時のソース |

リダイレクト先（GAS 本体 URL）は `index.html` 内の `APP_URL` に記載。

## アイコンの差し替え手順

1. 新しい元画像を用意し `icon-source.png` を差し替え（任意のサイズで可）
2. 正方形に切り抜いて `icon-192.png` / `icon-180.png` を生成（PIL 等）
   - iOS が自動で角丸マスクをかけるので **角まで塗った正方形** が基本
   - 現行アイコン（Gemini 生成）は元画像が「ダーク枠の入れ子デザイン＋外側余白」だったため、
     **外側余白のみ除去**（285×283 → crop `(11, 9, 274, 272)` = 263×263 → 192/180 にリサイズ）
3. `git add -A && git commit && git push origin main`
4. GitHub Pages の再ビルド（30〜60秒）後、URL のアイコンが更新される
5. **iOS はホーム画面アイコンをキャッシュする** → 実機では旧アイコンを一度削除して再追加が必要

## 既知のトレードオフ（許容済み）

ホーム画面アイコン起動時、リダイレクトで別オリジン（Google）へ遷移するため、
iOS の standalone 全画面表示は外れ、通常のブラウザ画面でアプリが開く。
（standalone を保つには iframe 方式が必要だが、GAS `access:MYSELF` × iOS のサードパーティ
Cookie 制限でログインが破綻するため不採用。アイコンが正しく出る＝ゴール達成を優先）

## 履歴

- 2026-05-30: ランチャー方式で初期構築・公開（セッション9）
- 2026-05-30: アイコンを Gemini 生成の3D調デザイン（グロッシーなターゲット×チェック）に差し替え。
  全面化案は大きすぎたため、外枠の入れ子デザインを残す「余白のみ除去」版を採用
