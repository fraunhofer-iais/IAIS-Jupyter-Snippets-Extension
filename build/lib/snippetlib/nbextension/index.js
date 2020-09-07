define([
    "require",
    "jquery",
    "base/js/namespace",
    "./menu",
], function (require, $, Jupyter, menu) {
    "use strict";

    var options = {
        sibling: undefined,
        menus : [],
        hooks: {
            pre_config: undefined,
            post_config: undefined,
        }
    };

    var cfg = {
        insert_as_new_cell: false,
        insert_before_sibling: false,
        include_custom_menu: false,
        include_submenu: {},
        sibling_selector: '#help_menu',
        top_level_submenu_goes_left: true
    };

    function config_loaded_callback () {
        cfg = $.extend(true, cfg, Jupyter.notebook.config.data.iais_snippets);
        var menuUrl = require.toUrl("/menu");

        return $.getJSON(menuUrl).then(function(data) {
            options.menus = data;

            if (options.hooks.post_config !== undefined) {
                options.hooks.post_config();
            }

            if (options.sibling === undefined) {
                options.sibling = $(cfg.sibling_selector).parent();
                if (options.sibling.length < 1) {
                    options.sibling = $("#help_menu").parent();
                }
            }
        });
    }

    function load_ipython_extension () {
        $('<link/>', {
            rel: 'stylesheet',
            type:'text/css',
            href: require.toUrl('./menu.css')
        }).appendTo('head');

        Jupyter.notebook.config.loaded.then(
            config_loaded_callback
        ).then(function () {
            menu.menu_setup(
              options.menus,
              options.sibling,
              cfg.insert_before_sibling
            );
        });
    }

    return {
        load_ipython_extension : load_ipython_extension,
    };
});
