//去除缓存
$(function(){
    $('img,script').each(function(){
        var url = $(this).attr('src');
        if(url != undefined){
            var rand;
            if(url.indexOf('?') == -1){
                rand = '?rand='+Math.random();
            }else{
                rand = '&rand='+Math.random();
            }
            $(this).attr('src',url+rand);
        }
    })
});
add_rand();
function add0(m){return m<10?'0'+m:m }
function format(timestamp)
{
    //timestamp是整数，否则要parseInt转换,不会出现少个0的情况
    var time = new Date(timestamp);
    //计算天数
    var days=Math.floor(time/(24*3600*1000));//总共小时数
    //计算出小时数
    var leave1=time%(24*3600*1000);    //计算天数后剩余的毫秒数
    var hours=Math.floor(leave1/(3600*1000));//总共小时数
    //计算相差分钟数
    var leave2=leave1%(3600*1000);       //计算小时数后剩余的毫秒数
    var minutes=Math.floor(leave2/(60*1000));
    //计算相差秒数
    var leave3=leave2%(60*1000);
    //计算分钟数后剩余的毫秒数
    var seconds=Math.round(leave3/1000);
    return add0(days)+'d '+add0(hours)+'h '+add0(minutes)+'m '+add0(seconds)+'s';
}
function selectHtml(minername){
   // var minername = getMinerNameValue();
    if(minername == 16)//chenchunxu
    {
        //$(".pool_div:eq(0) input").eq(0).attr("readonly","readonly").css("color","#BDBDBD");
        $('.pool1_select').html('<select name="Pool1" class="layui-input" style="width:90%"><option>stratum+tcp://dbg.stratum.slushpool.com:3335</option><option>stratum+tcp://btc-sz.s.innpool.com:1800</option><option>stratum+tcp://btc-va.s.innpool.com:1800</option></select>');

        $(".pool_div:eq(1),.pool_div:eq(2),.pool_div:eq(3)").remove();
        $(".Frequency-tipcon-Frequency .tip1,.Frequency-tipcon-Voltage .tip3").text('1332');
        $(".Frequency-tipcon-Frequency .tip2,.Frequency-tipcon-Voltage .tip2").text('13 to 8');
        $(".Frequency-tipcon-Voltage .tip1").text('10');
        var fselect = '<option value="1308">1308</option>' +
            '<option value="1320">1320</option>' +
            '<option value="1332" selected="">1332 (default)</option>' +
            '<option value="1344">1344 (overclock)</option>' +
            '<option value="1356">1356 (overclock)</option>';
        var vselect = '<option value="13">13</option>' +
            '<option value="12">12</option>' +
            '<option value="11">11</option>' +
            '<option value="10" selected="">10 (default)</option>' +
            '<option value="9">9</option>'+
            '<option value="8">8</option>';
    }else if(minername == 17){//huwentao
        //default
        $(".Frequency-tipcon-Frequency .tip1,.Frequency-tipcon-Voltage .tip3").text('1152');
        $(".Frequency-tipcon-Frequency .tip2,.Frequency-tipcon-Voltage .tip2").text('27 to 13');
        $(".Frequency-tipcon-Voltage .tip1").text('14');
        var defaultVID = getcookie('defaultVID');
        if(defaultVID){
            $(".Frequency-tipcon-Voltage .tip1").text(defaultVID);
            $('select[name=Voltage]').val(defaultVID);
        }else{
            selftestone();
        }
        var fselect = '<option value="1044">1044 (high efficient)</option>' +
            '<option value="1100">1100</option>' +
            '<option value="1152" selected="">1152 (high hashrate)</option>';
        var vselect = '<option value="27">27</option>' +
            '<option value="26">26</option>' +
            '<option value="25">25 (efficient)</option>' +
            '<option value="24">24</option>' +
            '<option value="23">23</option>' +
            '<option value="22">22</option>' +
            '<option value="21">21</option>' +
            '<option value="20">20</option>' +
            '<option value="19">19</option>' +
            '<option value="18">18</option>' +
            '<option value="17">17</option>' +
            '<option value="16">16</option>' +
            '<option value="15">15</option>' +
            '<option value="14" selected="">14 (default)</option>'+
            '<option value="13">13</option>' ;
    }else if(minername == 18){//sunjiwen
        //default
        $(".Frequency-tipcon-Frequency .tip1,.Frequency-tipcon-Voltage .tip3").text('1100');
        $(".Frequency-tipcon-Frequency .tip2,.Frequency-tipcon-Voltage .tip2").text('14 to 10');
        $(".Frequency-tipcon-Voltage .tip1").text('12');
        var defaultVID = getcookie('defaultVID');
        if(defaultVID){
            $(".Frequency-tipcon-Voltage .tip1").text(defaultVID);
            $('select[name=Voltage]').val(defaultVID);
        }else{
            selftestone();
        }
        var fselect = '<option value="1000">1000</option>' +
            '<option value="1050">1050</option>' +
            '<option value="1100" selected="">1100 (default)</option>' +
            '<option value="1130">1130 (overclock)</option>' +
            '<option value="1160">1160 (overclock)</option>' +
            '<option value="1200">1200 (overclock)</option>';
        var vselect = '<option value="14">14</option>' +
            '<option value="13">13</option>' +
            '<option value="12" selected="selected">12 (default)</option>' +
            '<option value="11">11</option>' +
            '<option value="10">10</option>';
    }else if(minername == 19){//wangpeng
        $(".pool_div:eq(2),.pool_div:eq(3)").remove();

        $(".Frequency-tipcon-Frequency .tip1,.Frequency-tipcon-Voltage .tip3").text('1000');
        $(".Frequency-tipcon-Frequency .tip2,.Frequency-tipcon-Voltage .tip2").text('175 to 150');
        $(".Frequency-tipcon-Voltage .tip1").text('175');
        var fselect = '<option value="800">800</option>' +
            '<option value="850">850</option>' +
            '<option value="900">900</option>' +
            '<option value="950">950</option>' +
            '<option value="1000" selected="">1000 (default)</option>' +
            '<option value="1100">1100 (overclock)</option>';
        var vselect = '<option value="175" selected="">175 (default)</option>' +
            '<option value="170">170</option>' +
            '<option value="165">165</option>' +
            '<option value="160">160</option>' +
            '<option value="155">155</option>' +
            '<option value="150">150</option>';
        var html='<table class="contable p30-x" width="100%"><tr><td width="45%">typically users don\'t need to adjust software automatically controls it</td><td width="55%"></td></tr></table>';
        //$('.FANSetup').append(html).show();
    }
    $('select[name=Frequency]').html(fselect);
    $('select[name=Voltage]').html(vselect);
}
function pooltype(num){
    var Pool = $('[name=Pool'+num+'] option:selected').val();
    if(num == 1){
        if(Pool == 'pool1'){
            $('select[name=Pool2]').val('pool2');
            $('.UserName2').html('<select name="UserName2" class="layui-input" style="width:90%"><option selected="selected">worker1</option><option>worker2</option></select>');
            $('.UserName1').html('<input name="UserName1" value="inno19.0001" class="layui-input" style="width:90%" type="text">');
        }else{
            $('select[name=Pool2]').val('pool1');
            $('.UserName1').html('<select name="UserName1" class="layui-input" style="width:90%"><option selected="selected">worker1</option><option>worker2</option></select>');
            $('.UserName2').html('<input name="UserName2" value="inno19.0001" class="layui-input" style="width:90%" type="text">');
        }
    }else if(num == 2){
        if(Pool == 'pool1'){
            $('select[name=Pool1]').val('pool2');
            $('.UserName1').html('<select name="UserName1" class="layui-input" style="width:90%"><option selected="selected">worker1</option><option>worker2</option></select>');
            $('.UserName2').html('<input name="UserName2" value="inno19.0001" class="layui-input" style="width:90%" type="text">');
        }else{
            $('select[name=Pool1]').val('pool1');
            $('.UserName2').html('<select name="UserName2" class="layui-input" style="width:90%"><option selected="selected">worker1</option><option>worker2</option></select>');
            $('.UserName1').html('<input name="UserName1" value="inno19.0001" class="layui-input" style="width:90%" type="text">');
        }
    }
    $.ajax({
        url: '/conf/miner.conf',
        type: "GET",
        cache: false,
        data: '',
        dataType: "json",
        success:function(data){
            //if(num == 1) {
            //    if (Pool == 'pool1') {
            //        $('[name=UserName1]').val(data.UserName1).attr('title',data.UserName1);
            //    }
            //}else if(num == 2){
            //    if (Pool == 'pool1') {
            //        $('[name=UserName2]').val(data.UserName2).attr('title',data.UserName2);
            //    }
            //}
            if(!$('[name=Password1]').val()){
                $('input[name=Password1]').val('x').attr('title','x');
            }
            if(!$('[name=Password2]').val()){
                $('input[name=Password2]').val('x').attr('title','x');
            }
        }
    });
}
function selectHtmlOption(minername){
    //var minername = getMinerNameValue();
    if(minername == 16)//chenchunxu
    {
        //default
        $(".Frequency-tipcon-Frequency .tip1,.Frequency-tipcon-Voltage .tip3").text('1332');
        $(".Frequency-tipcon-Frequency .tip2,.Frequency-tipcon-Voltage .tip2").text('13 to 8');
        $(".Frequency-tipcon-Voltage .tip1").text('10');
    }else if(minername == 17){//huwentao
        //default
        $(".Frequency-tipcon-Frequency .tip1,.Frequency-tipcon-Voltage .tip3").text('1152');
        $(".Frequency-tipcon-Frequency .tip2,.Frequency-tipcon-Voltage .tip2").text('27 to 13');
        $(".Frequency-tipcon-Voltage .tip1").text('14');
        var defaultVID = getcookie('defaultVID');
        if(defaultVID){
            $(".Frequency-tipcon-Voltage .tip1").text(defaultVID);
        }else{
            selftestone();
        }
    }else if(minername == 18){//sunjiwen
        //default
        $(".Frequency-tipcon-Frequency .tip1,.Frequency-tipcon-Voltage .tip3").text('1100');
        $(".Frequency-tipcon-Frequency .tip2,.Frequency-tipcon-Voltage .tip2").text('14 to 10');
        $(".Frequency-tipcon-Voltage .tip1").text('12');
        var defaultVID = getcookie('defaultVID');
        if(defaultVID){
            $(".Frequency-tipcon-Voltage .tip1").text(defaultVID);
        }else{
            selftestone();
        }
    }else if(minername == 19){//wangpeng
        //default
        $(".Frequency-tipcon-Frequency .tip1,.Frequency-tipcon-Voltage .tip3").text('1000');
        $(".Frequency-tipcon-Frequency .tip2,.Frequency-tipcon-Voltage .tip2").text('175 to 150');
        $(".Frequency-tipcon-Voltage .tip1").text('175');
        var html='<table class="contable p30-x" width="100%"><tr><td width="45%">typically users don\'t need to adjust software automatically controls it</td><td width="55%"><div class="setup1"><select name="speed" class="layui-input w100 layui-disabled" disabled><option>0</option><option>1</option><option>2</option><option selected="">3</option><option>4</option><option>5</option></select></div></td></tr></table>';
        //$('.FANSetup').append(html).show();
    }
}
$('#file').click(function(){
    return $('input[name=file]').click();
});
function handleFile(t){
    $('input[name=fileName]').val($(t).val());
}
$(".nav li").mouseover(function() {
    var index = $(this).index();
    $(this).siblings().removeClass('navhover');
    $(this).addClass('navhover');
    $(".navchild").hide();
    $(".nav" + index).show();
});
$(".navchild li").click(function() {
    $(".navchild li").removeClass('navhover');
    $(this).addClass('navhover');
});

