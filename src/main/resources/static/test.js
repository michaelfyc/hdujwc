$(function () {
    temp.getNews();
});

var temp = {
    getNews: function () {
        var page = temp.getUrlParam("p");
        if (page == null) {
            page = 1;
        }
        $.ajax({
            url: '/section',
            type: 'get',
            data: {'section': 'together', 'page': page},
            success: function (data) {
                console.log("success");
                temp.insert(data);
            },
            error: function () {
                console.log("fail");
            }
        })
    },

    insert: function (data) {
        var str = "";
        //插入内容
        for (var i = 0; i < data.data.length; i++) {
            str += "<li><a style='padding-left:15px;' href='" + data.data[i].link + "'>" + data.data[i].title + "</a> <span class='time'>" + data.data[i].time + "</span></li>"
        }
        $('#news').html(str);
        $('.total_count').html("共" + data.count + "条 共" + data.totalPage + "页 现在是第" + data.pageNum + "页");
        temp.pagination(data);
    },

    getUrlParam: function (param) {
        var reg = new RegExp("(^|&)" + param + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
        var r = window.location.search.substr(1).match(reg);  //匹配目标参数
        if (r != null) {
            return unescape(r[2]);
        }
        return null; //返回参数值
    },

    pagination: function (data) {
        var p = parseInt(temp.getUrlParam("p"));
        if (isNaN(p)) {
            p = Number(1);
        }
        //准备工作

        var pagination = "<a class='disabled' href='/'>首页</a>";
        var last = "<a target='_self' href='/?p=" + data.totalPage + "'>末页</a>";
        var previousPage = "";
        var nextPage = "";

        //分页页码
        if (data.isFirstPage) {
            previousPage = "<a class='disabled' href='javascript:void(0)'>上一页</a>";
        } else {

            if (p == 2) {
                previousPage = "<a class='disabled' href='/'>上一页</a>";
            } else {
                previousPage = "<a class='disabled' href='/?p=" + parseInt(p - 1) + "'>上一页</a>";
            }
        }

        if (data.isLastPage) {
            nextPage = "<a target='_self' href='javascript:void(0)'>下一页</a>";
        } else {
            nextPage = "<a class='disabled' href='/?p=" + parseInt(p + 1) + "'>下一页</a>";
        }


        //开始插！

        pagination += previousPage;
        debugger;

        //总页数大于5页，加省略号，隐藏部分页数，只显示前后5页


        //SHIT代码，嵌套一堆if else, ”能用就行，有空优化“
        if (data.totalPage > 5) {
            for (var k = 1; k <= 5; k++) {
                if (k == p) {
                    pagination += "<a href='javascript:void(0)' style='background-color: #bbb;'>" + k + "</a>";
                } else {
                    //如果是第一页就不用/?p=1了
                    if (k == 1) pagination += "<a href='/'>1</a>";
                    else pagination += "<a href='/?p=" + k + "'>" + k + "</a>";
                }
            }
            pagination += "<a class='disabled'>...</a>";
            for (var m = data.totalPage - 5; m <= data.totalPage; m++) {
                if (m == p) {
                    pagination += "<a href='javascript:void(0)' style='background-color: #bbb;'>" + k + "</a>";
                } else {
                    pagination += "<a href='/?p=" + m + "'>" + m + "</a>";
                }
            }

        } else {
            for (var j = 1; j <= data.totalPage; j++) {
                if (j == p) {
                    pagination += "<a href='javascript:void(0)' style='background-color: #bbb;'>" + j + "</a>";
                } else {
                    if (j == 1) pagination += "<a href='/'>1</a>";
                    else pagination += "<a href='/?p=" + j + "'>" + j + "</a>";
                }
            }
        }
        //加上”下一页“和”末页"
        pagination += nextPage;
        pagination += last;
        $('.p_btns').append(pagination);
    }
};