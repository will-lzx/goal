import time

import datetime
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.events import SubscribeEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from lib.utils.common import create_timestamp, get_openid, get_user_base_info, is_own_goal
from lib.weixin.weixin_sql import subcribe_save_openid, savegoal, get_goals, get_goal_by_id, get_audience, \
    get_goal_history, save_goal_history, get_history_images, update_goal, get_goals_rank, modify_audience, \
    get_audience_goals
from lib.weixin.draw_pic import *
from goal.settings import *
from weixin.templatetags.own_tag import get_headimg


@csrf_exempt
def wx(request):
    if request.method == 'GET':
        print('wx get msg')
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')

        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echostr = 'error'
        return HttpResponse(echostr, content_type="text/plain")
    if request.method == 'POST':
        print('')
        msg = parse_message(request.body)
        if msg.type == 'text' or msg.type == 'image' or msg.type == 'voice':
            reply = '<xml><ToUserName><![CDATA[' + msg.source + ']]></ToUserName><FromUserName><![CDATA[' + msg.target + \
                    ']]></FromUserName><CreateTime>' + str(create_timestamp()) + '</CreateTime><MsgType><![CDATA[transfer_customer_service]]></MsgType></xml>'
            return HttpResponse(reply, content_type="application/xml")
        elif msg.type == 'event':
            subcribe_event = SubscribeEvent(msg)
            if msg.event == subcribe_event.event:
                reply_msg = '全球自拍达人都在用的智能共享自拍杆，快来一起玩吧！\n\n' \
                            '当你自拍手短或拍照没电的时候，正是我挺"伸"而出之时～\n\n' \
                            '作为一款时尚的共享自拍神器，希望与你一起记录旅游的精彩～'
                reply = create_reply(reply_msg, msg)
                openid = msg.source
                subcribe_save_openid(openid)
            else:
                return 'success'
        else:
            return 'success'
        response = HttpResponse(reply.render(), content_type="application/xml")

        return response
    else:
        print('error')


def create1(request):
    template_name = 'weixin/create1.html'

    open_id = get_open_id(request)

    context = {
        'open_id': open_id,
        'goal_type': goal_type
    }

    response = render(request, template_name, context)
    return response


def create2(request, goal_type, open_id):
    template_name = 'weixin/create2.html'

    context = {
        'open_id': open_id,
        'goal_type': goal_type,
        'frequent': frequent
    }
    response = render(request, template_name, context)
    return response