$(".nav li").click(function() {
    var index = $(this).index();
    $(".navchild li").removeClass('navhover');
    $(".nav" + index + ' li').eq(0).addClass('navhover');
});
//top.html end

$(".nav li").mouseover(function() {
    var index = $(this).index();
    $(this).siblings().removeClass('navhover');
    $(this).addClass('navhover');
    $(".navchild").hide();
    $(".nav" + index).show();
});
$(".navchild li").click(function() {
    $(".navchild li").removeClass('navhover');
    $(this).addClass('navhover');
});
function getMinerNameValue(){
    var minername;
    $.ajax({
        url: '/cgi-bin/type.py',
        type: "POST",
        async:false,
        data: '',
        dataType: "json",
        success:function(data){
            minername = data.type;
        }
    });
    return minername;
}
function sendAjax(json,url){
    $.ajax({
        type: "POST",
        url: url,
        data: json,
        dataType: "json",
        success: function(form) {
            console.log(form);
            return form;
        },error:function(){
            return false;
        }
    });
}
function getcookie(name) {
    var cookie_start = document.cookie.indexOf(name);
    var cookie_end = document.cookie.indexOf(";", cookie_start);
    return cookie_start == -1 ? '' : unescape(document.cookie.substring(cookie_start + name.length + 1, (cookie_end > cookie_start ? cookie_end : document.cookie.length)));
}
function setcookie(cookieName, cookieValue, seconds, path, domain, secure) {
    seconds = seconds ? seconds : 24*60*60*1000;//默认保存一天
    var expires = new Date();
    expires.setTime(expires.getTime() + seconds);
    document.cookie = escape(cookieName) + '=' + escape(cookieValue)

        + (expires ? '; expires=' + expires.toGMTString() : '')
        + (path ? '; path=' + path : '/')
        + (domain ? '; domain=' + domain : '')
        + (secure ? '; secure' : '');
}
function delcookie(name)
{
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval=getcookie(name);
    if(cval!=null)
        document.cookie= name + "="+cval+";expires="+exp.toGMTString();
}

