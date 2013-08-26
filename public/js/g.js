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

$(function() {
    /**
     * like & unlike
     */
    $('body').on('click', '.jsLove', function(e) {
        e.preventDefault();
        if (this.sign) {
            return;
        }
        this.sign = true;
        var $me = $(this);
        var action = $me.data('action');
        var number = parseInt($me.data('num'), 10);
        var mid = $me.data('mid');
        var api = Apis[action];
        var template = {
            like: '<a href="#" class="jsLove" ' +
                    'data-action="unlike" data-num="{n}" data-mid="{mid}">' +
                    '<i class="icon-heart loved"></i>' +
                    '<span class="loved">{n}</span>' +
                  '</a>',
            unlike: '<a href="#" class="jsLove" ' +
                    'data-action="like" data-num="{n}" data-mid="{mid}">' +
                    '<i class="icon-heart"></i><span>{n}</span>' +
                  '</a>'
        };

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
        var $me = $(this);
        var action = $me.data('action');
        var ukey = $me.data('ukey');
        var api = Apis[action];
        var template = {
            follow: '<a href="#" class="jsFollow" ' +
                        'data-action="unfollow" data-ukey="{v}" ' +
                        'title="取消关注">正在关注</a>',
            unfollow: '<a href="#" class="jsFollow" ' +
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
