"undefined"==typeof ukey&&(ukey="");var Apis={like:function(t,o){$.get("/apis/like/",{mid:t,action:"like"},function(t){"ok"===t.result&&o&&o()},"json")},unlike:function(t,o){$.get("/apis/like/",{mid:t,action:"unlike"},function(t){"ok"===t.result&&o&&o()},"json")},islike:function(t,o){$.get("/apis/islike/",{mid:t},function(t){o&&o(t.result)},"json")},follow:function(t,o){$.get("/apis/follow/",{ukey:t,action:"follow"},function(t){"ok"===t.result&&o&&o()},"json")},unfollow:function(t,o){$.get("/apis/follow/",{ukey:t,action:"unfollow"},function(t){"ok"===t.result&&o&&o()},"json")}},Utils={};Utils.format=function(t,o,i){if(!o)return t;var a;if("object"!=typeof o){var e=i?o:"{v}";return a=i||o,t.replace(new RegExp(e,"g"),""+a)}var n=o;return t.replace(i||/\{([^{}]+)\}/g,function(t,o){return a=n[o],void 0!==a?""+a:""})},$("#log").ajaxError(function(){alert("抱歉出错了，请刷新页面重试。如果依旧失败，请联系Zhinsta。Blog: http://zhinsta.diandian.com")}),function(){var t='<div class="tooltip" style="position:absolute;z-index:999;padding:9px;background-color:#FFFED8;border:1px solid #B2B196;box-shadow:3px 3px 0 rgba(0,0,0,0.15);border-radius:1px;color:#666;font-size:14px;">{msg}<b style="{pointBStyle}"><s style="{pointSStyle}"></s></b></div>',o={up:"left",down:"left",right:"top",left:"top"},i={up:"top:-20px;border-bottom-style:solid;border-bottom-color:#B2B196;",down:"bottom:-20px;border-top-style:solid;border-top-color:#B2B196;",right:"right:-20px;border-left-style:solid;border-left-color:#B2B196;",left:"left:-20px;border-right-style:solid;border-right-color:#B2B196;"},a={up:"top:-8px;left:-9px;border-bottom-style:solid;border-bottom-color:#FFFED8;",down:"top:-10px;left:-9px;border-top-style:solid;border-top-color:#FFFED8;",right:"top:-9px;left:-10px;border-left-style:solid;border-left-color:#FFFED8;",left:"top:-9px;left:-8px;border-right-style:solid;border-right-color:#FFFED8;"},e=function(e,n,s){function l(){m.css({top:g.top+c[0],left:g.left+c[1],width:h}),$("b",m).css(o[p],u),$("body").append(m)}function r(){m.remove(),s()}var d=n.msg,c=n.position,f=$(n.coordinates),p=n.direction||"up",u=n.offset||0,h=n.width,v=$(e),g=v.offset(),m=$(Utils.format(t,{msg:d,direction:p,pointSStyle:"position:absolute;border-width:9px;border-color:transparent;border-style:dashed;width:0;height:0;font-size:0;"+a[p],pointBStyle:"position:absolute;border-width:10px;border-color:transparent;border-style:dashed;width:0;height:0;font-size:0;"+i[p]}));return f.length&&(f=f.position(),c[0]+=f.top,c[1]+=f.left),l(),{remove:r,$toolTip:m}};$.fn.tooltip=function(t){e(this[0],t)}}(),$(function(){function t(){this.$loading=$("#loading")}if("undefined"!=typeof gLogined&&gLogined){var o,i={like:'<a href="javascript:void(0);" class="jsLove3" data-action="unlike" data-mid="{mid}"><i class="icon-heart loved"></i></a>',unlike:'<a href="javascript:void(0);" class="jsLove3" data-action="like" data-mid="{mid}"><i class="icon-heart"></i></a>'};$("#photoList").on("mouseenter","li",function(){var t=$(this);t.data("loaded")||(o&&clearTimeout(o),o=setTimeout(function(){o=null,t.data("loaded",!0);var a=t.find(".jsLove3"),e=a.data("mid");e&&Apis.islike(e,function(t){var o=t?i.like:i.unlike;a.replaceWith(Utils.format(o,{mid:e}))})},1e3))}).on("click",".jsLove3",function(){var t=$(this),o=t.data("action"),a=t.data("mid"),e=Apis[o];e(a,function(){t.replaceWith(Utils.format(i[o],{mid:a}))})})}$("body").on("click",".jsLove",function(t){if(t.preventDefault(),!this.sign){if(this.sign=!0,"undefined"==typeof gLogined||!gLogined)return void $(this).tooltip({msg:'请先<a href="/">登录</a>',position:[-50,0],offset:8,width:80,direction:"down"});var o,i=$(this),a=i.data("action"),e=parseInt(i.data("num"),10),n=i.data("mid"),s=Apis[a];o=i.hasClass("jsLove")?{like:'<a href="javascript:void(0);" class="jsLove" data-action="unlike" data-num="{n}" data-mid="{mid}"><i class="icon-heart loved"></i><span class="loved">{n}</span></a>',unlike:'<a href="javascript:void(0);" class="jsLove" data-action="like" data-num="{n}" data-mid="{mid}"><i class="icon-heart"></i><span>{n}</span></a>'}:{like:'<a href="javascript:void(0);" class="jsLove2" data-action="unlike" data-num="{n}" data-mid="{mid}"><span class="loved">{n}</span><i class="icon-heart loved"></i></a>',unlike:'<a href="javascript:void(0);" class="jsLove2" data-action="like" data-num="{n}" data-mid="{mid}"><span>{n}</span><i class="icon-heart"></i></a>'},s(n,function(){"like"===a?e++:e--,i.replaceWith(Utils.format(o[a],{mid:n,n:e}))})}}),$("body").on("click",".jsFollow",function(t){if(t.preventDefault(),!this.sign){if(this.sign=!0,"undefined"==typeof gLogined||!gLogined)return void $(this).tooltip({msg:'请先<a href="/">登录</a>',position:[32,0],offset:10,width:80});var o=$(this),i=o.data("action"),a=o.data("ukey"),e=Apis[i],n={follow:'<a href="#" class="jsFollow info-follow" data-action="unfollow" data-ukey="{v}" title="取消关注">正在关注</a>',unfollow:'<a href="#" class="jsFollow info-follow" data-action="follow" data-ukey="{v}" title="关注TA">未关注</a>'};e(a,function(){o.replaceWith(Utils.format(n[i],a))})}}),t.prototype.start=function(){var t=this;t.starting||(t.starting=!0,t.$loading.css({transition:"width 3s",width:"60%",opacity:"1"}))},t.prototype.stop=function(){var t=this;t.starting&&(t.starting=!1,t.$loading.css({transition:"width 1s, opacity 1s",width:"100%",opacity:"0"}))};var a=new t;$(document).ajaxStart(function(){a.start()}).ajaxStop(function(){a.stop()})});