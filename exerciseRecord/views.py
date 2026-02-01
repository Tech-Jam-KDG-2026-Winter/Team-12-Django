from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from exerciseRecord.forms import ExerciseRecordForm
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import ExerciseRecord
from friend.models import Friend
from .consts import ITEM_PER_PAGE
from django.db.models import Q


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
        'record': record
    })

@login_required
def index_view(request):
    exercise_records = ExerciseRecord.objects.filter(user=request.user).order_by("-created_at")

    return render(
        request,
        "exerciseRecord/index.html",
        {
            "exercise_records": exercise_records,
            "user_profile": request.user,  # ←ここでユーザー情報を渡す
        },
    )


@login_required
def friends_execise_records(request):
    """
    フレンドの運動記録を取得
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

    # フレンドの運動記録を取得
    friends_exercise_records = ExerciseRecord.objects.filter(
        user_id__in=friend_ids
    ).select_related('user').order_by('-created_at')[:50]  # 最新50件

    context = {'exercise_records': friends_exercise_records,}
    return render(request, 'exerciseRecord/friends_exercise_records.html', context)