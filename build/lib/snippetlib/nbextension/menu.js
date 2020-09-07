define([
    "require",
    "jquery",
    "base/js/namespace",
], function (require, $, Jupyter) {
    "use strict";

    function insert_snippet_code (snippet_code, insert_as_new_cell) {
        if (insert_as_new_cell) {
            var new_cell = Jupyter.notebook.insert_cell_above('code');
            new_cell.set_text(snippet_code);
            new_cell.focus_cell();
        } else {
            var selected_cell = Jupyter.notebook.get_selected_cell();
            Jupyter.notebook.edit_mode();
            selected_cell.code_mirror.replaceSelection(snippet_code, 'around');
        }
    }

    function callback_insert_snippet (evt) {
        var insert_as_new_cell = false;
        insert_snippet_code($(evt.currentTarget).data('snippet-code'), insert_as_new_cell);
    }

    function build_menu_element (menu_item_spec, direction) {
        var element = $('<li/>');

        if (typeof menu_item_spec == 'string') {
            if (menu_item_spec != '---') {
                console.log('Don\'t understand sub-menu string "' + menu_item_spec + '"');
                return null;
            }
            return element.addClass('divider');
        }

        var a = $('<a/>')
            .attr('href', '#')
            .html(menu_item_spec.name)
            .appendTo(element);
        if (menu_item_spec.hasOwnProperty('snippet')) {
            var snippet = menu_item_spec.snippet;
            if (typeof snippet == 'string' || snippet instanceof String) {
                snippet = [snippet];
            }
            a.attr({
                'title' : "",
                'data-snippet-code' : snippet.join('\n'),
            })
            .on('click', callback_insert_snippet)
            .addClass('snippet');
        }
        else if (menu_item_spec.hasOwnProperty('internal-link')) {
            a.attr('href', menu_item_spec['internal-link']);
        }
        else if (menu_item_spec.hasOwnProperty('external-link')) {
            a.empty();
            a.attr({
                'target' : '_blank',
                'title' : 'Opens in a new window',
                'href' : menu_item_spec['external-link'],
            });
            $('<i class="fa fa-external-link menu-icon pull-right"/>').appendTo(a);
            $('<span/>').html(menu_item_spec.name).appendTo(a);
        }

        if (menu_item_spec.hasOwnProperty('sub-menu')) {
            element
                .addClass('dropdown-submenu')
                .toggleClass('dropdown-submenu-left', direction === 'left');
            var sub_element = $('<ul class="dropdown-menu"/>')
                .toggleClass('dropdown-menu-compact', menu_item_spec.overlay === true)
                .appendTo(element);

            var new_direction = (menu_item_spec['sub-menu-direction'] === 'left') ? 'left' : 'right';
            for (var j=0; j<menu_item_spec['sub-menu'].length; ++j) {
                var sub_menu_item_spec = build_menu_element(menu_item_spec['sub-menu'][j], new_direction);
                if(sub_menu_item_spec !== null) {
                    sub_menu_item_spec.appendTo(sub_element);
                }
            }
        }
       
        return element;
    }

    function menu_setup (menu_item_specs, sibling, insert_before_sibling) {
        for (var i=0; i<menu_item_specs.length; ++i) {
            var menu_item_spec;
            if (insert_before_sibling) {
                menu_item_spec = menu_item_specs[i];
            } else {
                menu_item_spec = menu_item_specs[menu_item_specs.length-1-i];
            }
            var direction = (menu_item_spec['menu-direction'] == 'left') ? 'left' : 'right';
            var menu_element = build_menu_element(menu_item_spec, direction);

            if ($(sibling).parent().is('ul.nav.navbar-nav')) {
                menu_element
                    .addClass('dropdown')
                    .removeClass('dropdown-submenu dropdown-submenu-left');
                menu_element.children('a')
                    .addClass('dropdown-toggle')
                    .attr({
                        'data-toggle' : 'dropdown',
                        'aria-expanded' : 'false'
                    });
            }
            
            
            menu_element[insert_before_sibling ? 'insertBefore': 'insertAfter'](sibling);
            
            window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub, menu_element[0]]);
        }


        //Add button to add your own snippets
            
  //     menu_element.append('<button id="sniptbn"> Add your snippets here</button>');

   /*     $(document).ready(function(){

            $('#sniptbn').on('click',function(){
               let params = `scrollbars=no,resizable=yes,status=yes,location=no,toolbar=yes,menubar=yes,width=600,height=300,left=100,top=100`;

               var win = window.open('http://localhost:5000','upload your snippet',params);
               
            })               
            
        }

        )
       
      */ 
    }
    
    return {
       menu_setup : menu_setup,
    };

});
