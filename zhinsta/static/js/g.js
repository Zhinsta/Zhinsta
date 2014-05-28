if (typeof ukey === 'undefined') {
    ukey = '';
}

var Apis = {
    like: function(mid, success) {
        $.get(
            '/apis/like/',
            {mid: mid, action: 'like'},
            function(data) {
                if (data.result === 'ok' && success) {
                    success();
                }
            },
            'json'
        );
    },
    unlike: function(mid, success) {
        $.get(
            '/apis/like/',
            {mid: mid, action: 'unlike'},
            function(data) {
                if (data.result === 'ok' && success) {
                    success();
                }
            },
            'json'
        );
    },
    islike: function(mid, success) {
        $.get(
            '/apis/islike/',
            {mid: mid},
            function(data) {
                if (success) {
                    success(data.result);
                }
            },
            'json'
        );
    },
    follow: function(ukey, success) {
        $.get(
            '/apis/follow/',
            {ukey: ukey, action: 'follow'},
            function(data) {
                if (data.result === 'ok' && success) {
                    success();
                }
            },
            'json'
        );
    },
    unfollow: function(ukey, success) {
        $.get(
            '/apis/follow/',
            {ukey: ukey, action: 'unfollow'},
            function(data) {
                if (data.result === 'ok' && success) {
                    success();
                }
            },
            'json'
        );
    }
};

var Utils = {};
/**
 * 用于替代字符串拼接的模板函数
 *      G.format( '{1} name is {2}!', { 1: 'Her', 2: 'Mo' });
 *      G.format( '{v} is good!', 'JavaScript' );
 *      G.format( '{s} is good!', '{s}', 'JavaScript' );
 *      G.format( '<1> name is <2>!', { 1: 'Her', 2: 'Mo' }, /<([^<>]+)>/g);
 * @param {string} tmpl 模板字符串
 * @param {string/object} key 如果是字符串则是键值；
 *                            如果是object则是Map,key为键值，value为替换值;
 *                            如果没有第三个参数，则key为{v}，value为此值
 * @param {string/regexp} val 如果key是字符串，则val是被替换值
 *                            如果key是Map，且有val，则val是搜索key的正则，
 *                            例如：/<([^<>]+)>\/g
 * @return {string} 替换成功后的值
 */
Utils.format = function(tmpl, _key, _val) {
    if (!_key) {
        return tmpl;
    }
    var val;

    if (typeof _key !== 'object') {
        var key = _val ? _key : '{v}';
        val = _val || _key;
        return tmpl.replace(new RegExp(key, 'g'), ('' + val));
    } else {
        var obj = _key;
        return tmpl.replace(_val || /\{([^{}]+)\}/g, function(match, key) {
            val = obj[key];
            return (val !== undefined) ? ('' + val) : '';
        });
    }
};

$('#log').ajaxError(function(e) {
    alert('抱歉出错了，请刷新页面重试。' +
          '如果依旧失败，请联系Zhinsta。Blog: http://zhinsta.diandian.com');
});

/**
 * 提示组件，用于页面上的小tip。例如第一次登录时候的“今日推荐”链接下的提示
 * @eg:
 *      toolTip( container, option, closeCallback );
 *      container 为position为relative的祖先元素
 *      option = {
 *          msg: 显示的html
 *          position: 坐标值[top,left]
 *          coordinates: 相对坐标系，jquery对象或选择符，提示的坐标值是相对于coordinates和position计算得到，可选
 *          direction: 小箭头的方向:up,down,left,right，默认为up
 *          offset: 小箭头与提示框的偏移距离，用于调整小箭头位置，默认为0
 *          width: 宽度
 *      },
 *      closeCallback 关闭时候的回调函数
 *
 */
