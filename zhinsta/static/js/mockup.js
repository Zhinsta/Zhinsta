var Apis = {
    like: function(mid, success) {
        success();
    },
    unlike: function(mid, success) {
        success();
    },
    islike: function(mid, success) {
        setTimeout(function () {
            success(true);
        }, 1000);
    },
    follow: function(ukey, success) {
        success();
    },
    unfollow: function(ukey, success) {
        success();
    }
};
