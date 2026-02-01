from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import FriendRequest, Friend
from accounts.models import User
from exerciseRecord.models import ExerciseRecord
from django.urls import reverse_lazy
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
        return redirect(request.META.get('HTTP_REFERER', 'friend:user_search'))

    # 既にフレンドかチェック
    if Friend.objects.filter(
        Q(user1=from_user, user2=to_user) | Q(user1=to_user, user2=from_user)
    ).exists():
        messages.info(request, 'すでにフレンドです')
        return redirect(request.META.get('HTTP_REFERER', 'friend:user_search'))

    # 既に申請済みかチェック
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        messages.info(request, 'すでに申請済みです')
        return redirect(request.META.get('HTTP_REFERER', 'friend:user_search'))

    # フレンド申請を作成
    FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    messages.success(request, f'{to_user.username}さんにフレンド申請を送りました')
    return redirect(request.META.get('HTTP_REFERER', 'friend:user_search'))

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

    messages.success(request, f'{friend_request.from_user.username}さんとフレンドになりました')
    return redirect('friend:friend_requests')


@login_required
def reject_friend_request(request, request_id):
    """
    フレンド申請を拒否
    """
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    from_user_name = friend_request.from_user.username

    # 申請を削除
    friend_request.delete()

    messages.info(request, f'{from_user_name}さんからの申請を拒否しました')
    return redirect('friend:friend_requests')


@login_required
def cancel_friend_request(request, request_id):
    """
    送ったフレンド申請をキャンセル
    """
    friend_request = get_object_or_404(FriendRequest, id=request_id, from_user=request.user)
    to_user_name = friend_request.to_user.username

    # 申請を削除
    friend_request.delete()

    messages.info(request, f'{to_user_name}さんへの申請をキャンセルしました')
    return redirect(request.META.get('HTTP_REFERER', 'friend:user_search'))


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
        friend_name = friend.user2.username
    else:
        friend_name = friend.user1.username

    # フレンド関係を削除
    friend.delete()

    messages.success(request, f'{friend_name}さんをフレンドから削除しました')
    return redirect(request.META.get('HTTP_REFERER', 'friend:friends'))


@login_required
def friend_requests(request):
    """
    受け取ったフレンド申請一覧
    """
    received_requests = FriendRequest.objects.filter(to_user=request.user).select_related('from_user')

    context = {'received_requests': received_requests,}
    return render(request, 'friend/friend_requests.html', context)

@login_required
def sent_requests(request):
    """
    送ったフレンド申請一覧
    """
    sent_requests = FriendRequest.objects.filter(from_user=request.user).select_related('to_user')

    context = {'sent_requests': sent_requests,}
    return render(request, 'friend/sent_requests.html', context)

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
                'friend_id': friendship.id,
                'created_at': friendship.created_at
            })
        else:
            friends.append({
                'user': friendship.user1,
                'friend_id': friendship.id,
                'created_at': friendship.created_at
            })

    context = {'friends': friends,}
    return render(request, 'friend/friends_list.html', context)

@login_required
def user_search(request):
    query = request.GET.get("q", "")
    users = []

    if query:
        users = (
            User.objects
            .filter(username__icontains=query)
            .exclude(id=request.user.id)
        )
    else:
        users = (
            User.objects
            .filter(username__icontains=query)
            .exclude(id=request.user.id)
        )[:5]  # 先頭5件だけ取得

    for user in users:
        # すでにフレンドか
        user.is_friend = Friend.objects.filter(
            Q(user1=request.user, user2=user) |
            Q(user1=user, user2=request.user)
        ).exists()

        # 申請済みか
        user.friend_request = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=user
        ).first()  # 存在しなければ None を返す

    return render(request, "friend/user_search.html", {
        "query": query,
        "users": users,
    })