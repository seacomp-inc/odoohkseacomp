odoo.define('chatter_label.chatter_label', function (require) {
'use strict';

    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb;

    ajax.loadXML('/chatter_label/static/src/xml/chatter_label.xml', qweb);

});