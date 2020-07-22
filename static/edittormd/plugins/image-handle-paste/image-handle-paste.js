function initPasteDragImg(Editor) {
    var doc = document.getElementById(Editor.id);
    doc.addEventListener('paste', function (event) {
        var items = (event.clipboardData || window.clipboardData).items;
        var file = null;
        if (items && items.length) {
            // 搜索剪切板items
            for (var i = 0; i < items.length; i++) {
                if (items[i].type.indexOf('image') !== -1) {
                    file = items[i].getAsFile();
                    break;
                }
            }
        } else {
            alert('您的浏览器不支持复制粘贴图片，请更换浏览器重新尝试！');
            return;
        }
        if (file) {
            uploadImg(file, Editor);
        }

    });
    var dashboard = document.getElementById(Editor.id)
    dashboard.addEventListener("dragover", function (e) {
        e.preventDefault()
        e.stopPropagation()
    });
    dashboard.addEventListener("dragenter", function (e) {
        e.preventDefault();
        e.stopPropagation()
    });
    dashboard.addEventListener("drop", function (e) {
        e.preventDefault()
        e.stopPropagation()
        var files = this.files || e.dataTransfer.files;
        uploadImg(files[0], Editor);
    })
}

function uploadImg(file, Editor) {
    var formData = new FormData();
    var fileName = new Date().getTime() + "." + file.name.split(".").pop();
    console.log(file.name);
    let token = $('[name="csrfmiddlewaretoken"]').attr("value");
    formData.append('editormd-image-file', file, fileName);
    formData.append('csrfmiddlewaretoken', token);
    console.log(formData.get('editormd-image-file'));
    $.ajax({
        "type": 'POST',
        "url": Editor.settings.imageUploadURL,//获取我们配置的url
        "data": formData,
        "dateType": "json",
        "processData": false,
        "contentType": false,
        "mimeType": "multipart/form-data",
        success: function (ret) {
            var json = $.parseJSON(ret);

            if (json.success) {
                var url = json.url;
                Editor.insertValue("![图片alt](" + url + "#pic_center ''图片title'')");

            } else {
                alert("上传失败:"+json.message);
            }

        },
        error: function (err) {
            console.log('请求失败')
        }
    });
}

