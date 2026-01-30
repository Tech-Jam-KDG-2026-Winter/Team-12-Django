from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import User, FriendRequest, Friend, ExerciseRecord
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ExerciseRecordForm
from django.utils import timezone

# Create your views here.
@login_required
def send_friend_request(request, user_id):
    """
    フレンド申請を送る
    """
    to_user = get_object_or_404(User, id=user_id)
    from_user = request.user
    
    # 自分自身には送れない
    if from_user == to_user:
        messages.error(request, '自分自身にフレンド申請はできません')
        return redirect('user_profile', user_id=user_id)
    
    # 既にフレンドかチェック
    if Friend.objects.filter(
        Q(user1=from_user, user2=to_user) | 
        Q(user1=to_user, user2=from_user)
    ).exists():
        messages.info(request, 'すでにフレンドです')
        return redirect('user_profile', user_id=user_id)
    
    # 既に申請済みかチェック
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        messages.info(request, 'すでに申請済みです')
        return redirect('user_profile', user_id=user_id)
    
    # フレンド申請を作成
    FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    messages.success(request, f'{to_user.name}さんにフレンド申請を送りました')
    return redirect('user_profile', user_id=user_id)


@login_required
def accept_friend_request(request, request_id):
    """
    フレンド申請を承認
    """
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    
    # フレンド関係を作成
    Friend.objects.create(
        user1=friend_request.from_user,
        user2=friend_request.to_user
    )
    
    # 申請を削除
    friend_request.delete()
    
    messages.success(request, f'{friend_request.from_user.name}さんとフレンドになりました')
    return redirect('friend_requests')


@login_required
def reject_friend_request(request, request_id):
    """
    フレンド申請を拒否
    """
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    from_user_name = friend_request.from_user.name
    
    # 申請を削除
    friend_request.delete()
    
    messages.info(request, f'{from_user_name}さんからの申請を拒否しました')
    return redirect('friend_requests')


@login_required
def cancel_friend_request(request, request_id):
    """
    送ったフレンド申請をキャンセル
    """
    friend_request = get_object_or_404(FriendRequest, id=request_id, from_user=request.user)
    to_user_name = friend_request.to_user.name
    
    # 申請を削除
    friend_request.delete()
    
    messages.info(request, f'{to_user_name}さんへの申請をキャンセルしました')
    return redirect('sent_requests')


@login_required
def remove_friend(request, friend_id):
    """
    フレンドを削除
    """
    friend = get_object_or_404(
        Friend,
        Q(id=friend_id) & (Q(user1=request.user) | Q(user2=request.user))
    )
    
    # フレンドの名前を取得
    if friend.user1 == request.user:
        friend_name = friend.user2.name
    else:
        friend_name = friend.user1.name
    
    # フレンド関係を削除
    friend.delete()
    
    messages.success(request, f'{friend_name}さんをフレンドから削除しました')
    return redirect('friends_list')


@login_required
def friend_requests(request):
    """
    受け取ったフレンド申請一覧
    """
    received_requests = FriendRequest.objects.filter(to_user=request.user).select_related('from_user')
    
    context = {'received_requests': received_requests,}
    return render(request, 'friends/friend_requests.html', context)


@login_required
def sent_requests(request):
    """
    送ったフレンド申請一覧
    """
    sent_requests = FriendRequest.objects.filter(from_user=request.user).select_related('to_user')
    
    context = {'sent_requests': sent_requests,}
    return render(request, 'friends/sent_requests.html', context)


@login_required
def friends_list(request):
    """
    フレンド一覧
    """
    # 自分がuser1またはuser2のフレンド関係を取得
    friendships = Friend.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).select_related('user1', 'user2')
    
    # フレンドのユーザーオブジェクトを抽出
    friends = []
    for friendship in friendships:
        if friendship.user1 == request.user:
            friends.append({
                'user': friendship.user2,
                'friendship_id': friendship.id,
                'created_at': friendship.created_at
            })
        else:
            friends.append({
                'user': friendship.user1,
                'friendship_id': friendship.id,
                'created_at': friendship.created_at
            })
    
    context = {'friends': friends,}
    return render(request, 'friends/friends_list.html', context)


@login_required
def get_friends_sleep_records(request):
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
    return render(request, 'friends/friends_exercise_records.html', context)

@login_required
def start_exercise(request):
    """
    運動を開始する
    """
    user = request.user
    
    # 既に運動中かチェック
    if user.last_exercise_time:
        messages.warning(request, '既に運動を開始しています')
        return redirect('index')
    
    # 現在時刻を保存
    user.last_exercise_time = timezone.now()
    user.save()
    
    messages.success(request, '運動を開始しました！')
    return redirect('index')

@login_required
def finish_exercise(request):
    """
    運動を終了する
    """
    user = request.user
    
    # 運動を開始しているかチェック
    if not user.last_exercise_time:
        messages.error(request, '運動を開始していません')
        return redirect('index')
    
    if request.method == 'POST':
        form = ExerciseRecordForm(request.POST)
        if form.is_valid():
            exercise_record = form.save(commit=False)
            exercise_record.user = user
            exercise_record.exercise_start_time = user.last_exercise_time
            exercise_record.exercise_end_time = timezone.now()
            exercise_record.save()
            
            # last_exercise_timeをリセット
            user.last_exercise_time = None
            user.save()
            
            # 運動時間を計算
            duration = exercise_record.exercise_end_time - exercise_record.exercise_start_time
            duration_minutes = int(duration.total_seconds() / 60)
            
            messages.success(request, f'運動を記録しました！（運動時間: {duration_minutes}分）')
            return redirect('exercise_record_list')
    else:
        form = ExerciseRecordForm()
    
    # 現在の運動時間を計算
    current_duration = timezone.now() - user.last_exercise_time
    current_minutes = int(current_duration.total_seconds() / 60)
    
    context = {
        'form': form,
        'start_time': user.last_exercise_time,
        'current_duration': current_minutes,
    }
    return render(request, 'exercise/finish_exercise.html', context)


# @login_required
# class ExerciseRecordCreateView(LoginRequiredMixin, CreateView):
#     model = ExerciseRecord
#     form_class = ExerciseRecordForm
#     template_name = 'exercise_record_form.html'
#     success_url = reverse_lazy('index')
    
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)