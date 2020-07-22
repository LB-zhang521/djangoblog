var Code = new GVerify({
    id: "picyzm",
    type: "blend"
});
let i = $('#nextBtn').index();
$(function () {

    $('#nextBtn').click(function () {
        var username = $('.username').val();
        var email = $('.email').val();
        var passwd = $('.passwd').val();
        var passwd2 = $('.passwd2').val();
        var verifyCode = $('.verifyCode').val();
        var EmailReg = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
        var UserName = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$/;
        if (username == '') {
            bs4pop.notice('请填写用户名', {type: 'danger', position: 'topcenter'})

        } else if (!UserName.test(username)) {
            bs4pop.notice('用户名必须数字组合6-16位哦~', {type: 'danger', position: 'topcenter'})
        } else if (email == '') {
            bs4pop.notice('请填写您的邮箱', {type: 'danger', position: 'topcenter'})
        } else if (!EmailReg.test(email)) {
            bs4pop.notice('您的邮箱格式错咯', {type: 'danger', position: 'topcenter'})
        } else if (passwd == '') {
            bs4pop.notice('请填写您的密码', {type: 'danger', position: 'topcenter'})
        } else if (passwd2 == '') {
            bs4pop.notice('请再次输入您的密码', {type: 'danger', position: 'topcenter'})

        } else if (passwd != passwd2 || passwd2 != passwd) {
            bs4pop.notice('两次密码输入不一致呢', {type: 'danger', position: 'topcenter'})
        } else if (verifyCode == '') {
            bs4pop.notice('请输入验证码', {type: 'danger', position: 'topcenter'})
        } else if (!Code.validate(verifyCode)) {
            bs4pop.notice('验证码不正确', {type: 'danger', position: 'topcenter'});
            Code.refresh()
        } else {
            bs4pop.notice("正在提交...", {type: 'info', position: 'topcenter'});
            let token = $('[name="csrfmiddlewaretoken"]').attr("value");
            $.ajax({
                url: '/accounts/reg/',
                type: 'post',
                data: {
                    "username": username,
                    "password": passwd,
                    "email": email,
                    "csrfmiddlewaretoken": token
                },
                success: function (data) {
                    bs4pop.notice(data.msg, {type: data.flag ? 'success' : 'danger', position: 'topcenter'});
                    if (data.flag) {
                        i++;
                        $('.processorBox li').removeClass('current').eq(i).addClass('current');
                        $('.step').fadeOut(300).eq(i).fadeIn(500);
                        $('.zc_username').text(username);
                        $('.zc_email').text(email);
                        email_state();
                    }
                }
            });
        }
    });
});

function email_state() {
    settime(this);
    let token = $('[name="csrfmiddlewaretoken"]').attr("value");
    $.ajax({
        url: '/accounts/email_result/',
        type: 'post',
        data: {
            "email": $('.email').val(),
            "csrfmiddlewaretoken": token,
            'email_type': "reg"
        },
        success: function (data) {
            bs4pop.notice(data.msg, {type: data.flag ? 'success' : 'danger', position: 'topcenter'});
        }
    });
}

var countdown = 30;

function settime(obj) {

    if (countdown == 0) {
        $(obj).on('click', email_state);
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

$('#re_email').on('click', email_state);