def create3(request, goal_id, open_id):
    template_name = 'weixin/create3.html'
    goal = get_goal_by_id(goal_id)[0]
    images_dir = os.path.join(STATIC_ROOT, 'images')
    if goal[2] == 'study':
        low_img = os.path.join(images_dir, 'dushu.jpg')
    elif goal[2] == 'activity':
        low_img = os.path.join(images_dir, 'yundong.jpg')
    elif goal[2] == 'health':
        low_img = os.path.join(images_dir, 'jiankang.jpg')
    elif goal[2] == 'tuodan':
        low_img = os.path.join(images_dir, 'tuodan.jpg')
    elif goal[2] == 'money':
        low_img = os.path.join(images_dir, 'cunqian.jpg')
    elif goal[2] == 'work':
        low_img = os.path.join(images_dir, 'qita.jpg')

    user_base_info = get_user_base_info(open_id)

    headimg = user_base_info['headimgurl']
    author_name = user_base_info['nickname']

    random_str = str(time.time())

    two_dimension = os.path.join(STATIC_ROOT, 'save_images', random_str + '.jpg')
    random_str = str(time.time())
    save_img = os.path.join(STATIC_ROOT, 'save_images', random_str + '.jpg')
    draw(low_img, headimg, goal[0], author_name, (goal[7] + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"), goal[3], goal[4], two_dimension, save_img)
    context = {
        'goal': goal,
        'img_url': '/static/save_images/' + random_str + '.jpg'
    }
    response = render(request, template_name, context)
    return response


@csrf_exempt
def save_goal(request):
    goaltype = request.POST.get('goal_type')
    penalty = request.POST.get('penalty')
    period = request.POST.get('period')
    goal_content = request.POST.get('goal_content')

    open_id = request.POST.get('open_id')

    user_base_info = get_user_base_info(open_id)
    print('save_goal', user_base_info, open_id)
    status = 0
    goal_id = savegoal(open_id, goaltype, penalty, int(period), goal_content, status)
    result = 'True&' + str(goal_id)

    return HttpResponse(result)


def createsuccess(request):
    template_name = 'weixin/createsuccess.html'

    open_id = get_open_id(request)

    user_base_info = get_user_base_info(open_id)
    author = user_base_info['nickname']
    goals = get_goals(author)
    context = {
        'goals': goals
    }
    response = render(request, template_name, context)
    return response


def history(request):
    template_name = 'weixin/history.html'

    open_id = get_open_id(request)
    user_base_info = get_user_base_info(open_id)

    author = user_base_info['nickname']

    goals = get_goals(open_id)

    context = {
        'goals': goals
    }
    response = render(request, template_name, context)
    return response


@csrf_exempt
def save_history(request):
    image_url = request.POST.get('image_url')
    goal_id = request.POST.get('goal_id')
    history_content = request.POST.get('history_content')

    try:
        save_goal_history(goal_id, history_content, image_url)
    except Exception as ex:
        return HttpResponse('False&' + str(ex))

    result = 'True&'

    return HttpResponse(result)


def goaldetail(request, goal_id):
    template_name = 'weixin/goaldetail.html'

    open_id = get_open_id(request)

    print('open id and goal id', open_id, goal_id)

    original_goal = get_goal_by_id(goal_id)

    if len(original_goal) > 0:
        goal = original_goal[0]

        is_own = is_own_goal(open_id, goal[1])

    audience_list = get_audience(goal_id)

    audience_headimgurl = {}

    for audience in audience_list:
        audience_headimgurl[audience] = get_headimg(audience)

    goal_histories = get_goal_history(goal_id)

    history_image_list = {}
    for goal_history in goal_histories:
        history_images = get_history_images(goal_history[0])
        images_list = []
        for image in history_images:
            images_list.append(image[1])

        history_image_list[goal_history[0]] = images_list

    context = {
        'open_id': open_id,
        'goal': goal,
        'is_own': is_own,
        'audience_headimgurl': audience_headimgurl,
        'audience_count': len(audience_list),
        'goal_histories': goal_histories,
        'history_count': len(goal_histories),
        'history_image_list': history_image_list
    }

    print('context,', context)
    response = render(request, template_name, context)
    return response


def others(request):
    template_name = 'weixin/others.html'

    open_id = get_open_id(request)

    audience_goals = get_audience_goals(open_id)

    context = {
        'audience_goals': audience_goals
    }

    response = render(request, template_name, context)
    return response


def ranking(request):
    template_name = 'weixin/ranking.html'

    open_id = get_open_id(request)

    goal_rank_dict, sort_values = get_goals_rank()

    context = {
        'open_id': open_id,
        'goal_rank_dict': goal_rank_dict,
        'sort_values': sort_values
    }

    response = render(request, template_name, context)
    return response


def goinglog(request, goal_id):
    template_name = 'weixin/goinglog.html'

    context = {
        'goal_id': goal_id
    }
    response = render(request, template_name, context)
    return response


@csrf_exempt
def goal_action(request):
    goal_id = request.POST.get('goal_id')
    action = request.POST.get('action')
    try:
        update_goal(goal_id, action)
    except Exception as ex:
        return HttpResponse('False&' + str(ex))

    result = 'True&'

    return HttpResponse(result)


@csrf_exempt
def operate_audience(request):
    goal_id = request.POST.get('goal_id')
    action = request.POST.get('action')
    open_id = request.POST.get('open_id')
    try:
        status = modify_audience(goal_id, open_id, action)
    except Exception as ex:
        return HttpResponse('False&' + str(ex))
    if status:
        result = 'True&'
    else:
        result = 'False&'

    return HttpResponse(result)


def get_open_id(request):
    code = request.GET.get('code', None)

    if code and not request.session.get('openid', default=None):
        openid = get_openid(code)
        request.session['openid'] = openid
        print('save session', openid)
    else:
        openid = request.session.get('openid', default=None)
        print('session get', openid)


    print('i want openid', openid)

    return openid



