$(function () {
     testEditor = editormd.markdownToHTML("editormd", {
        width: "100%",
        height: 'auto',
        delay: 550,
        previewTheme: "default",
        codeFold: true,
        emoji: true,
        taskList: true,
        toc: true,
        htmlDecode: "style,script,iframe|on*",
        tocContainer: "#custom-toc-container",
        tex: true,
        flowChart: true,
        sequenceDiagram: true,
        pluginPath: "{% static 'edittormd/plugins/' %}",
    });

    $('.click').click(function (e) {
        let token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $('.click').val('已赞');
        $('.click').attr('disabled', true);
        console.log(parseInt($('#editormd').attr('data-id')));
        $.ajax({
            url: '/blog/blog-click/',
            type: 'post',
            data: {
                "csrfmiddlewaretoken": token,
                'id': parseInt($('#editormd').attr('data-id'))
            },
            success: function (data) {
                bs4pop.notice('点赞成功', {type: data.flag ? 'success' : 'danger', position: 'topcenter'});

                $('.click_nums').text(parseInt($('.click_nums').text()) + 1);
            }
        });
    });

    $('.href-article-edit').click(function (e) {
        if ($('.slide-content-box').css('display') == 'block') {

            $(".href-article-edit").text('版权');
            $('.slide-content-box').css('display', 'none')
        } else {
            $('.slide-content-box').css('display', 'block');
            $(".href-article-edit").text('收起');
        }
    });

    function copyToClipboard(txt = '') {
        let iscopy = false;
        if (document) {
            let textArea = document.createElement('textarea');
            textArea.style.position = 'fixed';
            textArea.style.top = 0;
            textArea.style.left = 0;
            textArea.style.width = '2em';
            textArea.style.height = '2em';
            textArea.style.padding = 0;
            textArea.style.border = 'none';
            textArea.style.outline = 'none';
            textArea.style.boxShadow = 'none';
            textArea.style.background = 'transparent';
            textArea.value = txt;
            textArea.id = "hand";
            document.body.appendChild(textArea);
            textArea.select();

            try {
                document.execCommand('copy');
                iscopy = true;
            } catch (err) {
                console.log('不能使用这种方法复制内容' + err.toString());
            }
            document.body.removeChild(textArea);
        }
        return iscopy;
    }

    $('ol.linenums').mouseenter(function (e) {
        copyText = e.target.parentElement.innerText;
        var span = document.createElement('div');
        span.setAttribute('class', 'copy');
        span.textContent = '复制';

        e.target.parentElement.insertBefore(span, e.target.parentElement.firstChild);

        span.addEventListener('click', function () {
            is_copy = copyToClipboard(copyText);
            if (is_copy) {
                span.textContent = "复制成功";
            } else {
                span.textContent = "复制失败"
            }
        })
    });
    $('ol.linenums').mouseleave(function (e) {
        $('.copy').remove()
    });
    document.addEventListener("copy", function (e) {
        //取消默认事件，才能修改复制的值

        if (e.target.id != 'hand') {
            e.preventDefault();
        }
        add_1 = $('.creativecommons').text().trim().replace(/\s/g, "");
        add_2 = $('.article-source-link').text().trim().replace(/\s/g, "").substring(5);
        var copyTxt = `${window.getSelection(0).toString()}
            \n————————————————————\n` + add_1 + "\n原文链接：" + add_2;
        if (e.clipboardData) {
            e.clipboardData.setData('text/plain', copyTxt);
        } else if (window.clipboardData) {
            return window.clipboardData.setData("text", copyTxt);
        }
    });
    $('.content').focus(function () {
        $('.content').addClass('open');
    });
    $('.content').blur(function () {
        $('.content').removeClass('open');
    });

    $('.cancel').click(function () {
        $("#reply-title").show();
        $("#cancel_comment").hide();
        $("#id_parent_comment_id").val('');
        $("#commentform").appendTo($("#respond"));
        $('.content').attr('placeholder', '博主需要您的鼓励，才能有动力创作');
    });

// 提交评论
    $('#post_submit').click(function () {
        let token = $('[name="csrfmiddlewaretoken"]').attr("value");
        let content = $('.content').val();
        let parent_comment_id = $('.parent_comment_id').val();
        if (content == '') {
            bs4pop.notice('请填写内容呢~', {type: 'danger', position: 'topcenter'});

        } else {
            bs4pop.notice('正在提交...', {type: 'info', position: 'topcenter'});
            $.ajax({
                url: '/comment/post/',
                type: 'post',
                data: {
                    "csrfmiddlewaretoken": token,
                    'blog_id': parseInt($('#editormd').attr('data-id')),
                    'content': content,
                    'parent_comment_id': parent_comment_id ? parent_comment_id : 0,
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

        }
    });


});