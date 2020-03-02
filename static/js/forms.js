$(document).ready(function () {

    $.fn.api.settings.api = {
        'register_url': register_url,
        'login_url': login_url
    }
    // login form
    $('.login.ui.form')
        .form({
            fields: {
                username: {
                    identifier: 'username',
                    rules: [{
                        type: 'empty',
                        prompt: '请输入用户名'
                    }]
                },
                password: {
                    identifier: 'password',
                    rules: [{
                        type: 'empty',
                        prompt: '请输入密码'
                    },
                        {
                            type: 'minLength[6]',
                            prompt: '密码不能少于 6 个字符'
                        }
                    ]
                }
            }
        });

    $('.login.ui.form').api({
        action: 'login_url',
        method: 'POST',
        serializeForm: true,

        beforeXHR: function(xhr){
           xhr.setRequestHeader("X-CSRFToken", csrf_token )
           return xhr
        },
        onSuccess: function(data) {
            console.log(data)
            showModal(data.message, data.url, data.result)
        },
     })

    // register form
    $('.register.ui.form')
        .form({
            inline: true,
            fields: {
                realname: {
                    identifier: 'realname',
                    rules: [{
                        type: 'empty',
                        prompt: '请输入姓名'
                    },
                        {
                            type: 'maxLength[12]',
                            prompt: '姓名不能超过 {ruleValue} 个字符'
                        }
                    ]
                },
                username: {
                    identifier: 'username',
                    rules: [{
                        type: 'empty',
                        prompt: '请输入用户名'
                    },
                        {
                            type: 'maxLength[12]',
                            prompt: '用户名不能超过 {ruleValue} 个字符'
                        }
                    ]
                },
                password: {
                    identifier: 'password',
                    rules: [{
                        type: 'empty',
                        prompt: '请设置密码'
                    },
                        {
                            type: 'minLength[6]',
                            prompt: '密码不能少于 {ruleValue} 个字符'
                        },
                        {
                            type: 'maxLength[20]',
                            prompt: '密码不能超过 {ruleValue} 个字符'
                        }
                    ]
                },
                password2: {
                    identifier: 'password2',
                    rules: [{
                        type: 'empty',
                        prompt: '请输入验证密码'
                    },
                        {
                            type: 'minLength[6]',
                            prompt: '验证密码不能少于 {ruleValue} 个字符'
                        },
                        {
                            type: 'maxLength[20]',
                            prompt: '验证密码不能超过 {ruleValue} 个字符'
                        },
                        {
                            type: 'match[password]',
                            prompt: '两次密码输入不一致'
                        }
                    ]
                }
            },
//            onSuccess: function(event, fields) {
//                //阻止表单的提交
//                event.preventDefault();
//                console.log(event)
//                console.log(fields)
//            },
//            onValid: function(res) {
//                console.log('onvalide')
//                console.log(res)
//            },
//            onInvalid: function(res) {
//                console.log('onInvalid')
//                console.log(res)
//            },
//            onFailure: function(error, fields) {
//                console.log(error)
//                console.log(fields)
//            }
//        }).api({
//            action: 'register_url',
//            method: 'POST',
//            serializeForm: true,
//
//            beforeXHR: function(xhr){
//               xhr.setRequestHeader("X-CSRFToken", csrf_token )
//               return xhr
//            },
//
//            beforeSend: function(settings) {
//                console.log('settings:')
//                console.log(settings)
//                console.log($(this).data('realname'))
//                return settings
//            }
        })

    $('.register.ui.form').api({
        action: 'register_url',
        method: 'POST',
        serializeForm: true,

        beforeXHR: function(xhr){
           xhr.setRequestHeader("X-CSRFToken", csrf_token )
           return xhr
        },
        onSuccess: function(data) {
            console.log(data)
            showModal(data.message, data.url, data.result)
        },
     })


});
