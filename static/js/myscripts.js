$(document).ready(function () {
     var socket = io();

      var popupLoading = '<i class="notched circle loading icon green"></i> Loading...';
      var message_count = 0;
      // 回车键键值
      var ENTER_KEY = 13;

     socket.on('new message', function (data) {
        console.log('new_message：', data)
        if (!data.flag) {
            showModal('不能给自己留言', '', 'fail')
            return
        }
        // 未读消息提示
        message_count++;
        if (!document.hasFocus()) {
            document.title = '(' + message_count + ') ' + 'web聊天室';
        }
        // 加载消息列表
//        $('.messages_list').append(data.message_html);
        msg = renderMsg(data)
        $('.messages_list').append(msg);
        // 滚动条滚动到底部
        scrollToBottom();
    });

    // 点击 "发送" 按钮发送消息
    $('#send-button').on('click', function () {
        sendMsg()
    });
    // 点击回车发送消息
    $('#message-input').on('keypress', function(event) {
        if (event.keyCode == ENTER_KEY) {
            sendMsg()
        }
    })

    var sendMsg = function() {
        $msg_input = $('#message-input')
        var message = $msg_input.val();
        // 接收者 ID
        var to_id = $('#message_to').attr('data-id') | 0
        // 发送者 ID
        var user_id = $('.menu-item').data('id')
        if (to_id == user_id) {
            $('#message_to').val('')
            $('#message_to').attr('data-id', '')
            showModal('不能给自己留言', '', 'fail')
            return
        }
        // 消息正文
        message_body = {'data': message, 'id': to_id}
        if (message.trim() !== '') {
            // 发送到 new message 事件中
            socket.emit('new message', message_body);
//            flask_moment_render_all();
            // 清空输入框
            $msg_input.val('')
            $('#message_to').val('')
            $('#message_to').attr('data-id', '')
        }
    }

    // 选中用户名，要发送给谁
//    $('.m-user .item.logined').on('click', function(e) {
//        selectReceiver($(this))
//    })

    // js加载的用户列表需要用下面的函数才可以选择接收者
    $('.m-user').delegate('.item.logined', 'click', function(e) {
        console.log('click: ', $(this))
        selectReceiver($(this))
    })
    // 选中消息者
    var selectReceiver = function(obj) {
        var username = obj.data('username')
        var id = obj.data('id')

        $('#message_to').val(username)
        $('#message_to').attr('data-id', id)
    }
    // 更新消息列表， msg_text为 监听 new message 事件的返回数据
    var renderMsg = function(msg_text) {
        var user_id = $('.menu-item').data('id')
        var float_class = ''
        var point_class = 'left'
        var html_text = ''
        html_text += '<div class="item m-dialoge"><div class="content">'

        //console.log('msg_text: ', msg_text)
        if (msg_text.user_id == user_id) {
            float_class = 'right floated'
            point_class = 'right'
        }

            html_text += '<div class="item-author item ' + float_class + '">'
        if (msg_text.to_user_id) {
                    html_text += '<a class=""><i class="user icon"></i>' + msg_text.username + '</a> 对'
                    html_text += '<a class=""><i class="user outline icon"></i>' + msg_text.to_username + '</a>'
                    html_text += '<em style="color:green">说：</em>'
        } else {
                    html_text += '<a class=""><i class="user icon"></i>' + msg_text.username + '</a>'
        }
            html_text += '</div>'
            html_text += '<div class="m-message ui ' + point_class + ' pointing teal basic label">' + msg_text.message_body + '</div>'
        html_text += '   </div></div>'
        return html_text
    }
    function scrollToBottom() {
        var $messages = $('.m-content');
        $messages.scrollTop($messages[0].scrollHeight);
    }

    // 更新用户列表
    var renderUser = function(user) {
        var user_str = ''
        user_str += '<div class="item logined" data-id="' + user.id + '" data-username="' + user.username + '">'
        user_str += '<i class="ui user circle outline icon m-user-icon"></i>'
        user_str += '<div class="content">'
        user_str += '<a class="header"><i class="icon lightbulb"></i>' + user.username + '</a></div></div>'
        return user_str
    }

    // 加载页码数
    var page = 1;
    // 是否全部加载完毕
    var is_load_finished = false
    function load_messages() {
        var $messages = $('.m-content');
        var position = $messages.scrollTop();
        if (is_load_finished) {
            $('.ui.text.loader').html('消息加载完毕')
            $('.ui.loader').toggleClass('active');
            $('.ui.loader').toggleClass('active');
            return
        }
        if (position === 0) {
            page++;
            $('.ui.loader').toggleClass('active');
            $.ajax({
                url: messages_url,
                type: 'GET',
                data: {page: page},
                success: function (data) {
                    var before_height = $messages[0].scrollHeight;
                    $(data).prependTo(".messages_list").hide().fadeIn(800);
                    var after_height = $messages[0].scrollHeight;
                    flask_moment_render_all();
                    $messages.scrollTop(after_height - before_height);
                    $('.ui.loader').toggleClass('active');
//                    activateSemantics();
                },
                error: function () {
                    is_load_finished = true
                    $('.ui.loader').html('消息加载完毕')
                    $('.ui.loader').toggleClass('active');
                }
            });
        }
    }

    $('.m-content').scroll(load_messages);


    // 监听连接事件
    socket.on('user_connect', function (data) {
        console.log('user_connect：', data)
        // 更新用户在线人数
        $('#user-count').html(data.count);
        // 更新在线用户列表
        $('.m-user').html(data.user_html);
//        user = renderUser(data)
//        $('.m-user').append(user)
    });
    // 监听断开事件
    socket.on('user_disconnect', function (data) {
        console.log('user_disconnect：', data)
        // 更新用户在线人数
        $('#user-count').html(data.count);
        // 更新在线用户列表
        $('.m-user').html(data.user_html);
//        user = renderUser(data)
//        $('.m-user').append(user)
    });


    function init() {
        $(window).focus(function () {
            message_count = 0;
            document.title = '首页 - web聊天室 ';
        });
        scrollToBottom();

    }

    init();

//     id = $('.menu-item').data('id')
//    data = {'id': id, 'username': login_user}
//    socket.emit('my_connect_event', data)
//
//     socket.emit("message", { "data": "zhangsan" })
//     socket.on('connect', function (data) {
//        socket.emit('message', { 'data': 'I\'m connected!' });
//     });
//
//     socket.on('disconnect', function(data){
//        socket.emit('message', { 'data': 'I\'m disconnected!' });
//     });
//
//    socket.on('response', function (data) {
//        console.log(data.age)
//    });


    $('#logout').click(function(){
        $('#myConfirmModal').html('你确定退出登录吗？')
        $('#confirmModal').modal({
              closable  : true,
              onApprove : function() {
                    $.ajax({
                    url: logout_url,
                    data:  '',
                    success: function(data) {
                        console.log('成功退出登录')
                        if (data.result == 'success') {
                            socket.disconnect()
                            window.location.href = data.url
                        }
                    }
                })
              }
        }).modal('show')
    })

});
