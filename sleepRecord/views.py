from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Avg
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from .models import SleepRecord
from .forms import SleepRecordForm
from friend.models import Friend
from django.db.models import Q
import calendar


@login_required
def sleeping(request):
    """
    睡眠計測タイマーページ
    GET: タイマー画面を表示
    POST: 睡眠の開始・終了処理を実行
    """
    user = request.user
    # POSTリクエスト（ボタンが押された時）の処理
    if request.method == 'POST':
        # フォームの hidden input 'action' の値を取得 ('start' または 'end')
        action = request.POST.get('action')
        if action == 'start':  # 睡眠開始
            # 現在時刻を記録（ここからタイマー開始）
            user.last_sleep_time = timezone.now()
            user.save()
            # ページをリロードしてタイマー表示に切り替え
        elif action == 'end':  # 睡眠終了
            # 睡眠中（last_sleep_timeが存在する）場合のみ処理
            if user.last_sleep_time is not None:
                start_time = user.last_sleep_time
                end_time = timezone.now()
                # 開始時刻と終了時刻から睡眠時間（分）を計算
                duration_minutes = SleepRecord.calculate_duration(start_time, end_time)
                # 睡眠記録（SleepRecord）をデータベースに保存
                # 日記 (diary) はまだ空のまま作成
                record = SleepRecord.objects.create(
                    user=user,
                    sleep_start_time=start_time,
                    sleep_end_time=end_time,
                    duration_minutes=duration_minutes,
                    diary=''
                )
                # ユーザーの睡眠中状態を解除（次回のためにリセット）
                user.last_sleep_time = None
                user.save()
                # 投稿画面（日記入力画面）へリダイレクト
                return redirect('sleepRecord:post_sleep', pk=record.pk)
            # エラー等の場合はタイマー画面に戻る
            return redirect('sleepRecord:sleeping')

    is_sleeping = user.last_sleep_time is not None
    context = {
        'is_sleeping': is_sleeping,
    }
    # 睡眠中なら開始時刻をテンプレートに渡す（JSタイマー用）
    if is_sleeping:
        context['start_time'] = user.last_sleep_time
    return render(request, 'sleepRecord/sleeping.html', context)


@login_required
def post_sleep(request, pk):
    """
    睡眠終了後の投稿画面（日記入力画面）
    GET: 睡眠データと日記入力フォームを表示
    POST: 入力された日記を保存
    """
    # URLのpk（睡眠記録ID）に対応するデータを取得
    # 必ずログインユーザー本人の記録であることを確認（他人の記録は見れない）
    record = get_object_or_404(SleepRecord, pk=pk, user=request.user)
    # POSTリクエスト（「投稿する」ボタンが押された時）
    if request.method == 'POST':
        # フォームに入力データと、更新対象のレコード(instance)を渡す
        form = SleepRecordForm(request.POST, instance=record)
        # 入力内容にエラーがないかチェック
        if form.is_valid():
            sleep_record = form.save(commit=False)
            # 睡眠時間を再計算
            sleep_record.duration_minutes = SleepRecord.calculate_duration(
                sleep_record.sleep_start_time,
                sleep_record.sleep_end_time
            )
            sleep_record.save()
            # 保存完了後はトップ画面へリダイレクト
            return redirect('sleepRecord:index')

    # GETリクエスト（最初にページを開いた時）
    else:
        # 既存のデータがあればそれをフォームに入れた状態で初期化
        form = SleepRecordForm(instance=record)

    # テンプレートを表示
    # 'form': 入力フォーム
    # 'record': 睡眠時間などのデータ表示用
    return render(request, 'sleepRecord/post_sleep.html', {
        'form': form,
        'record': record,
    })


@login_required
def remove_sleep(request, pk):
    """
    睡眠記録削除
    """
    record = get_object_or_404(SleepRecord, pk=pk, user=request.user)

    if request.method == "POST":
        record.delete()
        messages.success(request, "記録を削除しました。")
        return redirect("sleepRecord:index")
    
    return render(request, 'sleepRecord/remove_sleep.html', {'record': record})


@login_required
def index_view(request):
    """
    睡眠記録一覧（トップページ）
    """
    user = request.user
    sleep_records = SleepRecord.objects.filter(user=user).order_by("-sleep_end_time")
    
    today = timezone.localdate()
    start_date = today - timedelta(days=6)

    start_datetime = timezone.make_aware(
        datetime.combine(start_date, datetime.min.time())
    )
    end_datetime = timezone.make_aware(
        datetime.combine(today, datetime.max.time())
    )

    # 日付ごとに睡眠時間を合算
    records = (
        SleepRecord.objects
        .filter(
            user=user,
            sleep_end_time__range=(start_datetime, end_datetime)
        )
        .annotate(date=TruncDate("sleep_end_time"))
        .values("date")
        .annotate(total_minutes=Sum("duration_minutes"))
        .order_by("date")
    )
    
    weekly_data = []
    total_time = 0
    max_time = 0

    date_map = {r["date"]: r["total_minutes"] for r in records}

    for i in range(7):
        day = start_date + timedelta(days=i)
        minutes = date_map.get(day, 0)

        total_time += minutes
        max_time = max(max_time, minutes)
        height = int((minutes / max_time) * 100) if max_time > 0 else 0

        weekly_data.append({
            "day_of_the_week": calendar.day_abbr[day.weekday()],
            "date": f"{day.month}/{day.day}",
            "time": minutes,
            "height": height,
        })

    average_time = total_time // 7

    # 統計情報
    total_records = sleep_records.count()
    avg_duration = sleep_records.aggregate(Avg('duration_minutes'))['duration_minutes__avg']

    return render(
        request,
        "sleepRecord/index.html",
        {
            "sleep_records": sleep_records,
            "weekly_records": {
                "records": weekly_data,
                "total_time": total_time,
                "average_time": average_time,
                "max_time": max_time,
            },
            "user_profile": user,
            "total_records": total_records,
            "avg_duration": avg_duration,
        },
    )


@login_required
def friends_sleep_records(request):
    """
    フレンドの睡眠記録を取得（24 * 7時間以内）
    """
    # フレンド一覧を取得
    friendships = Friend.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )

    friend_ids = []
    for friendship in friendships:
        if friendship.user1 == request.user:
            friend_ids.append(friendship.user2.id)
        else:
            friend_ids.append(friendship.user1.id)

    # 24時間 * 7日前
    since = timezone.now() - timedelta(hours=24 * 7)

    # フレンドの睡眠記録を取得（7日間以内）
    friends_sleep_records = SleepRecord.objects.filter(
        user_id__in=friend_ids,
        sleep_end_time__gte=since
    ).select_related('user').order_by('-sleep_end_time')

    context = {
        'sleep_records': friends_sleep_records,
    }
    return render(request, 'sleepRecord/friends_sleep_records.html', context)