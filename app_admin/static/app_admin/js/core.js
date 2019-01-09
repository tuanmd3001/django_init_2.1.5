$(function ($) {
    "use strict";
    var _side_menu = $('.nav.nav-list');

    //Handle active url
    if (typeof ACTIVE_URL !== 'undefined') {
        var _active_menu = _side_menu.find("a[href='" + ACTIVE_URL + "']");
        if (_active_menu.length > 0) {
            _active_menu.addClass('active');

            var _active_menu_li = _active_menu.closest('li');
            if (_active_menu_li.length > 0) {
                _active_menu_li.addClass('active');

                var _parent_menu = _active_menu_li.closest('li');
                if (_parent_menu.length > 0 && _parent_menu.hasClass('submenu')) {
                    _parent_menu.addClass('open');
                }
            }
        }
    }
});