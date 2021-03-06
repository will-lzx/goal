import datetime
import json

from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.events import SubscribeEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from lib.utils.common import create_timestamp, get_openid, get_user_base_info, is_own_goal, is_subscribe
from lib.weixin.weixin_sql import subcribe_save_openid, savegoal, get_goals, get_goal_by_id, get_audience, \
    get_goal_history, save_goal_history, get_history_images, update_goal, get_goals_rank, modify_audience, \
    get_audience_goals, get_history_image
from lib.weixin.draw_pic import *
from goal.settings import *
from weixin.models import Goal
from weixin.templatetags.own_tag import get_headimg, get_goal_current_status

import logging
log = logging.getLogger('django')


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


def create(request):
    template_name = 'weixin/create.html'

    open_id = get_open_id(request)

    context = {
        'open_id': open_id,
        'goal_type': GOAL_TYPE,
        'frequent': FREQUENT,
        'frequent_value': FREQUENT_VALUE[1],
        'period': PERIOD
    }

    response = render(request, template_name, context)
    return response


@csrf_exempt
def get_frequent(request):
    index = request.POST.get('index', None)
    if not index:
        index = 0

    values = FREQUENT_VALUE[int(index)]

    value_list = []
    for k, v in values.items():
        value_list.append({'index': k, 'value': v})

    return HttpResponse(json.dumps(value_list), content_type="application/json")


