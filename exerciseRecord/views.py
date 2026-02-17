from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from exerciseRecord.forms import ExerciseRecordForm, FeedbackHistoryForm
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import ExerciseRecord, FeedbackHistory
from friend.models import Friend
from .consts import ITEM_PER_PAGE
from django.db.models import Q
import calendar
import json
from .consts import EXERCISES

@login_required
def exercising(request):
    """
    運動計測タイマーページ
    GET: タイマー画面を表示
    POST: 運動の開始・終了処理を実行
    """
    user = request.user
    # POSTリクエスト（ボタンが押された時）の処理
    if request.method == 'POST':
        # フォームの hidden input 'action' の値を取得 ('start' または 'end')
        action = request.POST.get('action')
        if action == 'start': # 運動開始
            # 現在時刻を記録（ここからタイマー開始）
            user.last_exercise_time = timezone.now()
            user.save()
            # ページをリロードしてタイマー表示に切り替え
        elif action == 'end': # 運動終了
            # 運動中（last_exercise_timeが存在する）場合のみ処理
            if user.last_exercise_time is not None:
                start_time = user.last_exercise_time
                end_time = timezone.now()
                # 開始時刻と終了時刻から運動時間（分）を計算
                duration_minutes = ExerciseRecord.calculate_duration(start_time, end_time)
                # 運動記録（ExerciseRecord）をデータベースに保存
                # 日記 (diary) はまだ空のまま作成
                record = ExerciseRecord.objects.create(
                    user=user,
                    exercise_start_time=start_time,
                    exercise_end_time=end_time,
                    duration_minutes=duration_minutes,
                    diary=''
                )
                # ユーザーの運動中状態を解除（次回のためにリセット）
                user.last_exercise_time = None
                user.save()
                # 投稿画面（日記入力画面）へリダイレクト
                return redirect('post_exercise', pk=record.pk)
            # エラー等の場合はタイマー画面に戻る
            return redirect('exercising')

    is_exercising = user.last_exercise_time is not None
    context = {
        'is_exercising': is_exercising,
    }
    # 運動中なら開始時刻をテンプレートに渡す（JSタイマー用）
    if is_exercising:
        context['start_time'] = user.last_exercise_time
    return render(request, 'exerciseRecord/exercising.html', context)

@login_required
def post_exercise(request, pk):
    """
    運動終了後の投稿画面（日記入力画面）
    GET: 運動データと日記入力フォームを表示
    POST: 入力された日記を保存
    """
    # URLのpk（運動記録ID）に対応するデータを取得
    # 必ずログインユーザー本人の記録であることを確認（他人の記録は見れない）
    record = get_object_or_404(ExerciseRecord, pk=pk, user=request.user)
    # POSTリクエスト（「投稿する」ボタンが押された時）
    if request.method == 'POST':
        # フォームに入力データと、更新対象のレコード(instance)を渡す
        form = ExerciseRecordForm(request.POST, instance=record)
        # 入力内容にエラーがないかチェック
        if form.is_valid():
            # データベースに保存（日記の内容が更新される）
            form.save()
            # 保存完了後はトップ画面へリダイレクト
            return redirect('index')

    # GETリクエスト（最初にページを開いた時）
    else:
        # 既存のデータがあればそれをフォームに入れた状態で初期化
        form = ExerciseRecordForm(instance=record)

    # テンプレートを表示
    # 'form': 入力フォーム
    # 'record': 運動時間などのデータ表示用
    return render(request, 'exerciseRecord/post_exercise.html', {
        'form': form,
        'record': record,
        "exercises_json": EXERCISES,
    })


@login_required
def save_feedback(request, pk):
    """
    運動の感想を保存するビュー
    POST: 感想を保存し、感想履歴ページへリダイレクト
    """
    record = get_object_or_404(ExerciseRecord, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = FeedbackHistoryForm(request.POST)
        if form.is_valid():
            # 既存の感想がある場合は削除（OneToOneフィールドのため）
            if hasattr(record, 'feedback_history'):
                record.feedback_history.delete()
            
            # 新しい感想を保存
            feedback = form.save(commit=False)
            feedback.exercise_record = record
            feedback.save()
            
            messages.success(request, '感想を保存しました。')
            return redirect('feedback_history', pk=pk)
    else:
        # GET: 既存の感想があればそれを初期値として設定
        if hasattr(record, 'feedback_history'):
            form = FeedbackHistoryForm(instance=record.feedback_history)
        else:
            form = FeedbackHistoryForm()
    
    return render(request, 'exerciseRecord/save_feedback.html', {
        'form': form,
        'record': record,
    })


@login_required
def feedback_history(request, pk):
    """
    特定の運動記録の感想を表示
    """
    record = get_object_or_404(ExerciseRecord, pk=pk, user=request.user)
    feedback = None
    
    if hasattr(record, 'feedback_history'):
        feedback = record.feedback_history
    
    return render(request, 'exerciseRecord/feedback_history.html', {
        'record': record,
        'feedback': feedback,
    })


@login_required
def feedback_list(request):
    """
    ユーザーの全感想履歴を表示
    """
    user = request.user
    
    # ユーザーの全運動記録で感想がある場合のみ取得
    feedbacks = FeedbackHistory.objects.filter(
        exercise_record__user=user
    ).select_related('exercise_record').order_by('-created_at')
    
    # ページネーション
    paginator = Paginator(feedbacks, ITEM_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'exerciseRecord/feedback_list.html', {
        'page_obj': page_obj,
        'feedbacks': page_obj.object_list,
    })


@login_required
def remove_exercise(request, pk):
    record = get_object_or_404(ExerciseRecord, pk=pk, user=request.user)

    if request.method == "POST":
        record.delete()
        messages.success(request, "記録を削除しました。")
        return redirect("index")

@login_required
def index_view(request):
    user = request.user
    exercise_records = ExerciseRecord.objects.filter(user=user).order_by("-exercise_end_time")
    print(exercise_records)
    today = timezone.localdate()
    start_date = today - timedelta(days=6)

    start_datetime = timezone.make_aware(
        datetime.combine(start_date, datetime.min.time())
    )
    end_datetime = timezone.make_aware(
        datetime.combine(today, datetime.max.time())
    )

    # 日付ごとに運動時間を合算
    records = (
        ExerciseRecord.objects
        .filter(
            user=user,
            exercise_end_time__range=(start_datetime, end_datetime)
        )
        .annotate(date=TruncDate("exercise_end_time"))
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
            "height": height,  # ← これを渡す
        })


    average_time = total_time // 7

    return render(
        request,
        "exerciseRecord/index.html",
        {
            "exercise_records": exercise_records,
            "weekly_records": {
                "records": weekly_data,
                "total_time": total_time,
                "average_time": average_time,
                "max_time": max_time,
            },
            "user_profile": user,
        },
    )

@login_required
def friends_execise_records(request):
    """
    フレンドの運動記録を取得（24 * 7時間以内）
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

    # 24時間前
    since = timezone.now() - timedelta(hours=24 * 7)

    # フレンドの運動記録を取得（24時間以内）
    friends_exercise_records = ExerciseRecord.objects.filter(
        user_id__in=friend_ids,
        exercise_end_time__gte=since
    ).select_related('user').order_by('-exercise_end_time')

    context = {
        'exercise_records': friends_exercise_records,
    }
    return render(request, 'exerciseRecord/friends_exercise_records.html', context)
