MAX_RATE = 5
ITEM_PER_PAGE = 2

EXERCISES = {
    "upperArms": {
        "name": "上腕(二頭・三頭)",
        "exercises": [
            {"name": "アームカール", "type": "reps"},
            {"name": "トライセプスエクステンション", "type": "reps"},
            {"name": "ディップス", "type": "reps"},
            {"name": "ケーブルプッシュダウン", "type": "reps"},
            {"name": "ダイヤモンドプッシュアップ", "type": "reps"}
        ]
    },
    "lowerBody": {
        "name": "下半身(脚・臀部)",
        "exercises": [
            {"name": "スクワット", "type": "reps"},
            {"name": "ブルガリアンスクワット", "type": "reps"},
            {"name": "ランジ", "type": "reps"},
            {"name": "レッグプレス", "type": "reps"},
            {"name": "レッグエクステンション", "type": "reps"},
            {"name": "レッグカール", "type": "reps"},
            {"name": "シシースクワット", "type": "reps"},
            {"name": "ステップアップ", "type": "reps"},
            {"name": "カーフレイズ", "type": "reps"},
            {"name": "ヒップブリッジ", "type": "reps"},
            {"name": "ヒップスラスト", "type": "reps"},
            {"name": "ドンキーキック", "type": "reps"},
            {"name": "ファイアハイドラント", "type": "reps"},
            {"name": "レッグアダクション", "type": "reps"},
            {"name": "レッグアブダクション", "type": "reps"},
            {"name": "グッドモーニング", "type": "reps"}
        ]
    },
    "core": {
        "name": "体幹・腹筋",
        "exercises": [
            {"name": "クランチ", "type": "reps"},
            {"name": "シットアップ", "type": "reps"},
            {"name": "レッグレイズ", "type": "reps"},
            {"name": "ロシアンツイスト", "type": "reps"},
            {"name": "プランク", "type": "time"},
            {"name": "サイドプランク", "type": "time"},
            {"name": "フラッターキック", "type": "reps"},
            {"name": "マウンテンクライマー", "type": "reps"},
            {"name": "ドラゴンフラッグ", "type": "reps"},
            {"name": "アブローラー", "type": "reps"},
            {"name": "デッドバグ", "type": "reps"}
        ]
    },
    "back": {
        "name": "背中",
        "exercises": [
            {"name": "デッドリフト", "type": "reps"},
            {"name": "ラットプルダウン", "type": "reps"},
            {"name": "ローイング", "type": "reps"},
            {"name": "ベントオーバーロウ", "type": "reps"},
            {"name": "ワンハンドロウ", "type": "reps"},
            {"name": "懸垂", "type": "reps"},
            {"name": "フェイスプル", "type": "reps"},
            {"name": "シュラッグ", "type": "reps"},
            {"name": "バックエクステンション", "type": "reps"},
            {"name": "スーパーマン", "type": "reps"}
        ]
    },
    "chest": {
        "name": "胸・プッシュ系",
        "exercises": [
            {"name": "ベンチプレス", "type": "reps"},
            {"name": "チェストプレス", "type": "reps"},
            {"name": "ダンベルフライ", "type": "reps"},
            {"name": "ペックフライ", "type": "reps"},
            {"name": "インクラインプレス", "type": "reps"},
            {"name": "プッシュアップ", "type": "reps"},
            {"name": "ケーブルクロスオーバー", "type": "reps"}
        ]
    },
    "cardio": {
        "name": "有酸素・全身",
        "exercises": [
            {"name": "ウォーキング", "type": "time"},
            {"name": "ランニング", "type": "time"},
            {"name": "バーピー", "type": "reps"},
            {"name": "ジャンピングジャック", "type": "reps"},
            {"name": "ハイニー", "type": "reps"},
            {"name": "バットキック", "type": "reps"},
            {"name": "インチワーム", "type": "time"},
            {"name": "ベアクロール", "type": "time"},
            {"name": "クラブウォーク", "type": "time"},
            {"name": "スケーター", "type": "time"}
        ]
    },
    "martialArts": {
        "name": "格闘・コンディショニング",
        "exercises": [
            {"name": "シャドーボクシング", "type": "time"},
            {"name": "キックボクシング", "type": "time"},
            {"name": "サンドバッグ打ち", "type": "time"},
            {"name": "エアキック", "type": "time"}
        ]
    },
    "bodyCare": {
        "name": "ボディケア・調整",
        "exercises": [
            {"name": "ヨガ", "type": "time"},
            {"name": "ピラティス", "type": "time"},
            {"name": "ストレッチ", "type": "time"},
            {"name": "体操", "type": "time"},
            {"name": "太極拳", "type": "time"}
        ]
    },
    "aquatic": {
        "name": "水中運動",
        "exercises": [
            {"name": "水泳", "type": "time"},
            {"name": "水中ウォーキング", "type": "time"},
            {"name": "水中エアロビクス", "type": "time"}
        ]
    },
    "sports": {
        "name": "スポーツ",
        "exercises": [
            {"name": "テニス", "type": "time"},
            {"name": "バドミントン", "type": "time"},
            {"name": "卓球", "type": "time"},
            {"name": "バスケットボール", "type": "time"},
            {"name": "サッカー", "type": "time"},
            {"name": "バレーボール", "type": "time"},
            {"name": "野球", "type": "time"},
            {"name": "ボウリング", "type": "time"}
        ]
    },
    "others": {
        "name": "その他",
        "exercises": [
            {"name": "その他", "type": "time"}
        ]
    },
    "e-sports": {
        "name": "eスポーツ",
        "exercises": [
            {"name": "League of Legends", "type": "time"}
        ]
    }
}