def create3(request, goal_id, open_id):
    template_name = 'weixin/create3.html'
    goal = get_goal_by_id(goal_id)[0]
    images_dir = os.path.join(STATIC_ROOT, 'images')

    image_name = ''
    if goal[2] == 'study':
        image_name = 'dushu.jpg'
    elif goal[2] == 'activity':
        image_name = 'yundong.jpg'
    elif goal[2] == 'health':
        image_name = 'jiankang.jpg'
    elif goal[2] == 'tuodan':
        image_name = 'tuodan.jpg'
    elif goal[2] == 'money':
        image_name = 'cunqian.jpg'
    elif goal[2] == 'work':
        image_name = 'work.jpg'

    low_img = os.path.join(images_dir, image_name)

    user_base_info = get_user_base_info(open_id)

    headimg = user_base_info['headimgurl']
    author_name = user_base_info['nickname']

    two_dimension_link = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1e0129928b50b3e7&redirect_uri=http%3A%2F%2Fmgoal.cn%2Fweixin%2Fgoaldetail%2F{0}%2F&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect'.format(goal_id)
    random_str = str(time.time())
    save_img = os.path.join(STATIC_ROOT, 'save_images', random_str + '.jpg')
    draw(low_img, headimg, author_name, (goal[7] + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"), goal[3], goal[4], two_dimension_link, save_img)
    context = {
        'goal': goal,
        'img_url': '/static/save_images/' + random_str + '.jpg'
    }
    response = render(request, template_name, context)
    return response


def privatecenter(request):
    template_name = 'weixin/privatecenter.html'

    open_id = get_open_id(request)

    goals = Goal.objects.filter(author=open_id).order_by('-createtime')
    context = {
        'goals': goals
    }

    response = render(request, template_name, context)
    return response


def goal_square(request):
    template_name = 'weixin/goal_square.html'

    open_id = get_open_id(request)

    context = {}

    response = render(request, template_name, context)
    return response


def verify(request):
    template_name = 'weixin/verify.html'

    open_id = get_open_id(request)

    context = {}

    response = render(request, template_name, context)
    return response


def xuanyao(request, goal_id):
    template_name = 'weixin/xuanyao.html'

    goals = Goal.objects.filter(id=goal_id)

    if goals:
        goal = goals.first()
    else:
        return HttpResponse('Goal not exist')

    images_dir = os.path.join(STATIC_ROOT, 'images')

    if goal.goal_type == 1:
        image_name = 'done_dushu.jpg'
    elif goal.goal_type == 2:
        image_name = 'done_yundong.jpg'
    elif goal.goal_type == 3:
        image_name = 'done_yundong.jpg'
    elif goal.goal_type == 4:
        image_name = 'done_yundong.jpg'
    elif goal.goal_type == 5:
        image_name = 'done_yundong.jpg'
    else:
        image_name = 'done_yundong.jpg'

    low_img = os.path.join(images_dir, image_name)

    random_str = str(time.time())

    save_img = os.path.join(STATIC_ROOT, 'save_images', random_str + '.jpg')

    two_dimension_link = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI4NjkxMDg5Mw==&scene=124#wechat_redirect'

    draw_xuanyao(low_img, save_img, two_dimension_link)

    context = {
        'image_url': '/static/save_images/' + random_str + '.jpg'
    }
    response = render(request, template_name, context)
    return response


@csrf_exempt
def save_goal(request):
    open_id = get_open_id(request)
    if request.method == 'POST':
        goal_type = request.POST.get('direction', None)
        frequence = request.POST.get('frequent', None)
        frequent_value = request.POST.get('frequent_value', None)
        period = request.POST.get('period', None)
        goal_value = request.POST.get('goal_value', None)

        goal_dict = {
            'goal_type': int(goal_type),
            'frequent': int(frequence),
            'frequent_value': int(frequent_value),
            'period': int(period),
            'goal_value': float(goal_value),
            'author': open_id,
            'createtime': datetime.datetime.now()
        }

        try:
            Goal.objects.create(**goal_dict)
        except Exception as ex:
            log.info(str(ex))
            return HttpResponse('fail&create goal fail')

        goal = Goal.objects.filter(author=open_id).order_by('-createtime').first()
        return HttpResponse('success&' + str(goal.id))


def createsuccess(request, goal_id):
    template_name = 'weixin/createsuccess.html'

    open_id = get_open_id(request)

    # user_base_info = get_user_base_info(open_id)
    # author = user_base_info['nickname']
    goals = Goal.objects.filter(id=goal_id)

    if goals:
        goal = goals.first()
        context = {
            'goal_id': goal.id,
            'open_id': open_id,
            'goal_type': GOAL_TYPE[goal.goal_type],
            'frequence': FREQUENT[goal.frequent],
            'frequent_value': FREQUENT_VALUE[goal.goal_type][goal.frequent_value],
            'period': PERIOD[goal.period],
            'goal_value': float(goal.goal_value)
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
    files = request.FILES.getlist("photo", None)

    print('files count', len(files))

    history_content = request.POST.get("goal_log", None)
    goal_id = request.POST.get('goal_id', None)

    try:
        save_goal_history(goal_id, history_content, files)
    except Exception as ex:
        return HttpResponse('False&' + str(ex))

    return HttpResponse('True&')


def goaldetail(request, goal_id):
    template_name = 'weixin/goaldetail.html'

    open_id = get_open_id(request)

    #is_subscribed = is_subscribe(open_id)
    is_subscribed = True

    if not is_subscribed:
        redirect_link = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI4NjkxMDg5Mw==&scene=124#wechat_redirect'
        return HttpResponseRedirect(redirect_link)

    goal_id = goal_id.split('/')[0]

    original_goal = Goal.objects.filter(id=int(goal_id))

    if original_goal:
        goal = original_goal.first()

        is_own = is_own_goal(open_id, goal.author)
    else:
        return HttpResponse('goal not exist')

    audience_list = get_audience(goal_id)

    audience_headimgurl = {}

    # for audience in audience_list:
    #     audience_headimgurl[audience[0]] = get_headimg(audience[0])

    # is_audience = False
    #
    # if not is_own:
    #     if audience_headimgurl.keys().__contains__(open_id):
    #         is_audience = True

    goal_histories = get_goal_history(goal_id)

    history_image_list = {}
    for goal_history in goal_histories:
        history_images = get_history_images(goal_history[0])
        images_list = []
        for image in history_images:
            images_list.append(image[2])

        history_image_list[goal_history[0]] = images_list

    context = {
        'open_id': open_id,
        'goal': goal,
        'is_own': is_own,
        'is_audience': is_audience,
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

    goal_id_status_dict = {}

    audience_goals = get_audience_goals(open_id)

    for audience in audience_goals:
        goal_id_status_dict[audience[0]] = get_goal_current_status(audience[0])

    context = {
        'audience_goals': audience_goals,
        'goal_id_status_dict': goal_id_status_dict
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


@csrf_exempt
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
        audience_count = len(get_audience(goal_id))

        audience_list = get_audience(goal_id)

        audience_headimgurl = {}

        for audience in audience_list:
            audience_headimgurl[audience[0]] = get_headimg(audience[0])

    except Exception as ex:
        return HttpResponse('False&' + str(ex))
    if status:
        audience_imgs = '<h4>监督好友（' + str(audience_count) + '）</h4><div class="jd_con">'
        for k, v in audience_headimgurl.items():
            audience_imgs = audience_imgs + '<img class="img_jd" src="' + v + '" alt="监督好友">'

        audience_imgs = audience_imgs + '</div>'
        result = 'True&' + str(audience_count) + '&' + audience_imgs
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

    openid = '123'
    return openid


def pil_image(request, history_id, index):
    data = get_history_image(history_id, index)
    data_stream = io.BytesIO(data)

    im = Image.open(data_stream)
    response = HttpResponse(content_type="image/png")
    im.save(response, 'PNG')
    return response




