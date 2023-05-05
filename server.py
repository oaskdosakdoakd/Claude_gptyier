import web
import requests
import jsonpath
import json
import random
import time
import html


urls = (
    '/gptyier', 'gptyier',
    '/setsession', 'setsession',
    '/stream', 'stream',
    '/css/(.*)', 'static_handler_css',
    '/js/(.*)', 'static_handler_js',
)

headers = {
        'Host': 'yierco.slack.com',
        'Cookie': '',
    }

token="xoxc-5112221223653-aaa-5112252871845-d53f887502bdd5bb9d4a0c232ff34e37cb8bfa249690bbcfb5de90b57bfd9375"

Claude_userid="U0542RBDN4Q"
fangjian_id="C0536GHFS2J"

app = web.application(urls, globals())
app.debug = False
render = web.template.render('templates')


class gptyier:
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8')
        with open('gpt.html', 'r',encoding='utf-8') as file:
            html_content = file.read()
        return html_content



class static_handler_css:
    def GET(self, filename):
        try:
            with open(f'css/{filename}', 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise web.notfound("File not found")
class static_handler_js:
    def GET(self, filename):
        try:
            with open(f'js/{filename}', 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise web.notfound("File not found")

class setsession:

    def POST(self):

        stream_url_post_postMessage_r_json_ts = web.cookies().get('ts')
        url_conversations_replies_huoqu_latest_reply_json_latest_reply2 = web.cookies().get('latest_reply')


        setsession_data = web.input(message=None)
        message = setsession_data.message


        message=message.replace("\"", '\\\"')

        print(message)

        prompt=message


        url_post_postMessage = 'https://yierco.slack.com/api/chat.postMessage'

        if(url_conversations_replies_huoqu_latest_reply_json_latest_reply2!=None):
            url_post_postMessage_file = {
                'token': (None,
                          token,
                          None),
                'channel': (None, '{}'.format(fangjian_id), None),
                'ts': (None, '1681546073.xxxxx5', None),
                'type': (None, 'message', None),
                'reply_broadcast': (None, 'false', None),
                'thread_ts': (None, '{}'.format(stream_url_post_postMessage_r_json_ts), None),
                'unfurl': (None, '[]', None),
                'blocks': (None,
                           '[{"type":"rich_text","elements":[{"type":"rich_text_section","elements":[{"type":"user","user_id":"%s"},{"type":"text","text":" %s"}]}]}]' % (
                               Claude_userid,prompt), None),
                'include_channel_perm_error': (None, 'true', None),
                '_x_reason': (None, 'webapp_message_send', None),
                '_x_mode': (None, 'online', None),
                '_x_sonic': (None, 'true', None)
            }
        else:
            url_post_postMessage_file = {
                'token': (None,
                          token,
                          None),
                'channel': (None, '{}'.format(fangjian_id), None),
                'ts': (None, '1681546073.xxxxx5', None),
                'type': (None, 'message', None),
                'unfurl': (None, '[]', None),
                'blocks': (None,
                           '[{"type":"rich_text","elements":[{"type":"rich_text_section","elements":[{"type":"user","user_id":"%s"},{"type":"text","text":" %s"}]}]}]' % (
                               Claude_userid,prompt), None),
                'include_channel_perm_error': (None, 'true', None),
                '_x_reason': (None, 'webapp_message_send', None),
                '_x_mode': (None, 'online', None),
                '_x_sonic': (None, 'true', None)
            }

        try:
            url_post_postMessage_r = requests.post(url_post_postMessage, headers=headers,
                                               files=url_post_postMessage_file, verify=False)

        except BaseException as e:
            print("查询失败,正在重试")
            print(e)
            for o in range(100):
                try:
                    url_post_postMessage_r = requests.post(url_post_postMessage, headers=headers,
                                                           files=url_post_postMessage_file, verify=False)
                    if url_post_postMessage_r.status_code == 200:
                        break
                except BaseException as e:
                    print("再次查询子域名失败", o)
                    print(e)

        if ("\"ok\":true" in url_post_postMessage_r.text and "thread_ts" in url_post_postMessage_r.text and url_conversations_replies_huoqu_latest_reply_json_latest_reply2!=None):
            url_post_postMessage_r_json = json.loads(url_post_postMessage_r.text)
            url_post_postMessage_r_json_thread_ts = jsonpath.jsonpath(url_post_postMessage_r_json, "$.message.thread_ts")[0]

            url_post_postMessage_r_json_ts = jsonpath.jsonpath(url_post_postMessage_r_json, "$.ts")[0]
            web.setcookie('ts', '{}'.format(url_post_postMessage_r_json_thread_ts), 36000)
            web.setcookie('thread_ts', '{}'.format(url_post_postMessage_r_json_ts), 36000)


            return '{"success":true}'
        elif ("\"ok\":true" in url_post_postMessage_r.text and url_conversations_replies_huoqu_latest_reply_json_latest_reply2==None):
            url_post_postMessage_r_json = json.loads(url_post_postMessage_r.text)
            url_post_postMessage_r_json_ts = jsonpath.jsonpath(url_post_postMessage_r_json, "$.ts")[0]
            web.setcookie('ts', '{}'.format(url_post_postMessage_r_json_ts), 36000)

            return '{"success":true}'
        else:
            return '{"success":false}'


class stream:
    def GET(self):

        stream_url_post_postMessage_r_json_ts = web.cookies().get('ts')
        # url_conversations_replies_huoqu_latest_reply_json_latest_reply2 = web.cookies().get('latest_reply')
        url_post_postMessage_r_json_thread_ts = web.cookies().get('thread_ts')

        url_conversations_replies = 'https://yierco.slack.com/api/conversations.replies'


        for i in range(120):
            try:
                url_conversations_replies_file = {
                    'token': (None,
                              token,
                              None),
                    'channel': (None, '{}'.format(fangjian_id), None),
                    'ts': (None, '{}'.format(stream_url_post_postMessage_r_json_ts), None),
                    'inclusive': (None, 'ture', None),
                    'limit': (None, '28', None),
                    'oldest': (None, '{}'.format(stream_url_post_postMessage_r_json_ts), None),
                    '_x_reason': (None, 'history-api/fetchReplies', None),
                    '_x_mode': (None, 'online', None),
                    '_x_sonic': (None, 'true', None)
                }
                url_conversations_replies_huoqu_latest_reply = requests.post(url_conversations_replies, headers=headers,
                                                        files=url_conversations_replies_file, verify=False)
            except BaseException as e:
                print("查询失败,正在重试")
                print(e)
                for o in range(100):
                    try:
                        url_conversations_replies_huoqu_latest_reply = requests.post(url_conversations_replies, headers=headers,
                                                                    files=url_conversations_replies_file,
                                                                    verify=False)
                        if url_conversations_replies_huoqu_latest_reply.status_code == 200:
                            break
                    except BaseException as e:
                        print("再次查询子域名失败", o)
                        print(e)

            if(i>2 and "latest_reply" not in url_conversations_replies_huoqu_latest_reply.text and "thread_ts" not in url_conversations_replies_huoqu_latest_reply.text):
                web.header('Content-Type', 'text/event-stream')
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                web.header('Pragma', 'no-cache')
                return """data: {"id":"chatcmpl-75nIQFpIpwE3zjcpga0VGgULV3Lyh","object":"chat.completion.chunk","created":1681615490,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"%s"},"index":0,"finish_reason":null}]}


                            data: [DONE]

                            """ % ("错误")

            #print(url_conversations_replies_huoqu_latest_reply.text)
            if ("\"ok\":true" in url_conversations_replies_huoqu_latest_reply.text and "latest_reply" in url_conversations_replies_huoqu_latest_reply.text and "thread_ts" in url_conversations_replies_huoqu_latest_reply.text):

                url_conversations_replies_huoqu_latest_reply_json = json.loads(url_conversations_replies_huoqu_latest_reply.text)

                url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply = jsonpath.jsonpath(url_conversations_replies_huoqu_latest_reply_json, "$.messages[0].latest_reply")[0]

                #print("url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply:{}".format(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply))
                #print("url_post_postMessage_r_json_thread_ts:{}".format(url_post_postMessage_r_json_thread_ts))

                if(url_post_postMessage_r_json_thread_ts!=url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply and url_post_postMessage_r_json_thread_ts!=None):
                    #print(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply)
                    web.setcookie('latest_reply', '{}'.format(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply), 36000)
                    break

                elif(url_post_postMessage_r_json_thread_ts==None):
                    #print(url_post_postMessage_r_json_thread_ts)
                    web.setcookie('latest_reply',
                                  '{}'.format(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply),
                                  36000)
                    break
            else:
                time.sleep(0.2)
        # url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply = web.cookies().get('latest_reply')


        if(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply!=None):
            for i in range(120):
                try:
                    url_conversations_replies_file2 = {
                        'token': (None,
                                  token,
                                  None),
                        'channel': (None, '{}'.format(fangjian_id), None),
                        'ts': (None, '{}'.format(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply), None),
                        'inclusive': (None, 'ture', None),
                        'limit': (None, '28', None),
                        'oldest': (None, '{}'.format(url_conversations_replies_huoqu_latest_reply_json_messages_latest_reply), None),
                        '_x_reason': (None, 'history-api/fetchReplies', None),
                        '_x_mode': (None, 'online', None),
                        '_x_sonic': (None, 'true', None)
                    }
                    url_conversations_replies_r = requests.post(url_conversations_replies, headers=headers,
                                                            files=url_conversations_replies_file2, verify=False)
                except BaseException as e:
                    print("查询失败,正在重试")
                    print(e)
                    for o in range(100):
                        try:
                            url_conversations_replies_r = requests.post(url_conversations_replies, headers=headers,
                                                                        files=url_conversations_replies_file2,
                                                                        verify=False)
                            if url_conversations_replies_r.status_code == 200:
                                break
                        except BaseException as e:
                            print("再次查询子域名失败", o)
                            print(e)

                # print(url_conversations_replies_r.text)
                if(i>2 and "_Typing" not in url_conversations_replies_r.text and "thread_ts" not in url_conversations_replies_r.text):
                    web.header('Content-Type', 'text/event-stream')
                    web.header('Access-Control-Allow-Origin', '*')
                    web.header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                    web.header('Pragma', 'no-cache')
                    return """data: {"id":"chatcmpl-75nIQFpIpwE3zjcpga0VGgULV3Lyh","object":"chat.completion.chunk","created":1681615490,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"%s"},"index":0,"finish_reason":null}]}\n\n\ndata: [DONE]\n\n"""% ("错误")

                if ("\"ok\":true" in url_conversations_replies_r.text and "_Typing" not in url_conversations_replies_r.text and "thread_ts" in url_conversations_replies_r.text):
                    url_conversations_replies_r_json = json.loads(url_conversations_replies_r.text)
                    url_conversations_replies_r_json_text = jsonpath.jsonpath(url_conversations_replies_r_json, "$.messages[0].text")[0]

                    url_conversations_replies_r_json_text=html.unescape(url_conversations_replies_r_json_text).replace("\n","\\\\n").replace("\"","\\\"")

                    break
                else:
                    time.sleep(1)
            else:
                web.header('Content-Type', 'text/event-stream')
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                web.header('Pragma', 'no-cache')
                return """data: {"id":"chatcmpl-75nIQFpIpwE3zjcpga0VGgULV3Lyh","object":"chat.completion.chunk","created":1681615490,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"%s"},"index":0,"finish_reason":null}]}\n\n\ndata: [DONE]\n\n"""% ("错误")

            #print(url_conversations_replies_r_json_text)
            web.header('Content-Type', 'text/event-stream')
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
            web.header('Pragma', 'no-cache')
            return """data: {"id":"chatcmpl-75nIQFpIpwE3zjcpga0VGgULV3Lyh","object":"chat.completion.chunk","created":1681615490,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"%s"},"index":0,"finish_reason":null}]}\n\n\ndata: [DONE]\n\n"""%(url_conversations_replies_r_json_text)


if __name__ == "__main__":
    app.run()