(function() {
    var html = '<div class="tooltip" style="position:absolute;z-index:999;padding:9px;background-color:#FFFED8;border:1px solid #B2B196;box-shadow:3px 3px 0 rgba(0,0,0,0.15);border-radius:1px;color:#666;font-size:14px;">' +
                    '{msg}' +
                    '<b style="{pointBStyle}"><s style="{pointSStyle}"></s></b>' +
                '</div>';
    var offsets = {
            up: 'left',
            down: 'left',
            right: 'top',
            left: 'top'
        };
    var pointBStyles = {
            up: 'top:-20px;border-bottom-style:solid;border-bottom-color:#B2B196;',
            down: 'bottom:-20px;border-top-style:solid;border-top-color:#B2B196;',
            right: 'right:-20px;border-left-style:solid;border-left-color:#B2B196;',
            left: 'left:-20px;border-right-style:solid;border-right-color:#B2B196;'
        };
    var pointSStyles = {
            up: 'top:-8px;left:-9px;border-bottom-style:solid;border-bottom-color:#FFFED8;',
            down: 'top:-10px;left:-9px;border-top-style:solid;border-top-color:#FFFED8;',
            right: 'top:-9px;left:-10px;border-left-style:solid;border-left-color:#FFFED8;',
            left: 'top:-9px;left:-8px;border-right-style:solid;border-right-color:#FFFED8;'
        };
    var toolTip = function( container, option, closeCallback ) {
            var msg = option.msg,
                position = option.position,
                coordinates = $(option.coordinates),
                direction = option.direction || 'up',
                offset = option.offset || 0,
                width = option.width,
                $con = $(container),                    // 容器
                conOffset = $con.offset(),
                $toolTip = $(Utils.format(html, {        // tooltip
                                msg: msg,
                                direction: direction,
                                pointSStyle: 'position:absolute;border-width:9px;border-color:transparent;border-style:dashed;width:0;height:0;font-size:0;'+pointSStyles[direction],
                                pointBStyle: 'position:absolute;border-width:10px;border-color:transparent;border-style:dashed;width:0;height:0;font-size:0;'+pointBStyles[direction]
                            }));
            $con.css('position','relative');
            // 显示toolTip
            function show() {
                $toolTip.css({
                    top: position[0],
                    left: position[1],
                    width: width
                });
                $( 'b', $toolTip ).css( offsets[direction], offset );
                $con.append( $toolTip );
            }
            // 移除此toolTip
            function remove() {
                $toolTip.remove();
                closeCallback();
            }

            if ( coordinates.length ) {
                coordinates = coordinates.position();
                position[0] += coordinates.top;
                position[1] += coordinates.left;
            }
            show();
            return {
                remove: remove,
                $toolTip: $toolTip
            };
        };

    $.fn.tooltip = function(container, option) {
        toolTip(container || this[0], option);
    };
})();



