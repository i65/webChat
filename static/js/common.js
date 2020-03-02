var showModal = function(msg='', url='', type='success') {
    if (type == 'success') {
        if (!msg) {
            msg = '操作成功'
        }
        $('#myModalBody').css('color','green')
    } else {
        if (!msg) {
            msg = '操作失败'
        }
        $('#myModalBody').css('color','red')
    }
    // 弹出框, 1.5秒后自动关闭
     $('#myModalBody').html(msg)
     $('#showModal').modal('show')

     if (timer != null) {clearTimeout(timer);timer=null;}
     var timer = setTimeout(function() {
        $('.small.modal').modal('hide')
        if (url) {
            window.location.href = url
        }
     }, 1600)
}