function ResetDefault(){
    $.ajax({
        type: "POST",
        url: 'cgi-bin/resetdefault.py',
        data: '',
        dataType: "json",
        beforeSend:function(json) {
            layer.load();
        },
        success: function(json) {
            layer.closeAll('loading');
            if(json.result == true){
                layer.msg('ResetDefault success');
            }else{
                layer.msg('fail');
            }
        },error:function(){
            layer.closeAll('loading');
            layer.msg('error');
        }
    });
}
//校验ip
function isValidIP(ip) {
    var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    return reg.test(ip);
}
//子网掩码
function checkMask(mask)
{
    obj=mask;
    var exp=/^(254|252|248|240|224|192|128|0)\.0\.0\.0|255\.(254|252|248|240|224|192|128|0)\.0\.0|255\.255\.(254|252|248|240|224|192|128|0)\.0|255\.255\.255\.(254|252|248|240|224|192|128|0)$/;
    var reg = obj.match(exp);
    if(reg==null)
    {
        return false; //"非法"
    }
    else
    {
        return true; //"合法"
    }
}
//网关的合法性
function checkNet(static_ip,static_mask,static_gw){
    if(static_ip == static_mask || static_ip == static_gw  || static_mask == static_gw)
    {
        return false; //IP地址与子网掩码、网关地址不能相同
    }
    var static_ip_arr = new Array;
    var static_mask_arr = new Array;
    var static_gw_arr = new Array;

    static_ip_arr = static_ip.split(".");
    static_mask_arr = static_mask.split(".");
    static_gw_arr = static_gw.split(".");

    var res0 = parseInt(static_ip_arr[0]) & parseInt(static_mask_arr[0]);
    var res1 = parseInt(static_ip_arr[1]) & parseInt(static_mask_arr[1]);
    var res2 = parseInt(static_ip_arr[2]) & parseInt(static_mask_arr[2]);
    var res3 = parseInt(static_ip_arr[3]) & parseInt(static_mask_arr[3]);

    var res0_gw = parseInt(static_gw_arr[0]) & parseInt(static_mask_arr[0]);
    var res1_gw = parseInt(static_gw_arr[1]) & parseInt(static_mask_arr[1]);
    var res2_gw = parseInt(static_gw_arr[2]) & parseInt(static_mask_arr[2]);
    var res3_gw = parseInt(static_gw_arr[3]) & parseInt(static_mask_arr[3]);

    if(res0==res0_gw && res1==res1_gw && res2==res2_gw  && res3==res3_gw)
    {
        return true; //"合法"
    }
    else
    {
        return false; //IP地址与子网掩码、网关地址不匹配
    }
}
//
function checkDNS(dns) {
    var reg = /^[0-9a-zA-Z_-]+(\\.[0-9a-zA-Z_-]+)*(\\.[a-zA-Z]{2,}\\.)$/;
    return reg.test(dns);
}
//回车事件
$(function(){
    document.onkeydown = function(e){
        var ev = document.all ? window.event : e;
        if(ev.keyCode==13){
            $('.enterclick').click();
        }
    }
})
function getQueryString(name){
    var reg = new RegExp("(^|&)"+ name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if(r!=null)return unescape(r[2]);return null;
}
function debug(){
    layui.use('layer',function(){
        var layer = layui.layer;
        var log_data = "";
        //for (var i = 0; i <= 9; i++)
        //{
            $.ajax({
               // url: '../conf/analys'+i+'.log',
	        url:'/cgi-bin/showdebug.py',
                type: "GET",
                cache: false,
                data: '',
                dataType: "json",
                async:false,
                beforeSend:function()
                {
                    layer.load();
                },
                success:function(data)
                {
                    if(data.result == 'true')
                    {
                        log_data+=data.data;
                    }
                }
            });
       //}
        //分割为html代码-start
        var html = "<div><table style='width:100%'>";
        var html_data = log_data.split(/\r\n|\n/);
        $.each(html_data,function(index,data)
        {
            if(data.substr(0,1) == "+")
            {
                html += "<tr><td style='padding-right:15px;'>"+data.substr(0,1)+"</td><td>"+data.substr(1).replace(/ /g,"&nbsp;").replace(/\t/g,"&nbsp;&nbsp;&nbsp;&nbsp;")+"</td></tr>";
            }
            else
            {
                html += "<tr style='background-color:red'><td style='padding-right:15px;'>"+data.substr(0,1)+"</td><td>"+data.substr(1).replace(/ /g,"&nbsp;").replace(/\t/g,"&nbsp;&nbsp;&nbsp;&nbsp;")+"</td></tr>";
            }
        });
        html += "</table></div>";
        //end
        layer.closeAll('loading');
        layer.open({
            type: 1,
            skin: 'layui-layer-rim', //加上边框
            area: ['500px', '500px'], //宽高
            content: html
        });
    });
}
function add_rand()
{
    $('a').each(function()
    {
        rand = Math.random();
        href = $(this).attr('href');
        if (href.length == 0 || href.indexOf('javascript') > -1) return;
        else if(href.indexOf('?') > -1)
        {
            $(this).attr('href', href + '&' + rand);
        }
        else
        {
            $(this).attr('href', href + '?' + rand);
        }
    });
}
//fan setup
function setupSelect(num){
    if(num == 'auto'){
        $("select[name=speed]").attr("disabled",true).addClass('layui-disabled');
    }else if(num == 'manual'){
        $("select[name=speed]").attr("disabled",false).removeClass('layui-disabled');
    }
}

//请求到成功为止
function selftest(){
    $.ajax({// #/innocfg/defaultVID
        type: "GET",
        url: "/conf/defaultVID?v="+new Date,
        cache: false,
        data: '',
        dataType: "text",
        success: function(json) {
            layer.closeAll('loading');
            setcookie('defaultVID',json);
            $(".Frequency-tipcon-Voltage .tip1").text(json);
            layer.msg('success');
            //setcookie('login',true);
            //window.location.href='generalsetup.html?action=submit&'+ Math.random();
        },error:function() {
            setTimeout('selftest()',3000);
        }
    });
}
//只调用一次
function selftestone(){
    $.ajax({// #/innocfg/defaultVID
        type: "GET",
        url: "/conf/defaultVID?v="+new Date,
        data: '',
        dataType: "text",
        success: function(json) {
            setcookie('defaultVID',json);
            $(".Frequency-tipcon-Voltage .tip1").text(json);
            $('select[name=Voltage]').val(json);
        }
    });
}

function logo(){
    layui.use('layer',function(){
        var layer = layui.layer;
        var html = '<div class="border-ra5"><div class="layui-row p5"><br/><div class="imgupload layui-clear"><div class="fl text-right"></div><div class="imgupload02 fl p5"><input name="nologo" value="0" type="radio" checked="checked" onchange="nologo(this);" /> <label style="padding-right: 15px;">With Logo</label><input name="nologo" value="1" type="radio" onchange="nologo(this);" /> <label>Without Logo</label></div></div><div class="imgupload layui-clear"></div><div class="imgupload layui-clear"><div class="fl"><div class="fl col col1"><button type="button" class="layui-btn layui-btn-small mr10" id="file">Choose logo</button></div><div class="fl col col2"><input type="file" name="file" style="display: none;" onchange="handleFile(this)" /><input type="text" name="fileName" class="form-control w180 mr10" /></div><div class="fl col col3"><div class="layui-btn Update layui-btn-small enterclick" onclick="Update();"><i class="layui-icon"></i>Apply</div><div class="layui-btn layui-btn-warm Update layui-btn-small resetlogo" onclick="resetlogo();">Reset Logo</div></div></div></div></div><div class="p5" id="upload_tip"><span style="color:red;font-weight:bold;">*Note:</span>Format: .jpg,.jpeg,.png,.gif　Size: no more than 512KB<br></div></div>';
        layer.open({
            type: 1,
            skin: 'layui-layer-rim', //加上边框
            area: ['500px', '160px'], //宽高
            content: html
        });
    });
}

function selfteststate()
{
    layui.use('layer',function(){
        var layer = layui.layer;
        $.ajax({
            type: "POST",
            url: "../cgi-bin/selfteststate.py",
            data: '',
            dataType: "json",
            beforeSend:function(){
                layer.closeAll('loading');
                layer.load();
            },
            success:function(data) {
                layer.closeAll('loading');
                if(data.result == 'true')
                {
                    layer.msg('Auto vol search is running. This will take about 30 minutes, please wait patiently...',{time:0,icon:16,shade:0.01,area:[,]});
                }
                else
                {
                    layer.closeAll('loading');
                    //layer.msg('success');
                }
            },error:function()
            {
                //layer.msg('error');
            }
        });
    });
}
