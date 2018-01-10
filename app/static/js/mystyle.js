/**
 * Created by xuyong on 2018-01-05.
 */
$(function() {
    $('form').on('submit', function (event) {
        // 阻止元素发生默认的行为，此处用来阻止对表单的提交
        event.preventDefault();
        var formData = new FormData(this);
        // jQuery Ajax 上传文件，关键在于设置：processData 和 contentType
        $.ajax({
            type: 'POST',
            url: '/upload',
            cache: false,
            data: formData,
            // 告诉 jQuery 不要去处理发送的数据
            processData: false,
            // 告诉 jQuery 不要去设置 Content-Type 请求头
            // 因为这里是由 <form> 表单构造的 FormData 对象，且已经声明了属性 enctype="multipart/form-data"，所以设置为 false
            contentType: false
        }).done(function (res) {
            var data = res.toString();
            $.ajax({
                type: 'POST',
                url: '/input/'+ data,
                cache: false,
                data: formData,
                processData: false,
                contentType: false
            }).done(function (ret) {
                var res = JSON.parse(ret);
                if (res.errcode == 0) {
                    txt = '<h2>导入成功!</h2>\n本次新增' + res.result + '条数据';
                    window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.success);
                }
            });
        }).fail(function (res) {
            txt = '<h2>上传失败!</h2>';
            window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.error);
        });
    });
    var curRow = {};
    $('#tb_departments').bootstrapTable({
        url: '/searchall',         //请求后台的URL（*）
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        //detailView:true,            //详情展示
        showRefresh:true,           //刷新按钮
        pageNumber:1,                       //初始化加载第一页，默认第一页
        pageSize: 20,                       //每页的记录行数（*）
        pageList: [5, 10, 20, 50],            //可供选择的每页的行数（*）
        search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
        pagination:true,
        clickToSelect: true,                //是否启用点击选中行
        uniqueId: "name",
        showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
        cardView: false,                    //是否显示详细视图
        detailView: false,                  //是否显示父子表
        showColumns: true,                  //是否显示所有的列
        toolbar: "#toolbar",
        columns: [{
            checkbox: true
        }, {
            field: 'name',
            title: '姓名',
            sortable: true,
            width: "16%"
        }, {
            field: 'sex',
            title: '性别',
            width: "16%"
        }, {
            field: 'indate',
            title: '入职日期',
            sortable: true,
            width: "16%"
        }, {
            field: 'outdate',
            title: '转正日期',
            sortable: true,
            width: "16%"
        }, {
            field: 'other',
            title: '备注',
            width: "16%"
        }, {
            field: 'status',
            title: '是否提醒',
            width: "16%",
            formatter: function(value,row,index) {
                var aa = "";
                if(value == "0"){
                    var aa = '<span style="color:black">是</span>';
                }else if(value == "1"){
                    var aa = '<span style="color:red">否</span>';
                }else{
                    var aa = '<span style="color:red">未定义</span>'
                }
                return aa;
            }
        }]
    });
});