$(function() {
    if (typeof gLogined !== 'undefined' && gLogined) {
        var timeout;
        var jsLove3Tpl = {
            like: '<a href="javascript:void(0);" class="jsLove3" ' +
                'data-action="unlike" data-mid="{mid}">' +
                '<i class="icon-heart loved"></i>' +
            '</a>',
            unlike: '<a href="javascript:void(0);" class="jsLove3" ' +
                'data-action="like" data-mid="{mid}">' +
                '<i class="icon-heart"></i>' +
            '</a>'
        };

        $('#photoList')
            .on('mouseenter', 'li', function(e) {
                var $me = $(this);
                if ($me.data('loaded')) {
                    return;
                }

                if (timeout) {
                    clearTimeout(timeout);
                }

                timeout = setTimeout(function() {
                    timeout = null;
                    $me.data('loaded', true);

                    var $love = $me.find('.jsLove3');
                    var mid = $love.data('mid');
                    if (mid) {
                        Apis.islike(mid, function(result) {
                            var tpl = result ? jsLove3Tpl.like : jsLove3Tpl.unlike;
                            $love.replaceWith(Utils.format(tpl, {mid: mid}));
                        });
                    }
                }, 1000);
            })
            .on('click', '.jsLove3', function(e) {
                var $me = $(this);
                var action = $me.data('action');
                var mid = $me.data('mid');
                var api = Apis[action];

                api(mid, function() {
                    $me.replaceWith(
                        Utils.format(jsLove3Tpl[action],{mid: mid})
                    );
                });
            });
    }

    /**
     * like & unlike
     */
    $('body').on('click', '.jsLove,.jsLove2', function(e) {
        e.preventDefault();
        if (this.sign) {
            return;
        }
        this.sign = true;

        if (typeof gLogined === 'undefined' || !gLogined) {
            var after = $('<span></span>').insertBefore(this);
            $(this).tooltip(after, {
                msg: '请先<a href="/">登录</a>',
                position: [-36, 0],
                offset: 8,
                width: 80,
                direction: 'down'
            });
            return;
        }

        var $me = $(this);
        var action = $me.data('action');
        var number = parseInt($me.data('num'), 10);
        var mid = $me.data('mid');
        var api = Apis[action];
        var template;
        if ($me.hasClass('jsLove')) {
            template = {
                like: '<a href="javascript:void(0);" class="jsLove" ' +
                        'data-action="unlike" data-num="{n}" data-mid="{mid}">' +
                        '<i class="icon-heart loved"></i>' +
                        '<span class="loved">{n}</span>' +
                      '</a>',
                unlike: '<a href="javascript:void(0);" class="jsLove" ' +
                        'data-action="like" data-num="{n}" data-mid="{mid}">' +
                        '<i class="icon-heart"></i><span>{n}</span>' +
                      '</a>'
            };
        } else {
            template = {
                like: '<a href="javascript:void(0);" class="jsLove2" ' +
                        'data-action="unlike" data-num="{n}" data-mid="{mid}">' +
                        '<span class="loved">{n}</span>' +
                        '<i class="icon-heart loved"></i>' +
                      '</a>',
                unlike: '<a href="javascript:void(0);" class="jsLove2" ' +
                        'data-action="like" data-num="{n}" data-mid="{mid}">' +
                        '<span>{n}</span><i class="icon-heart"></i>' +
                      '</a>'
            };
        }

        api(mid, function() {
            if (action === 'like') {
                number++;
            } else {
                number--;
            }
            $me.replaceWith(
                Utils.format(
                    template[action],
                    {
                        mid: mid,
                        n: number
                    }
                )
            );
        });
    });

    /**
     * follow & unfollow
     */
    $('body').on('click', '.jsFollow', function(e) {
        e.preventDefault();
        if (this.sign) {
            return;
        }
        this.sign = true;

        if (typeof gLogined === 'undefined' || !gLogined) {
            var after = $('<span>&nbsp;</span>').insertAfter(this);
            $(this).tooltip(after, {
                msg: '请先<a href="/">登录</a>',
                position: [32, -60],
                offset: 10,
                width: 80
            });
            return;
        }

        var $me = $(this);
        var action = $me.data('action');
        var ukey = $me.data('ukey');
        var api = Apis[action];
        var template = {
            follow: '<a href="#" class="jsFollow info-follow" ' +
                        'data-action="unfollow" data-ukey="{v}" ' +
                        'title="取消关注">正在关注</a>',
            unfollow: '<a href="#" class="jsFollow info-follow" ' +
                        'data-action="follow" data-ukey="{v}" ' +
                        'title="关注TA">未关注</a>'
        };

        api(ukey, function() {
            $me.replaceWith(
                Utils.format(
                    template[action],
                    ukey
                )
            );
        });
    });


    /**
     * loading style
     */
    function Stopwatch() {
        this.$stopwatch =
            $('<span id="stopwatch" class="stopwatch" style="display:none;">' +
                '<span class="stopwatch-tp"></span>' +
                '<span class="stopwatch-hd"></span>' +
                '<span class="stopwatch-ft"></span>' +
                '<span class="stopwatch-back"></span>' +
                '<span class="stopwatch-fore"></span>' +
                '<span class="stopwatch-point"></span>' +
            '</span>');
        this.$stopwatch.appendTo('body');
        if (this.useTween()) {
            this._transform = Modernizr.prefixed('transform');
        }
    }

    Stopwatch.prototype.useTween = function() {
        return !Modernizr.cssanimations && typeof TWEEN !== 'undefined';
    };

    Stopwatch.prototype.start = function() {
        var me = this;
        if (me.starting) {
            return;
        }
        me.starting = true;
        me.$stopwatch
            .removeClass('stopwatch-done')
            .css('display', 'block')
            .addClass('bounceInDown');
        if (me.useTween()) {
            var $point = me.$stopwatch.find('.stopwatch-point');
            var tween = new TWEEN.Tween({ deg: -90 })
                .to({deg: 3510}, 10000)
                .onUpdate(function () {
                    $point.css(
                        me._transform,
                        'rotate(' + this.deg + 'deg)'
                    );
                })
                .start();

            (function animate() {
                me._timeout = setTimeout(animate, 50);
                TWEEN.update();
            })();
        }
    };

    Stopwatch.prototype.stop = function() {
        var me = this;
        if (!me.starting) {
            return;
        }
        me.starting = false;
        me.$stopwatch
            .removeClass('bounceInDown')
            .addClass('stopwatch-done')
            .fadeOut();
        if (me.useTween()) {
            TWEEN.removeAll();
            clearTimeout(me._timeout);
        }
    };

    var watch = new Stopwatch();
    $(document)
        .ajaxStart(function() {
            watch.start();
        })
        .ajaxStop(function() {
            watch.stop();
        });
});
