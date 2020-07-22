$(function () {
    let token = $('[name="csrfmiddlewaretoken"]').attr("value");
    $('.login').click(function () {
        var username = $("#username").val();
        var password = $("#password").val();

        if (username == '' || password == '')
            bs4pop.notice('请填写用户名及密码', {type: 'danger', position: 'topcenter'});
        else {
            bs4pop.notice('正在登录...', {type: 'info', position: 'topcenter'});
            $.ajax({
                url: '/accounts/login/',
                type: 'post',
                data: {
                    "username": username,
                    "password": password,
                    "csrfmiddlewaretoken": token
                },

                success: function (data) {
                    bs4pop.notice(data.msg, {type: data.flag ? 'success' : 'danger', position: 'topcenter'});
                    if (data.flag) {
                        window.location.reload();
                    }else {
                        $("#password").val('');
                    }
                },
                error: function () {
                    bs4pop.notice('网络异常，请刷新页面重试', {type: 'info', position: 'topcenter'});
                }
            });

        }

    });


    var countdown = 30;

    function send_yzm() {
        let flag = email_active();
        if (flag) {
            settime(this);
            var email_type = "password_reset";
            var email = $('#email').val();
            $.ajax({
                url: '/accounts/email_result/',
                type: 'post',
                data: {
                    "email_type": email_type,
                    "csrfmiddlewaretoken": token,
                    "email": email
                },
                success: function (data) {
                    bs4pop.notice(data.msg, {type: data.flag ? 'success' : 'danger', position: 'topcenter'});
                    if (data.flag) {
                        location.reload();
                    }
                },
                error: function () {
                    bs4pop.notice('网络异常，请刷新页面重试', {type: 'info', position: 'topcenter'});
                }
            });
        }

    }

    function settime(obj) {

        if (countdown == 0) {
            $(obj).on('click', send_yzm);
            $(obj).text("获取验证码");
            countdown += 60;
            return;
        } else {
            $(obj).off('click');
            $(obj).text(countdown + "s后重新获取邮件");
            countdown--;
        }
        setTimeout(function () {
            settime(obj);
        }, 1000);
    }

    function email_active() {
        var email = $('#email').val();
        var EmailReg = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
        flag = false;
        if (email == "") {
            bs4pop.notice("请填写注册邮箱呢~", {type: 'danger', position: 'topcenter'});
        } else if (!EmailReg.test(email)) {
            bs4pop.notice("注册邮箱格式不对呢~", {type: 'danger', position: 'topcenter'});
        } else {
            flag = true
        }
        return flag
    }

    $('.send_reset_password_yzm').on('click', send_yzm);

    $('.reset_password').click(function () {
        let password = $('#new_pwd').val();
        let re_password = $('#re_new_pwd').val();
        let email = $('#email').val();
        let yzm = $('#yzm').val();
        let flag = email_active();
        if (flag) {
            if (password == "") {
                bs4pop.notice("请您填写表单呢~", {type: 'danger', position: 'topcenter'});
            } else if (password != re_password) {
                bs4pop.notice("两次密码输入不一样呢~", {type: 'danger', position: 'topcenter'});
            } else if (yzm.length != 6) {
                bs4pop.notice("验证码位数不够呢~", {type: 'danger', position: 'topcenter'});
            } else {
                bs4pop.notice("正在提交...", {type: 'success', position: 'topcenter'});
                $.ajax({
                    url: '/accounts/reset_password/',
                    type: 'post',
                    data: {
                        "email": email,
                        "yzm": yzm,
                        'password': password,
                        "csrfmiddlewaretoken": token
                    },
                    success: function (data) {
                        bs4pop.notice(data.msg, {
                            type: data.flag ? 'success' : 'danger',
                            position: 'topcenter'

                        });
                        if (data.flag) {
                            window.location.reload();
                        }
                    },
                    error: function () {
                        bs4pop.notice('网络异常，请刷新页面重试', {type: 'info', position: 'topcenter'});
                    }
                });
            }
        }
    });
    
});
