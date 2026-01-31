from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import ExerciseRecord
from .forms import ExerciseDiaryForm


@login_required
def timer(request):
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
        
        # ----------------------------------------
        # 運動開始処理
        # ----------------------------------------
        if action == 'start':
            # 現在時刻を記録（ここからタイマー開始）
            user.last_exercise_time = timezone.now()
            user.save()
            
            # ページをリロードしてタイマー表示に切り替え
            return redirect('workouts:timer')
            
        # ----------------------------------------
        # 運動終了処理
        # ----------------------------------------
        elif action == 'end':
            # 運動中（last_exercise_timeが存在する）場合のみ処理
            if user.last_exercise_time:
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
                return redirect('workouts:post_exercise', pk=record.pk)
            
            # エラー等の場合はタイマー画面に戻る
            return redirect('workouts:timer')
    
    # ----------------------------------------
    # GETリクエスト（ページ表示）の処理
    # ----------------------------------------
    # ユーザーが現在運動中かどうかを判定
    is_exercising = user.last_exercise_time is not None
    
    context = {
        'is_exercising': is_exercising,
    }
    
    # 運動中なら開始時刻をテンプレートに渡す（JSタイマー用）
    if is_exercising:
        context['start_time'] = user.last_exercise_time
    
    return render(request, 'workouts/timer.html', context)



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
        form = ExerciseDiaryForm(request.POST, instance=record)
        
        # 入力内容にエラーがないかチェック
        if form.is_valid():
            # データベースに保存（日記の内容が更新される）
            form.save()
            
            # 保存完了後はトップ画面へリダイレクト
            return redirect('workouts:index')
    
    # GETリクエスト（最初にページを開いた時）
    else:
        # 既存のデータがあればそれをフォームに入れた状態で初期化
        form = ExerciseDiaryForm(instance=record)
    
    # テンプレートを表示
    # 'form': 入力フォーム
    # 'record': 運動時間などのデータ表示用
    return render(request, 'workouts/post_exercise.html', {
        'form': form,
        'record': record
    })


def index(request):
    """
    トップページ（仮）
    """
    return render(request, 'workouts/index.html')
