$('.del-all').click(function (e) {
    bs4pop.confirm('你确定删除所有通知吗？', function (sure) {
        console.log('操作结果', sure, e.target.id);
        let token = $('[name="csrfmiddlewaretoken"]').attr("value");
        if (sure) {

            $.ajax({
                url: '/message/update/',
                type: 'post',
                data: {
                    "csrfmiddlewaretoken": token,
                },
                success: function (data) {
                    bs4pop.notice(data.msg, {type: data.flag ? 'success' : 'danger', position: 'topcenter'});

                    if (data.flag) {
                        setTimeout(function () {
                            window.location.reload()
                        }, 1000)
                    }
                }
            });
        } else {

        }
    }, {
        title: '删除提示',
        hideRemove: true,
    });

});

$('.del').click(function (e) {
    let token = $('[name="csrfmiddlewaretoken"]').attr("value");
    $.ajax({
        url: '/message/update/',
        type: 'post',
        data: {
            "msg_id": e.target.id,
            "csrfmiddlewaretoken": token,
        },
        success: function (data) {
            bs4pop.notice(data.msg, {type: data.flag ? 'success' : 'danger', position: 'topcenter'});
            if (data.flag) {
                setTimeout(function () {
                    window.location.reload()
                }, 1000)
            }
        }
    });
});