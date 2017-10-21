from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.events import SubscribeEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from lib.utils.common import create_timestamp
from lib.weixin.weixin_sql import subcribe_save_openid, savegoal, get_goals, get_goal_by_id, get_audience, \
    get_goal_history, save_goal_history
from lib.weixin.draw_pic import *
from goal.settings import *


@csrf_exempt
def wx(request):
    if request.method == 'GET':
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
    context = {
        'goal_type': goal_type
    }

    response = render(request, template_name, context)
    return response


def create2(request, goal_type):
    template_name = 'weixin/create2.html'

    context = {
        'goal_type': goal_type,
        'frequent': frequent
    }
    response = render(request, template_name, context)
    return response


def create3(request, goal_id):
    template_name = 'weixin/create3.html'
    goal = get_goal_by_id(goal_id)[0]
    images_dir = os.path.join(STATIC_ROOT, 'images')
    if goal[2] == 'study':
        low_img = os.path.join(images_dir, 'kanshu.jpg')
    elif goal[2] == 'activity':
        low_img = os.path.join(images_dir, 'yundong.jpg')
    elif goal[2] == 'health':
        low_img = os.path.join(images_dir, 'jiankang.jpg')
    elif goal[2] == 'tuodan':
        low_img = os.path.join(images_dir, 'tuodan.jpg')
    elif goal[2] == 'money':
        low_img = os.path.join(images_dir, 'zanqian.jpg')
    elif goal[2] == 'other':
        low_img = os.path.join(images_dir, 'qita.jpg')

    author_name = 'test'
    headimg = os.path.join(images_dir, 'shengji.png')
    two_dimension = ''
    random_str = str(time.time())
    save_img = os.path.join(STATIC_ROOT, 'save_images', random_str + '.jpg')
    draw(low_img, headimg, author_name, goal[3], goal[4], two_dimension, save_img)
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

    author = 'temple'
    status = 0
    goal_id = savegoal(author, goaltype, penalty, int(period), goal_content, status)
    result = 'True&' + str(goal_id)

    return HttpResponse(result)


def createsuccess(request):
    template_name = 'weixin/createsuccess.html'
    author = 'temple'
    goals = get_goals(author)
    context = {
        'goals': goals
    }
    response = render(request, template_name, context)
    return response


def history(request):
    template_name = 'weixin/history.html'
    author = 'temple'
    goals = get_goals(author)
    context = {
        'goals': goals
    }
    response = render(request, template_name, context)
    return response


@csrf_exempt
def save_history(request):
    print('file photo', request.FILES['photo'])
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

    is_own = True

    goal = get_goal_by_id(goal_id)

    audience_list = get_audience(goal_id)

    audience_headimgurl = {}
    for audience in audience_list:
        audience_headimgurl[audience] = ''

    goal_histories = get_goal_history(goal_id)

    if len(goal) > 0:
        goal = goal[0]
    context = {
        'goal': goal,
        'is_own': is_own,
        'headimg_url': '',
        'author_name': '',
        'audience_headimgurl': audience_headimgurl,
        'audience_count': len(audience_list),
        'goal_histories': goal_histories,
        'history_count': len(goal_histories)
    }
    response = render(request, template_name, context)
    return response


def others(request):
    template_name = 'weixin/others.html'
    response = render(request, template_name)
    return response


def ranking(request):
    template_name = 'weixin/ranking.html'
    response = render(request, template_name)
    return response


def goinglog(request, goal_id):
    template_name = 'weixin/goinglog.html'

    context = {
        'goal_id': goal_id
    }
    response = render(request, template_name, context)
    return response
